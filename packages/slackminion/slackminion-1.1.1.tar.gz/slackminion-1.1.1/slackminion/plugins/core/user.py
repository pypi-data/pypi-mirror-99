from slackminion.plugin.base import BasePlugin

from . import version

try:
    from . import commit
except ImportError:
    commit = 'HEAD'


class UserManager(BasePlugin):
    """
    Loads and stores user information
    """

    def on_load(self):
        self._dont_save = True  # Don't save this plugin's state on shutdown
        self.users = {}
        self.admins = {}
        if 'bot_admins' in self._bot.config:
            self.admins = self._bot.config['bot_admins']
        setattr(self._bot, 'user_manager', self)

        return super(UserManager, self).on_load()

    def get(self, userid):
        """Retrieve user by id"""
        if userid in self.users:
            return self.users[userid]
        return None

    def get_by_username(self, username):
        """Retrieve user by username"""
        res = [x for x in list(self.users.values()) if x.username == username]
        if len(res) > 0:
            return res[0]
        return None

    def set(self, user):
        """
        Adds a user object to the user manager

        user - a SlackUser object
        """

        self.log.debug("Loading user information for %s/%s", user.id, user.username)
        self.load_user_info(user)
        self.log.debug("Loading user rights for %s/%s", user.id, user.username)
        self.load_user_rights(user)
        self._add_user_to_cache(user)
        return user

    def _add_user_to_cache(self, user):
        if user.id not in list(self.users.keys()):
            self.users[user.id] = user
            self.log.debug("Added user: %s/%s", user.id, user.username)

    def load_user_info(self, user):
        """Loads additional user information and stores in user object"""
        # We have no additional information to load, but a child plugin
        # might want to override this
        pass

    def load_user_rights(self, user):
        """Sets permissions on user object"""
        if user.username in self.admins:
            user.set_admin(True)
        user.set_admin(False)
