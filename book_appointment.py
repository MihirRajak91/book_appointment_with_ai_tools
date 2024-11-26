import sqlite3
import dateparser
from datetime import datetime, timedelta

def create_database(db_name="appointments.db"):
    """
    Creates a SQLite database with users and appointments tables if they don't exist.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )
    """)

    # Create the appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def save_user(name, phone, email, db_name="appointments.db"):
    """
    Saves a user to the database, ensuring unique phone and email.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, phone, email) VALUES (?, ?, ?)
        """, (name, phone, email))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        cursor.execute("""
            SELECT id FROM users WHERE phone = ? OR email = ?
        """, (phone, email))
        user_id = cursor.fetchone()[0]
        return user_id
    finally:
        conn.close()

def save_appointment(user_id, appointment_date, db_name="appointments.db"):
    """
    Saves an appointment to the database for a given user.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (user_id, appointment_date) VALUES (?, ?)
    """, (user_id, appointment_date))
    conn.commit()
    conn.close()

def fetch_all_users(db_name="appointments.db"):
    """
    Fetches all users from the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def fetch_all_appointments(db_name="appointments.db"):
    """
    Fetches all appointments from the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT appointments.id, users.name, users.phone, users.email, appointments.appointment_date 
        FROM appointments
        JOIN users ON appointments.user_id = users.id
    """)
    appointments = cursor.fetchall()
    conn.close()
    return appointments

def correct_typos(user_input):
    """
    Corrects common typos in the user input.
    """
    corrections = {
        "moday": "monday",
        "tuesay": "tuesday",
        "wedesday": "wednesday",
        "thrusday": "thursday",
        "firday": "friday",
        "satureday": "saturday",
        "sundayy": "sunday"
    }
    for typo, correct in corrections.items():
        user_input = user_input.lower().replace(typo, correct)
    return user_input

def parse_date(user_input):
    """
    Parses natural language date input to a complete date format (YYYY-MM-DD).
    Returns the date string if valid, None otherwise.
    """
    user_input = correct_typos(user_input) 

    # Debugging output to understand how the input is being processed
    print(f"Processing user input: '{user_input}'")

    # Parse the date using dateparser
    parsed_date = dateparser.parse(
        user_input,
        settings={
            'PREFER_DATES_FROM': 'future', 
            'RELATIVE_BASE': datetime.now()  
        }
    )

    if parsed_date:
        print(f"Parsed date: {parsed_date}")  
    else:
        print("Dateparser could not parse the input.")  

    # Ensure the parsed date is in the future
    if parsed_date and parsed_date >= datetime.now():
        return parsed_date.strftime('%Y-%m-%d')

    # Fallback to simple parsing if dateparser fails
    return parse_simple_dates(user_input)

def parse_simple_dates(user_input):
    """
    A fallback parser for simple natural language dates like 'next Monday'.
    """
    user_input = user_input.lower().strip()
    days_of_week = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }

    today = datetime.now()
    if "next" in user_input:
        day = user_input.split()[-1]
        if day in days_of_week:
            target_day = days_of_week[day]
            days_ahead = (target_day - today.weekday() + 7) % 7
            days_ahead = days_ahead or 7  
            parsed_date = today + timedelta(days=days_ahead)
            print(f"Fallback parsed date: {parsed_date}")  
            return parsed_date.strftime('%Y-%m-%d')
    return None
