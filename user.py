


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonuymous(self):
        return False

    def get_id(self):
        return self.username