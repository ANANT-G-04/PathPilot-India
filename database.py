
import sqlite3


def create_table(connection):

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            college TEXT,
            career TEXT,
            education TEXT,
            year TEXT,
            interests TEXT,
            subjects TEXT,
            skills TEXT
        )
    """)


def save_student(name, college, career, education, year, interests, subjects, skills):

    connection = sqlite3.connect("pathpilot.db")

    create_table(connection)

    connection.execute("""
        INSERT INTO students
        (name, college, career, education, year, interests, subjects, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, college, career, education, year, interests, subjects, skills))

    connection.commit()
    connection.close()


def get_students():

    connection = sqlite3.connect("pathpilot.db")

    create_table(connection)

    result = connection.execute("SELECT * FROM students")

    students = result.fetchall()

    connection.close()

    return students


def get_latest_student():

    connection = sqlite3.connect("pathpilot.db")

    create_table(connection)

    result = connection.execute("""
        SELECT name, college, career, education, year, interests, subjects, skills
        FROM students
        ORDER BY id DESC
        LIMIT 1
    """)

    student = result.fetchone()

    connection.close()

    if student is None:
        return None

    return {
        "name": student[0],
        "college": student[1],
        "career": student[2],
        "education": student[3],
        "year": student[4],
        "interests": student[5],
        "subjects": student[6],
        "skills": student[7]
    }


def clear_students():

    connection = sqlite3.connect("pathpilot.db")

    create_table(connection)

    connection.execute("DELETE FROM students")

    connection.commit()
    connection.close()


