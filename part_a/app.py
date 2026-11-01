import re
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "week8a-student-mgmt-secret-key"

# In-memory student store for Week 8(a)
students = [
    {"id": 1, "roll_no": "22CS101", "name": "Aarav Sharma", "department": "Computer Science & Engineering", "email": "aarav@college.edu"},
    {"id": 2, "roll_no": "23IT204", "name": "Bhavya Patel", "department": "Information Technology", "email": "bhavya@college.edu"},
    {"id": 3, "roll_no": "21AI305", "name": "Chirag Verma", "department": "Artificial Intelligence & Data Science", "email": "chirag@college.edu"},
]
next_id = 4


@app.route("/")
def index():
    """Displays student list."""
    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    """Validates and adds a new student record."""
    global next_id
    roll_no = request.form.get("roll_no", "").strip()
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()
    email = request.form.get("email", "").strip()

    # Server-side validation
    if not roll_no or not name or not department or not email:
        flash("All fields are mandatory.", "error")
        return redirect(url_for("index"))

    if not re.match(r"^[A-Za-z0-9\-]+$", roll_no):
        flash("Roll number must be alphanumeric.", "error")
        return redirect(url_for("index"))

    if not re.match(r"^[A-Za-z\s\.]+$", name):
        flash("Student name must contain only letters and spaces.", "error")
        return redirect(url_for("index"))

    if any(s["roll_no"].lower() == roll_no.lower() for s in students):
        flash(f"Student with Roll No '{roll_no}' already exists.", "error")
        return redirect(url_for("index"))

    students.append({
        "id": next_id,
        "roll_no": roll_no,
        "name": name,
        "department": department,
        "email": email
    })
    next_id += 1
    flash(f"Student '{name}' ({roll_no}) added successfully!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id: int):
    """Deletes a student record."""
    global students
    student = next((s for s in students if s["id"] == id), None)
    if student:
        students = [s for s in students if s["id"] != id]
        flash(f"Student '{student['name']}' deleted.", "success")
    else:
        flash("Student record not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
