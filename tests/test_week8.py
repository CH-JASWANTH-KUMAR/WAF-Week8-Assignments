import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Part A
from part_a.app import app as app_a
# Part B
from part_b.app import app as app_b
# Part C
from part_c.app import app as app_c
from part_c.database import init_db, get_courses, is_already_registered


class TestWeek8Assignments(unittest.TestCase):
    """Automated Test Suite for Week 8 Laboratory Experiments."""

    def setUp(self):
        self.client_a = app_a.test_client()
        self.client_b = app_b.test_client()
        self.client_c = app_c.test_client()

    # Part (a) Tests
    def test_part_a_get(self):
        res = self.client_a.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Student Information System", res.data)

    def test_part_a_add_and_delete(self):
        payload = {
            "roll_no": "24CS999",
            "name": "Test Student A",
            "department": "Computer Science & Engineering",
            "email": "test.a@college.edu"
        }
        res = self.client_a.post("/add", data=payload, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Test Student A", res.data)
        self.assertIn(b"24CS999", res.data)

        # Duplicate rejection
        dup_res = self.client_a.post("/add", data=payload, follow_redirects=True)
        self.assertIn(b"already exists", dup_res.data)

    # Part (b) Tests
    def test_part_b_get_and_add(self):
        res = self.client_b.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Student Information Management", res.data)

        payload = {
            "roll_no": "24IT888",
            "name": "Test Student B",
            "department": "Information Technology",
            "year": "2nd Year"
        }
        add_res = self.client_b.post("/add", data=payload, follow_redirects=True)
        self.assertEqual(add_res.status_code, 200)
        self.assertIn(b"Test Student B", add_res.data)

    # Part (c) Tests
    def test_part_c_course_registration(self):
        init_db()
        res = self.client_c.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Online Student Course Registration System", res.data)
        self.assertIn(b"Cloud Computing &amp; Distributed Architecture", res.data)

        courses = get_courses()
        self.assertGreater(len(courses), 0)
        c_id = courses[0]["id"]

        reg_data = {
            "student_name": "Kiran Rao",
            "roll_no": "24EC777",
            "email": "kiran.rao@college.edu",
            "course_id": str(c_id)
        }
        reg_res = self.client_c.post("/register", data=reg_data, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b"Kiran Rao", reg_res.data)
        self.assertIn(b"24EC777", reg_res.data)

        # Prevent duplicate registration
        dup_res = self.client_c.post("/register", data=reg_data, follow_redirects=True)
        self.assertIn(b"already registered for this course", dup_res.data)


if __name__ == "__main__":
    unittest.main()
