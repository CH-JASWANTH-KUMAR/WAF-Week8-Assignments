import os
import sqlite3
from typing import List, Optional, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "course_registration.db")


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Connects to SQLite database with Row factory."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Initializes tables for courses and student registrations."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            instructor TEXT NOT NULL,
            credits INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            email TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses (id),
            UNIQUE(roll_no, course_id)
        )
        """
    )
    conn.commit()

    # Seed courses if empty
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        sample_courses = [
            ("CS-401", "Cloud Computing & Distributed Architecture", "Dr. A. Verma", 4),
            ("IT-302", "Web Application Frameworks & Security", "Prof. R. Krishnan", 3),
            ("AI-405", "Machine Learning & Neural Networks", "Dr. S. Mitchell", 4),
            ("DS-303", "Data Engineering & Big Data Analytics", "Prof. M. Iyer", 3),
            ("CS-408", "Full Stack Development with Python & React", "Prof. P. Sundaram", 3)
        ]
        cursor.executemany(
            "INSERT INTO courses (code, title, instructor, credits) VALUES (?, ?, ?, ?)",
            sample_courses
        )
        conn.commit()

    conn.close()


def get_courses(db_path: Optional[str] = None) -> List[sqlite3.Row]:
    """Retrieves all active courses with registered student counts."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT c.*, COUNT(r.id) AS enrolled_count
        FROM courses c
        LEFT JOIN registrations r ON c.id = r.course_id
        GROUP BY c.id
        ORDER BY c.code ASC
        """
    )
    courses = cursor.fetchall()
    conn.close()
    return courses


def register_student(name: str, roll_no: str, email: str, course_id: int, db_path: Optional[str] = None) -> int:
    """Registers a student for a course using parameterized SQL."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO registrations (student_name, roll_no, email, course_id)
        VALUES (?, ?, ?, ?)
        """,
        (name.strip(), roll_no.strip(), email.strip(), int(course_id))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def is_already_registered(roll_no: str, course_id: int, db_path: Optional[str] = None) -> bool:
    """Checks if a student is already registered for this specific course."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM registrations WHERE roll_no = ? AND course_id = ?",
        (roll_no.strip(), int(course_id))
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def get_all_registrations(db_path: Optional[str] = None) -> List[sqlite3.Row]:
    """Retrieves all registrations joined with course details."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.id, r.student_name, r.roll_no, r.email, r.registered_at,
               c.code AS course_code, c.title AS course_title, c.credits, c.instructor
        FROM registrations r
        JOIN courses c ON r.course_id = c.id
        ORDER BY r.id DESC
        """
    )
    records = cursor.fetchall()
    conn.close()
    return records


def cancel_registration(id: int, db_path: Optional[str] = None) -> bool:
    """Cancels a student course enrollment."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registrations WHERE id = ?", (id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success


def get_total_enrollments_count(db_path=None) -> int:
    """Helper added by collaborator to query total registrations count."""
    conn = get_db_connection(db_path)
    count = conn.execute("SELECT COUNT(*) FROM registrations").fetchone()[0]
    conn.close()
    return count

