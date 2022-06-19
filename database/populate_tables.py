import config
import sqlite3
import csv
import random

import emails
import user
from datetime import datetime


def populate_users(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users')
    with open('user_mock.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            mock_user = user.new_user(row[0], row[1])
            mock_user.insert_into_database(cursor)

    admin_user = user.new_user('admin', 'admin')
    admin_user.insert_into_database(cursor)


def get_lorem_ipsum(word_count):
    with open('lorem_ipsum.txt') as lorem:
        text = lorem.read()
        text = text.split()
        text = text*(word_count//len(text) + 1)
        return ' '.join(text[:word_count])


def populate_emails(conn, email_count = 200):
    conn.execute('DELETE FROM Emails')
    for _ in range(email_count):
        to, from_ = conn.execute('SELECT userid FROM Users ORDER BY random() LIMIT 2').fetchall()
        to = to[0]
        from_ = from_[0]
        title = get_lorem_ipsum(random.randint(3, 10))
        body = get_lorem_ipsum(random.randint(15, 100))
        date = random.randint(datetime.timestamp(datetime(year=2000, month=1, day=1)), datetime.timestamp(datetime(year=2025, month=12, day=31)))
        date = datetime.fromtimestamp(date).isoformat()
        email = emails.Email(to, from_, title, body, date)
        email.insert_into_database(connection)


if __name__ == '__main__':
    connection = sqlite3.connect(config.DATABASE_LOCATION)
    populate_users(connection)
    populate_emails(connection)
    connection.commit()
    connection.close()