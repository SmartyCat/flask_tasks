import sqlite3 as sq

users = [("Alex", 17), ("Bob", 22), ("John", 15)]


with sq.connect("users.db") as con:
    cur = con.cursor()


    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER
                )
                """
    )
    cur.executemany("INSERT INTO users(name,age) VALUES(?, ?)",users)
    cur.execute("UPDATE users SET age=18 WHERE name='Alex'")
    cur.execute("DELETE FROM users WHERE age < 16")
    cur.execute("SELECT name, age FROM users")
    print(cur.fetchall())
