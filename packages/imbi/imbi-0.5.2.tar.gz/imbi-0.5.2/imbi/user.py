"""
User Model supporting both LDAP and PostgreSQL data sources

"""
import datetime
import logging
import typing
from itertools import chain

from tornado import web

from imbi import ldap, timestamp

LOGGER = logging.getLogger(__name__)


class Group:
    """Group class to represent a single group a user is a member of"""
    __slots__ = ['name', 'permissions']

    def __init__(self, name: str, permissions: typing.List[str]):
        self.name = name
        self.permissions = sorted(permissions or [])

    def __iter__(self):
        return iter([('name', self.name), ('permissions', self.permissions)])

    def __repr__(self):
        return '<Group name={} permissions={}>'.format(
            self.name, self.permissions)


class User:
    """Holds the user attributes and interfaces with the directory server"""

    REFRESH_AFTER = datetime.timedelta(minutes=5)

    SQL_AUTHENTICATE = """\
       UPDATE v1.users
          SET last_seen_at = CURRENT_TIMESTAMP
        WHERE username = %(username)s
          AND password = %(password)s
          AND user_type = 'internal'
    RETURNING username;"""

    SQL_AUTHENTICATE_TOKEN = """\
       UPDATE v1.users
          SET last_seen_at = CURRENT_TIMESTAMP
        WHERE username IN (
                SELECT username
                  FROM v1.authentication_tokens
                 WHERE token = %(token)s
                   AND expires_at > CURRENT_TIMESTAMP)
    RETURNING username, user_type, external_id;"""  # nosec

    SQL_GROUPS = """\
    SELECT a.name, a.permissions
      FROM v1.groups AS a
      JOIN v1.group_members AS b ON b.group = a.name
     WHERE b.username = %(username)s;"""

    SQL_REFRESH = """\
    SELECT username, created_at, last_seen_at, user_type, external_id,
           email_address, display_name
      FROM v1.users
     WHERE username = %(username)s;"""

    SQL_UPDATE_GROUP_MEMBERSHIPS_FROM_LDAP = """\
    SELECT maintain_group_membership_from_ldap_groups AS groups
      FROM maintain_group_membership_from_ldap_groups(%(username)s,
                                                      %(groups)s);"""

    SQL_UPDATE_LAST_SEEN_AT = """\
        UPDATE v1.users
           SET last_seen_at = CURRENT_TIMESTAMP
         WHERE username = %(username)s
     RETURNING last_seen_at"""

    SQL_UPDATE_USER_FROM_LDAP = """\
    INSERT INTO v1.users (username, user_type, external_id,
                          display_name, email_address, last_seen_at)
         VALUES (%(username)s,
                 %(user_type)s,
                 %(external_id)s,
                 %(display_name)s,
                 %(email_address)s,
                 CURRENT_TIMESTAMP)
    ON CONFLICT (username)
             DO UPDATE SET email_address = EXCLUDED.email_address,
                             external_id = EXCLUDED.external_id,
                               user_type = EXCLUDED.user_type,
                                password = NULL,
                            last_seen_at = CURRENT_TIMESTAMP
                    WHERE users.username = EXCLUDED.username
      RETURNING last_seen_at;"""

    def __init__(self, application,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 token: typing.Optional[str] = None) -> None:
        self._application = application
        self._ldap = ldap.Client(application.settings['ldap'])
        self._ldap_conn = None
        self.username = username
        self.created_at: typing.Optional[datetime.datetime] = None
        self.last_refreshed_at: typing.Optional[datetime.datetime] = None
        self.last_seen_at: typing.Optional[datetime.datetime] = None
        self.user_type = 'internal'
        self.external_id: typing.Optional[str] = None
        self.email_address: typing.Optional[str] = None
        self.display_name: typing.Optional[str] = None
        self.password = password
        self.token = token
        self.groups: typing.List[Group] = []
        self.permissions: typing.List[str] = []

    def __repr__(self):
        return '<User username={} user_type={} permissions={}>'.format(
            self.username, self.user_type, self.permissions)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        """Intercept the assignment of a signed password and decrypt it
        if it appears to be encrypted.

        """
        if name == 'password' \
                and self._application.is_encrypted_value(value):
            value = self._application.decrypt_value(
                name, value).decode('utf-8')
        object.__setattr__(self, name, value)

    def as_dict(self) -> dict:
        """Return a representation of the user data as a dict"""
        return {
            'username': self.username,
            'user_type': self.user_type,
            'external_id': self.external_id,
            'created_at': timestamp.isoformat(self.created_at),
            'last_seen_at': timestamp.isoformat(self.last_seen_at),
            'email_address': self.email_address,
            'display_name': self.display_name,
            'groups': [g.name for g in self.groups],
            'password': self._application.encrypt_value(
                'password', self.password),
            'permissions': self.permissions,
            'last_refreshed_at': timestamp.isoformat(self.last_refreshed_at)
        }

    async def authenticate(self) -> bool:
        """Validate that the current session is valid. Returns boolean
        if successful.

        """
        if self.token:
            return await self._token_auth()
        result = await self._db_auth()
        if not result and self._ldap.is_enabled:
            return await self._ldap_auth()
        return result

    def has_permission(self, value: str) -> bool:
        """Check all of the permissions assigned to the user, returning
        `True` if the role is assigned through any group memberships

        :param value: The role to check for

        """
        return value in self.permissions

    @staticmethod
    def on_postgres_error(_metric_name: str, exc: Exception) -> None:
        raise web.HTTPError(500, 'System error')

    async def refresh(self) -> None:
        """Update the attributes from LDAP"""
        if self.external_id and self._ldap.is_enabled:
            await self._ldap_refresh()
        else:
            await self._db_refresh()

    @property
    def should_refresh(self) -> bool:
        """Returns True if the amount of time that has passed since the last
        refresh has exceeded the threshold.

        """
        age = timestamp.age(self.last_refreshed_at)
        LOGGER.debug('Last refresh: %s < %s == %s, %s < %s == %s',
                     self.REFRESH_AFTER, age, self.REFRESH_AFTER < age,
                     self.last_refreshed_at, self.last_seen_at,
                     self.last_refreshed_at < self.last_seen_at)
        return ((self.REFRESH_AFTER < age) or
                (self.last_refreshed_at < self.last_seen_at))

    async def update_last_seen_at(self) -> None:
        """Update the last_seen_at column in the database for the user"""
        async with self._application.postgres_connector(
                on_error=self.on_postgres_error) as conn:
            result = await conn.execute(
                self.SQL_UPDATE_LAST_SEEN_AT,
                {'username': self.username},
                'user-update-last-seen-at')
            self.last_seen_at = result.row['last_seen_at']

    def _assign_values(self, data: dict) -> None:
        """Assign values from the cursor row to the instance"""
        for key, value in data.items():
            setattr(self, key, value)

    async def _db_auth(self) -> bool:
        """Validate via the v1.users table in the database"""
        LOGGER.debug('Authenticating with the database')
        async with self._application.postgres_connector(
                on_error=self.on_postgres_error) as conn:
            result = await conn.execute(
                self.SQL_AUTHENTICATE,
                {'username': self.username,
                 'password': self._application.encrypt_value(
                     'password', self.password) if self.password else None},
                'user-authenticate')
            if not result.row_count:
                self._reset()
                return False
        await self._db_refresh()
        return True

    async def _db_groups(self) -> typing.List[Group]:
        """Return the groups for the user as a list of group objects"""
        async with self._application.postgres_connector(
                on_error=self.on_postgres_error) as conn:
            result = await conn.execute(
                self.SQL_GROUPS, {'username': self.username},
                'user-groups')
            return [Group(**r) for r in result]

    async def _db_refresh(self) -> None:
        """Fetch the latest values from the database"""
        async with self._application.postgres_connector(
                on_error=self.on_postgres_error) as conn:
            result = await conn.execute(
                self.SQL_REFRESH, {'username': self.username},
                'user-refresh')
            self._assign_values(result.row)
        self.groups = await self._db_groups()
        self.permissions = sorted(set(
            chain.from_iterable([g.permissions for g in self.groups])))
        self.last_refreshed_at = max(
            timestamp.utcnow(), self.last_seen_at or timestamp.utcnow())

    async def _ldap_auth(self) -> bool:
        """Authenticate via LDAP"""
        if not self.password:
            LOGGER.debug('Can not LDAP authenticate without a password')
            return False
        LOGGER.debug('Authenticating via LDAP')
        self._conn = await self._ldap.connect(self.username, self.password)
        if self._conn:
            LOGGER.debug('Authenticated as %s', self.username)
            self.user_type = 'ldap'
            result = self._conn.extend.standard.who_am_i()
            self.external_id = result[3:].strip()
            await self._ldap_refresh()
            return True
        self._reset()
        return False

    async def _ldap_refresh(self) -> None:
        """Update the attributes from LDAP"""
        LOGGER.debug('Refreshing attributes from LDAP server')
        attrs = await self._ldap.attributes(self._conn, self.external_id)
        LOGGER.debug('Attributes: %r', attrs)
        self.display_name = attrs.get('displayName', attrs['cn'])
        self.email_address = attrs.get('mail')

        async with self._application.postgres_connector(
                on_error=self.on_postgres_error) as conn:
            result = await conn.execute(
                self.SQL_UPDATE_USER_FROM_LDAP,
                {
                    'username': self.username,
                    'user_type': 'ldap',
                    'external_id': self.external_id,
                    'display_name': self.display_name,
                    'email_address': self.email_address
                }, 'user-update')
            self.last_seen_at = result.row['last_seen_at']

        # Update the groups in the database and get the group names
        ldap_groups = await self._ldap.groups(self._conn, self.external_id)
        async with self._application.postgres_connector(
                on_error=self.on_postgres_error) as conn:
            await conn.callproc(
                'v1.maintain_group_membership_from_ldap_groups',
                (self.username, ldap_groups),
                'user-maintain-groups')

        # Update the groups attribute
        self.groups = await self._db_groups()
        self.permissions = sorted(set(
            chain.from_iterable([g.permissions for g in self.groups])))
        self.last_refreshed_at = max(timestamp.utcnow(), self.last_seen_at)

    def _reset(self) -> None:
        """Reset the internally assigned values associated with this user
        object.

        """
        self._ldap_conn = None
        self.created_at: typing.Optional[datetime.datetime] = None
        self.last_seen_at: typing.Optional[datetime.datetime] = None
        self.user_type = 'internal'
        self.external_id: typing.Optional[str] = None
        self.email_address: typing.Optional[str] = None
        self.display_name: typing.Optional[str] = None
        self.groups: typing.List[Group] = []
        self.permissions: typing.List[str] = []
        self.last_refreshed_at: typing.Optional[datetime.datetime] = None

    async def _token_auth(self) -> bool:
        """Validate via v1.authentication_tokens table"""
        LOGGER.debug('Authenticating with token: %s', self.token)
        async with self._application.postgres_connector(
                on_error=self.on_postgres_error) as conn:
            result = await conn.execute(
                self.SQL_AUTHENTICATE_TOKEN, {'token': self.token},
                'user-token-auth')
            if not result.row_count:
                return False
            self._assign_values(result.row)
        await self._db_refresh()
        return True
