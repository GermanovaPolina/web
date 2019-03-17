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
                             password_hash VARCHAR(128),
                             communities VARCHAR(1000)
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
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id), ))
        row = cursor.fetchone()
        return row

    def get_name(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (str(user_name), ))
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
                          (user_name, password_hash, communities) 
                          VALUES (?,?,?)''', (user_name, password_hash, ''))
        cursor.close()
        self.connection.commit()

    def update(self, user_name, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET user_name = '{}' WHERE id = {}'''.format(user_name, str(user_id)))
        cursor.close()
        self.connection.commit()

    def unfollow(self, user_id, community_id):
        cursor = self.connection.cursor()
        communities = self.get(user_id)[3].split()
        if str(community_id) in communities:
            communities.remove(str(community_id))
            cursor.execute('''UPDATE users SET communities = '{}' WHERE id = {}'''.format(' '.join(communities), str(user_id)))
        cursor.close()
        self.connection.commit()

    def follow(self, user_id, community_id):
        cursor = self.connection.cursor()
        communities = self.get(user_id)[3].split()
        if not str(community_id) in communities:
            communities.append(str(community_id))
            cursor.execute('''UPDATE users SET communities = '{}' WHERE id = {}'''.format(' '.join(communities), str(user_id)))
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
                             user_id INTEGER
                             )''')
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

    def get_all(self, user_id=None, community_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?",
                           (str(user_id), ))
        elif community_id:
            cursor.execute("SELECT * FROM news WHERE community = ?",
                           (str(community_id),))
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
            cursor.execute('''UPDATE news SET hashtag = '{}' WHERE id = {}'''.format(hashtag, str(news_id)))
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
                             users VARCHAR(10000)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, bio, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO communities 
                          (title, bio, users) 
                          VALUES (?,?,?)''', (title, bio, str(user_id) + ' '))
        cursor.close()
        self.connection.commit()

    def get(self, community_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM communities WHERE id = ?", (str(community_id), ))
        row = cursor.fetchone()
        return row

    def get_name(self, community_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM communities WHERE title = ?", (str(community_name), ))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM communities")
        rows = cursor.fetchall()
        return rows

    def update(self, community_id, title=None, bio=None):
        cursor = self.connection.cursor()
        if title:
            cursor.execute('''UPDATE communities SET title = '{}' WHERE id = {}'''.format(title, str(community_id)))
        if bio:
            cursor.execute('''UPDATE communities SET bio = '{}' WHERE id = {}'''.format(bio, str(community_id)))
        cursor.close()
        self.connection.commit()

    def unfollow(self, user_id, community_id):
        cursor = self.connection.cursor()
        users = self.get(community_id)[3].split()
        if str(user_id) in users:
            users.remove(str(user_id))
            cursor.execute('''UPDATE communities SET users = '{}' WHERE id = {}'''.format(' '.join(users), str(community_id)))
        cursor.close()
        self.connection.commit()

    def follow(self, user_id, community_id):
        cursor = self.connection.cursor()
        users = self.get(community_id)[3].split()
        if str(user_id) not in users:
            users.append(str(user_id))
            cursor.execute('''UPDATE communities SET users = '{}' WHERE id = {}'''.format(' '.join(users), str(community_id)))
        cursor.close()
        self.connection.commit()

    def delete(self, community_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM communities WHERE id = ?''', (str(community_id), ))
        cursor.close()
        self.connection.commit()