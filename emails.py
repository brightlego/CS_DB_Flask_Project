import random
import sqlite3
import config


class Email:
    def __init__(self, to_, from_, title, body, datetime, email_id=None):
        self.__to = to_
        self.__from = from_
        self.__title = title
        self.__body = body
        self.__datetime = datetime
        if email_id is None:
            email_id = random.getrandbits(32)
        self.__email_id = email_id

    def get_to(self):
        return self.__to

    def get_from(self):
        return self.__from

    def get_title(self):
        return self.__title

    def get_body(self):
        return self.__body

    def get_datetime(self):
        return self.__datetime

    def get_email_id(self):
        return self.__email_id

    def insert_into_database(self, connection=None):
        created_connection = False
        if connection is None:
            created_connection = True
            connection = sqlite3.connect(config.DATABASE_LOCATION)

        try:
            connection.execute('''INSERT INTO 
                                 Emails (emailID, fromID, toID, datetime, title, body)
                                 VALUES (?, ?, ?, ?, ?, ?)''',
                         (
                             self.get_email_id(),
                             self.get_from(),
                             self.get_to(),
                             self.get_datetime(),
                             self.get_title(),
                             self.get_body()
                         ))
        finally:
            if created_connection:
                connection.close()
