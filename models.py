import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()

    def update(self, user_name, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET username = '{}' WHERE id = {}'''.format(user_name, str(user_id)))
        cursor.close()
        self.connection.commit()

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id), ))
        cursor.close()
        self.connection.commit()


class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             community INTEGER, 
                             title VARCHAR(100),
                             hashtag VARCHAR(100),
                             content VARCHAR(1000),
                             date VARCHAR(1000),
                             user_id INTEGER,
                             edited INTEGER
                             )''')
        cursor.execute('''ALTER TABLE news
                            DEFAULT 0 FOR EDITED''')
        cursor.close()
        self.connection.commit()

    def insert(self, community, title, hashtag, content, date, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (commmunity, title, hashtag, content, date, user_id) 
                          VALUES (?,?,?,?,?,?)''', (community, title, content, date, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id), ))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?",
                           (str(user_id), ))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id), ))
        cursor.close()
        self.connection.commit()

    def update(self, news_id, title=None, hashtag=None, content=None):
        cursor = self.connection.cursor()
        if title:
            cursor.execute('''UPDATE news SET title = '{}' WHERE id = {}'''.format(title, str(news_id)))
        if content:
            cursor.execute('''UPDATE news SET content = '{}' WHERE id = {}'''.format(content, str(news_id)))
        if hashtag:
            cursor.execute('''UPDATE news SET content = '{}' WHERE id = {}'''.format(hashtag, str(news_id)))
        cursor.execute('UPDATE news SET edited = 1 WHERE id = {}')
        cursor.close()
        self.connection.commit()


class CommunityModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS communities 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             title VARCHAR(100),
                             bio VARCHAR(1000),
                             admin INTEGER,
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, bio, admin):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO communities 
                          (title, bio, admin) 
                          VALUES (?,?,?)''', (tite, bio, str(admin)))
        cursor.close()
        self.connection.commit()

    def get(self, community_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM communities WHERE id = ?", (str(community_id), ))
        row = cursor.fetchone()
        return row

    def get_all(self, community_id=None):
        cursor = self.connection.cursor()
        if community_id:
            cursor.execute("SELECT * FROM communties WHERE user_id = ?",
                           (str(community_id), ))
        else:
            cursor.execute("SELECT * FROM communities")
        rows = cursor.fetchall()
        return rows

    def delete(self, community_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM communities WHERE id = ?''', (str(community_id), ))
        cursor.close()
        self.connection.commit()