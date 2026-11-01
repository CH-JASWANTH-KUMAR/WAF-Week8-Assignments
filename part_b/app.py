import re
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "week8b-github-workflow-secret-key"

students = [
    {"id": 1, "roll_no": "23IT102", "name": "Diya Sengupta", "department": "Information Technology", "year": "2nd Year"},
    {"id": 2, "roll_no": "22CS215", "name": "Farhan Akhtar", "department": "Computer Science", "year": "3rd Year"},
    {"id": 3, "roll_no": "24DS301", "name": "Gauri Sundaram", "department": "Data Science & AI", "year": "1st Year"}
]
next_id = 4


@app.route("/")
def index():
    """Lists all students."""
    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    """Adds a new student with validation."""
    global next_id
    roll_no = request.form.get("roll_no", "").strip()
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()
    year = request.form.get("year", "1st Year").strip()

    if not roll_no or not name or not department:
        flash("Roll number, name, and department are required.", "error")
        return redirect(url_for("index"))

    if not re.match(r"^[A-Za-z0-9\-]+$", roll_no):
        flash("Roll number must be alphanumeric.", "error")
        return redirect(url_for("index"))

    if any(s["roll_no"].lower() == roll_no.lower() for s in students):
        flash(f"Student with Roll No '{roll_no}' already exists.", "error")
        return redirect(url_for("index"))

    students.append({
        "id": next_id,
        "roll_no": roll_no,
        "name": name,
        "department": department,
        "year": year
    })
    next_id += 1
    flash(f"Student '{name}' registered successfully!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id: int):
    """Deletes a student."""
    global students
    students = [s for s in students if s["id"] != id]
    flash("Student record removed.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5002, debug=True)
