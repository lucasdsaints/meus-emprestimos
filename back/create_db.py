import sqlite3

connection = sqlite3.connect('storage.db')
cursor = connection.cursor()

script = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
"""
cursor.execute(script)

script = """
CREATE TABLE IF NOT EXISTS friends (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    user INT NOT NULL,
    FOREIGN KEY (user) REFERENCES user(id),
    UNIQUE(name, user)
);
"""
cursor.execute(script)

script = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    user INT NOT NULL,
    FOREIGN KEY (user) REFERENCES user(id),
    UNIQUE(name, user)
);
"""
cursor.execute(script)

script = """
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY,
    user INT NOT NULL,
    friend INT NOT NULL,
    item INT NOT NULL,
    loan_type INT NOT NULL DEFAULT 0, -- 0: amigo -> usuario | 1: usuario --> amigo
    returned TEXT NOT NULL DEFAULT "NO",
    FOREIGN KEY (user) REFERENCES users(id)
        ON DELETE RESTRICT,
    FOREIGN KEY (friend) REFERENCES friends(id)
        ON DELETE RESTRICT,
    FOREIGN KEY (item) REFERENCES items(id)
        ON DELETE RESTRICT
);
"""
cursor.execute(script)

connection.commit()
connection.close()