import hashlib
import base64
import random
import sqlite3
import config


def new_user(username, password):
    user = User(username)
    user.set_password(password)
    return user


def user_from_username(username):
    with sqlite3.connect(config.DATABASE_LOCATION) as conn:
        cur = conn.execute('SELECT username, password_hash, password_salt, userid FROM Users WHERE username=? LIMIT 1', (username,))
        results = cur.fetchall()
        if len(results) == 0:
            raise ValueError(f'No users of username {username}')
        user = User(results[0][0], results[0][1], results[0][2], results[0][3])
        return user


def user_from_userid(userid):
    with sqlite3.connect(config.DATABASE_LOCATION) as conn:
        cur = conn.execute('SELECT username, password_hash, password_salt, userid FROM Users WHERE userid=? LIMIT 1', (userid,))
        results = cur.fetchall()
        if len(results) == 0:
            raise ValueError(f'No users of username {userid}')
        user = User(results[0][0], results[0][1], results[0][2], results[0][3])
        return user


class User:
    def __init__(self, username, password_hash=None, salt=None, userid=None):
        self.__username = username
        self.__password_hash = password_hash
        self.__salt = salt

        if userid is None:
            userid = random.getrandbits(32)

        self.__userid = userid

    @staticmethod
    def hash_password(password, salt):
        if isinstance(password, str):
            password = password.encode('UTF-8')
        if isinstance(salt, str):
            salt = salt.encode('UTF-8')

        hash_ = hashlib.sha512()
        hash_.update(password + salt)
        hash_ = hash_.digest()

        return base64.b64encode(hash_)

    @staticmethod
    def generate_salt():
        salt = random.getrandbits(128)
        salt = hex(salt)[2:]
        return salt

    def set_password(self, raw_password):
        self.__salt = self.generate_salt()
        self.__password_hash = self.hash_password(raw_password, self.__salt)

    def is_password(self, password):
        return self.hash_password(password, self.__salt) == self.__password_hash

    def get_username(self):
        return self.__username

    def get_salt(self):
        return self.__salt

    def get_userid(self):
        return self.__userid

    def get_password_hash(self):
        return self.__password_hash

    def insert_into_database(self, connection=None):
        created_connection = False
        if connection is None:
            created_connection = True
            connection = sqlite3.connect(config.DATABASE_LOCATION)

        try:
            connection.execute('''INSERT INTO
                               USERS (userid, username, password_hash, password_salt) 
                               VALUES (?, ?, ?, ?)''',
                   (
                       self.get_userid(),
                       self.get_username(),
                       self.get_password_hash(),
                       self.get_salt()
                   ))
        finally:
            if created_connection:
                connection.close()