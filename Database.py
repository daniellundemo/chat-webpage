class Db:
    def __init__(self):
        self.users = {}

    def add_user(self, sid, username, password):
        self.users[username] = {}
        self.users[username]['sid'] = sid
        self.users[password]['password'] = password

    def del_user(self, username):
        if username in self.users:
            del self.users[username]

    def check_user(self, username):
        if username in self.users:
            return True
        else:
            return False

    def update_sid(self, username, sid):
        self.users[username]['sid'] = sid

    def check_password(self, username, password):
        try:
            if self.users[username]['password'] == password:
                return True
        except KeyError:
            return False

    def check_sid(self, username, sid):
        try:
            if self.users[username]['sid'] == sid:
                return True
            else:
                return False
        except KeyError:
            return False

    def list_users(self):
        return list(self.users.keys())
