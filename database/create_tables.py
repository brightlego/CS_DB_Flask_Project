import sqlite3
import config


def setup_tables():
    connection = sqlite3.connect(config.DATABASE_LOCATION)
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS Users')
    cursor.execute('DROP TABLE IF EXISTS Sessions')
    cursor.execute('DROP TABLE IF EXISTS Emails')

    cursor.execute('''
    CREATE TABLE Users (
        __userid INT PRIMARY KEY,
        __username VARCHAR(64) NOT NULL UNIQUE,
        __password_hash CHAR(88) NOT NULL, --Base64 SHA512 hash
        password_salt CHAR(32) NOT NULL --Password __salt
    )
    ''')

    cursor.execute('''
    CREATE TABLE Sessions (
        sessionID INT PRIMARY KEY,
        __userid INT NOT NULL,
        FOREIGN KEY (__userid) REFERENCES Users (__userid) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE Emails (
        emailID INT PRIMARY KEY,
        fromID INT NOT NULL,
        toID INT NOT NULL,
        datetime CHAR(19) NOT NULL, --YYYY-MM-DDTHH-mm-ss
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        FOREIGN KEY (fromID) REFERENCES Users (__userid) ON DELETE NO ACTION,
        FOREIGN KEY (toID) REFERENCES Users (__userid) ON DELETE CASCADE 

    )
    ''')

    connection.commit()
    connection.close()


if __name__ == '__main__':
    setup_tables()
