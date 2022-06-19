import sqlite3
import config


def setup_tables():
    connection = sqlite3.connect(config.DATABASE_LOCATION)
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS Users')
    cursor.execute('DROP TABLE IF EXISTS Sessions')
    cursor.execute('DROP TABLE IF EXISTS Email')

    cursor.execute('''
    CREATE TABLE Users (
        userid INT PRIMARY KEY,
        username VARCHAR(64) NOT NULL,
        password_hash CHAR(88) NOT NULL --Base64 SHA512 hash
    )
    ''')

    cursor.execute('''
    CREATE TABLE Sessions (
        sessionID INT PRIMARY KEY,
        userid INT NOT NULL,
        FOREIGN KEY (userid) REFERENCES Users (userid) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE Emails (
        emailID INT PRIMARY KEY,
        fromID INT NOT NULL,
        toID INT NOT NULL,
        datetime CHAR(19) NOT NULL, --YYYY-MM-DDTHH-mm-ss
        title TEXT NOT NULL,
        body TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


if __name__ == '__main__':
    setup_tables()
