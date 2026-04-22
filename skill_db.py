import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cr = self.conn.cursor()

    def execute(self, query, params=()):
        self.cr.execute(query, params)
        return self.cr

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
        print("Connection To Database Is Closed")


class Auth:
    def __init__(self, db: Database):
        self.db = db

    def login(self):
        name = input("Enter Name: ").strip()
        surname = input("Enter Surname: ").strip()

        self.db.execute(
            "SELECT id FROM users WHERE name = ? AND surname = ?", (name, surname)
        )

        user = self.db.cr.fetchone()

        if user:
            print("Login Successful.")
            return user[0]

        self.db.execute(
            "INSERT INTO users(name, surname) VALUES (?, ?)", (name, surname)
        )

        self.db.commit()

        self.db.execute(
            "SELECT id FROM users WHERE name = ? AND surname = ?", (name, surname)
        )

        user = self.db.cr.fetchone()

        print("User created successfully!")
        return user[0]


class SkillsApp:
    def __init__(self, db: Database, user_id: int):
        self.db = db
        self.user_id = user_id

    def show_skills(self):
        self.db.execute(
            "SELECT name, progress FROM skills WHERE user_id = ?", (self.user_id,)
        )

        results = self.db.cr.fetchall()

        print(f"You Have {len(results)} Skills.")

        for name, progress in results:
            print(f"Skill => {name}, Progress => {progress}%")

    def add_skill(self):
        sk = input("Write Skill Name: ").strip().capitalize()
        prog = int(input("Write Skill Progress: ").strip())

        self.db.execute(
            "SELECT name FROM skills WHERE name = ? AND user_id = ?", (sk, self.user_id)
        )

        if self.db.cr.fetchone():
            print("Skill already exists.")
            return

        self.db.execute(
            "INSERT INTO skills(name, progress, user_id) VALUES (?, ?, ?)",
            (sk, prog, self.user_id),
        )

        print("Skill Added.")

    def delete_skill(self):
        sk = input("Write Skill Name: ").strip().capitalize()

        self.db.execute(
            "DELETE FROM skills WHERE name = ? AND user_id = ?", (sk, self.user_id)
        )

        print("Skill Deleted (if it existed).")

    def update_skill(self):
        sk = input("Write Skill Name: ").strip().capitalize()
        prog = int(input("Write New Progress: ").strip())

        self.db.execute(
            "UPDATE skills SET progress = ? WHERE name = ? AND user_id = ?",
            (prog, sk, self.user_id),
        )

        print("Skill Updated.")


def setup(db):
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        progress INTEGER NOT NULL,
        user_id INTEGER NOT NULL
    )
    """)

    db.commit()


db = Database("app.db")
setup(db)

auth = Auth(db)
user_id = auth.login()

if user_id is None:
    db.close()
    exit()

app = SkillsApp(db, user_id)

input_message = """
What Do You Want To Do?
"s" => Show All Skills
"a" => Add New Skill
"d" => Delete A Skill
"u" => Update Skill Progress
"q" => Quit
Choose Option:
"""

while True:
    choice = input(input_message).strip().lower()

    if choice == "s":
        app.show_skills()

    elif choice == "a":
        app.add_skill()

    elif choice == "d":
        app.delete_skill()

    elif choice == "u":
        app.update_skill()

    elif choice == "q":
        break

    else:
        print("Invalid Option.")

db.commit()
db.close()
print("App Closed.")
