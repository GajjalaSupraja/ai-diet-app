import sqlite3
import bcrypt


# ================= INIT DATABASE =================

def init_db():
    conn = sqlite3.connect("diet.db")
    cursor = conn.cursor()

    # users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password BLOB,
        photo TEXT
    )
    """)

    # diet history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diet_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        age TEXT,
        goal TEXT,
        diet TEXT,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()


# ================= CREATE USER =================

def create_user(name, email, password, photo):

    conn = sqlite3.connect("diet.db")
    cursor = conn.cursor()

    # ✅ Check duplicate email
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone():
        conn.close()
        return False

    # ✅ Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users(name,email,password,photo) VALUES(?,?,?,?)",
        (name, email, hashed, photo)
    )

    conn.commit()
    conn.close()
    return True


# ================= LOGIN USER =================

def login_user(email, password):

    conn = sqlite3.connect("diet.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and user[3]:
        stored_password = user[3]

        # ✅ FIX HERE
        if isinstance(stored_password, str):
            stored_password = stored_password.encode()

        if bcrypt.checkpw(password.encode(), stored_password):
            return user

    return None

# ================= SAVE HISTORY =================

def save_history(user, age, goal, diet, result):

    conn = sqlite3.connect("diet.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO diet_history(user,age,goal,diet,result) VALUES(?,?,?,?,?)",
        (user, age, goal, diet, result)
    )

    conn.commit()
    conn.close()


# ================= GET HISTORY =================

def get_history(user):

    conn = sqlite3.connect("diet.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM diet_history WHERE user=? ORDER BY id DESC",
        (user,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


# ================= GET USER =================

def get_user(name):

    conn = sqlite3.connect("diet.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE name=?", (name,))
    user = cursor.fetchone()

    conn.close()

    return user


# ================= UPDATE PHOTO =================

def update_photo(name, photo_path):

    conn = sqlite3.connect("diet.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET photo=? WHERE name=?",
        (photo_path, name)
    )

    conn.commit()
    conn.close()