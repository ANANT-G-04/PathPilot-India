
import sqlite3

def save_student(name, college, career,education,year,interests,subjects,skills):

    connection = sqlite3.connect("pathpilot.db")

    connection.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        college TEXT,
        career TEXT
    )
    """)

    # NEW CODE STARTS HERE
    columns = connection.execute(
        "PRAGMA table_info(students)"
    ).fetchall()

    column_names = []

    for column in columns:
        column_names.append(column[1])

    if "education" not in column_names:
        connection.execute(
            "ALTER TABLE students ADD COLUMN education TEXT"
        )
    if "year" not in column_names:
        connection.execute(
        "ALTER TABLE students ADD COLUMN year TEXT"
    )
    if "interests" not in column_names:
        connection.execute(
        "ALTER TABLE students ADD COLUMN interests TEXT"
    )
    if "subjects" not in column_names:
        connection.execute(
        "ALTER TABLE students ADD COLUMN subjects TEXT"
    )
    if "skills" not in column_names:
        connection.execute(
        "ALTER TABLE students ADD COLUMN skills TEXT"
    )
    # NEW CODE ENDS HERE

    connection.execute(
        "INSERT INTO students (name, college, career,education,year,interests,subjects,skills) VALUES (?, ?, ?,?,?,?,?,?)",
        (name, college, career,education,year,interests,subjects,skills)
    )

    connection.commit()
    connection.close()



def get_students():

    connection = sqlite3.connect("pathpilot.db")

    columns = connection.execute(
        "PRAGMA table_info(students)"
    ).fetchall()

    column_names = []

    for column in columns:
        column_names.append(column[1])

    if "education" not in column_names:
        connection.execute(
            "ALTER TABLE students ADD COLUMN education TEXT"
        )

    if "year" not in column_names:
        connection.execute(
            "ALTER TABLE students ADD COLUMN year TEXT"
        )

    if "interests" not in column_names:
        connection.execute(
            "ALTER TABLE students ADD COLUMN interests TEXT"
        )

    if "subjects" not in column_names:
        connection.execute(
            "ALTER TABLE students ADD COLUMN subjects TEXT"
        )

    if "skills" not in column_names:
        connection.execute(
            "ALTER TABLE students ADD COLUMN skills TEXT"
        )

    connection.commit()

    result = connection.execute("SELECT * FROM students")

    students = result.fetchall()

    connection.close()

    return students
def get_latest_student():

    connection = sqlite3.connect("pathpilot.db")

    result = connection.execute("""
        SELECT name, college, career, education,
               year, interests, subjects, skills
        FROM students
        ORDER BY id DESC
        LIMIT 1
    """)

    student = result.fetchone()

    connection.close()

    return student


def clear_students():
    connection = sqlite3.connect("pathpilot.db")

    connection.execute("DELETE FROM students")

    connection.commit()
    connection.close()


