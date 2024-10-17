import sqlite3


def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products_list = cursor.fetchall()
    connection.close()
    return products_list


def is_included(username):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    check = cursor.execute('SELECT COUNT(*) FROM Users WHERE username == ?', (username,)).fetchone()
    connection.commit()
    connection.close()
    if check[0] == 0:
        return False
    else:
        return True



def add_user(username, email, age):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()
    connection.close()
