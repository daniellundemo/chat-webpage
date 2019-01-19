class Db:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        self.users[username] = password

    def del_user(self, username):
        if username in self.users:
            del self.users[username]

    def check_user(self, username):
        if username in self.users:
            return True
        else:
            return False

    def check_password(self, username, password):
        try:
            if self.users[username] == password:
                return True
        except KeyError:
            return False

    def list_users(self):
        return self.users.keys()
