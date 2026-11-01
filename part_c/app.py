import os
import sys
import re

PART_C_DIR = os.path.abspath(os.path.dirname(__file__))
if PART_C_DIR not in sys.path:
    sys.path.insert(0, PART_C_DIR)

from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_courses, register_student, is_already_registered, get_all_registrations, cancel_registration

app = Flask(__name__)
app.secret_key = "week8c-course-registration-secret-key"

# Ensure SQLite schema is ready
init_db()


@app.route("/")
def index():
    """Displays course offerings, registration form, and enrolled registrations."""
    courses = get_courses()
    registrations = get_all_registrations()
    return render_template("index.html", courses=courses, registrations=registrations)


@app.route("/register", methods=["POST"])
def register():
    """Validates inputs and registers student for selected course."""
    student_name = request.form.get("student_name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    email = request.form.get("email", "").strip()
    course_id = request.form.get("course_id", "").strip()

    # Input validation
    if not student_name or not roll_no or not email or not course_id:
        flash("All fields are mandatory for course registration.", "error")
        return redirect(url_for("index"))

    if not re.match(r"^[A-Za-z0-9\-]+$", roll_no):
        flash("Roll number must be alphanumeric (e.g. 23CS502).", "error")
        return redirect(url_for("index"))

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("index"))

    try:
        c_id = int(course_id)
    except ValueError:
        flash("Invalid course selection.", "error")
        return redirect(url_for("index"))

    # Duplicate registration check
    if is_already_registered(roll_no, c_id):
        flash(f"Student '{roll_no}' is already registered for this course.", "error")
        return redirect(url_for("index"))

    register_student(student_name, roll_no, email, c_id)
    flash(f"Student '{student_name}' successfully registered for course!", "success")
    return redirect(url_for("index"))


@app.route("/cancel/<int:id>", methods=["POST"])
def cancel(id: int):
    """Cancels a student registration."""
    success = cancel_registration(id)
    if success:
        flash("Course registration cancelled successfully.", "success")
    else:
        flash("Registration record not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5003, debug=True)
