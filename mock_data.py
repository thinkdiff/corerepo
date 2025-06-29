import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Mock data for the school management system
# This replaces all database dependencies

# Mock user data
MOCK_USERS = {
    1: {"id": 1, "role": "student", "email": "student@test.com", "is_active": True},
    2: {"id": 2, "role": "teacher", "email": "teacher@test.com", "is_active": True},
    3: {"id": 3, "role": "hod", "email": "hod@test.com", "is_active": True},
    4: {"id": 4, "role": "admin", "email": "admin@test.com", "is_active": True},
}

# Mock student data
MOCK_STUDENTS = {
    1: {
        "id": 1,
        "user_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "class": "10A",
        "roll_number": "S001",
        "date_of_birth": "2006-05-15",
        "gender": "Male",
        "contact_number": "+1234567890",
        "address": "123 Main St, City",
        "admission_date": "2020-06-01",
        "profile_image_url": "https://via.placeholder.com/150",
        "department": "Science"
    }
}

# Mock teacher data
MOCK_TEACHERS = {
    2: {
        "id": 2,
        "user_id": 2,
        "first_name": "Dr. Sarah",
        "last_name": "Smith",
        "department": "Physics",
        "designation": "Senior Teacher",
        "qualification": "Ph.D. Physics",
        "contact_number": "+1234567891",
        "joining_date": "2018-03-15",
        "profile_image_url": "https://via.placeholder.com/150",
        "employee_id": "T001"
    }
}

# Mock HOD data
MOCK_HODS = {
    3: {
        "id": 3,
        "user_id": 3,
        "first_name": "Prof. Michael",
        "last_name": "Johnson",
        "department": "Physics",
        "designation": "Head of Department",
        "qualification": "Ph.D. Physics",
        "contact_number": "+1234567892",
        "joining_date": "2015-08-01",
        "profile_image_url": "https://via.placeholder.com/150",
        "employee_id": "H001"
    }
}

# Mock admin data
MOCK_ADMINS = {
    4: {
        "id": 4,
        "user_id": 4,
        "first_name": "Admin",
        "last_name": "User",
        "designation": "System Administrator",
        "contact_number": "+1234567893",
        "profile_image_url": "https://via.placeholder.com/150"
    }
}

# Mock timetable data
MOCK_TIMETABLE = {
    1: [
        {"day": "Monday", "time": "08:00-09:00", "subject": "Physics", "teacher": "Dr. Smith", "room": "101"},
        {"day": "Monday", "time": "09:00-10:00", "subject": "Mathematics", "teacher": "Mr. Brown", "room": "102"},
        {"day": "Monday", "time": "10:00-11:00", "subject": "Chemistry", "teacher": "Dr. Wilson", "room": "103"},
        {"day": "Monday", "time": "11:00-12:00", "subject": "English", "teacher": "Ms. Davis", "room": "104"},
        {"day": "Monday", "time": "12:00-13:00", "subject": "History", "teacher": "Mr. Taylor", "room": "105"},
        {"day": "Tuesday", "time": "08:00-09:00", "subject": "Biology", "teacher": "Dr. Anderson", "room": "106"},
        {"day": "Tuesday", "time": "09:00-10:00", "subject": "Physics", "teacher": "Dr. Smith", "room": "101"},
        {"day": "Tuesday", "time": "10:00-11:00", "subject": "Mathematics", "teacher": "Mr. Brown", "room": "102"},
        {"day": "Tuesday", "time": "11:00-12:00", "subject": "Chemistry", "teacher": "Dr. Wilson", "room": "103"},
        {"day": "Tuesday", "time": "12:00-13:00", "subject": "English", "teacher": "Ms. Davis", "room": "104"},
    ]
}

# Mock attendance data
MOCK_ATTENDANCE = {
    1: [
        {"date": "2024-01-15", "subject": "Physics", "status": "Present"},
        {"date": "2024-01-15", "subject": "Mathematics", "status": "Present"},
        {"date": "2024-01-15", "subject": "Chemistry", "status": "Absent"},
        {"date": "2024-01-16", "subject": "Biology", "status": "Present"},
        {"date": "2024-01-16", "subject": "Physics", "status": "Present"},
        {"date": "2024-01-16", "subject": "Mathematics", "status": "Present"},
        {"date": "2024-01-17", "subject": "Chemistry", "status": "Present"},
        {"date": "2024-01-17", "subject": "English", "status": "Present"},
        {"date": "2024-01-17", "subject": "History", "status": "Present"},
        {"date": "2024-01-18", "subject": "Biology", "status": "Present"},
    ]
}

# Mock assignments data
MOCK_ASSIGNMENTS = {
    1: [
        {
            "id": 1,
            "title": "Physics Lab Report",
            "description": "Complete the lab report for the pendulum experiment",
            "subject": "Physics",
            "due_date": "2024-01-25",
            "max_marks": 100,
            "is_submitted": False,
            "submitted_date": None,
            "marks_obtained": None,
            "teacher": "Dr. Smith"
        },
        {
            "id": 2,
            "title": "Mathematics Problem Set",
            "description": "Solve problems 1-20 from Chapter 5",
            "subject": "Mathematics",
            "due_date": "2024-01-22",
            "max_marks": 50,
            "is_submitted": True,
            "submitted_date": "2024-01-20",
            "marks_obtained": 45,
            "teacher": "Mr. Brown"
        },
        {
            "id": 3,
            "title": "Chemistry Quiz",
            "description": "Online quiz on chemical bonding",
            "subject": "Chemistry",
            "due_date": "2024-01-28",
            "max_marks": 30,
            "is_submitted": False,
            "submitted_date": None,
            "marks_obtained": None,
            "teacher": "Dr. Wilson"
        }
    ]
}

# Mock performance data
MOCK_PERFORMANCE = {
    1: {
        "overall_percentage": 85.5,
        "subjects": [
            {"subject": "Physics", "percentage": 88, "grade": "A"},
            {"subject": "Mathematics", "percentage": 92, "grade": "A+"},
            {"subject": "Chemistry", "percentage": 82, "grade": "B+"},
            {"subject": "Biology", "percentage": 87, "grade": "A"},
            {"subject": "English", "percentage": 85, "grade": "A"},
            {"subject": "History", "percentage": 78, "grade": "B+"}
        ],
        "recent_tests": [
            {"test": "Physics Mid-Term", "marks": 88, "max_marks": 100, "date": "2024-01-10"},
            {"test": "Mathematics Quiz", "marks": 18, "max_marks": 20, "date": "2024-01-08"},
            {"test": "Chemistry Lab", "marks": 25, "max_marks": 30, "date": "2024-01-05"}
        ]
    }
}

# Mock announcements data
MOCK_ANNOUNCEMENTS = [
    {
        "id": 1,
        "title": "Annual Sports Day",
        "content": "Annual sports day will be held on February 15th, 2024. All students are encouraged to participate.",
        "priority": "High",
        "date": "2024-01-15",
        "author": "Principal"
    },
    {
        "id": 2,
        "title": "Parent-Teacher Meeting",
        "content": "Parent-teacher meeting scheduled for January 30th, 2024. Please book your slots online.",
        "priority": "Medium",
        "date": "2024-01-14",
        "author": "Admin"
    },
    {
        "id": 3,
        "title": "Library Week",
        "content": "Library week celebration from January 22nd to 26th. Special activities and book fair.",
        "priority": "Low",
        "date": "2024-01-13",
        "author": "Librarian"
    }
]

# Mock study materials data
MOCK_STUDY_MATERIALS = [
    {
        "id": 1,
        "title": "Physics Formula Sheet",
        "subject": "Physics",
        "class": "10A",
        "type": "PDF",
        "upload_date": "2024-01-10",
        "teacher": "Dr. Smith",
        "description": "Complete formula sheet for all physics chapters"
    },
    {
        "id": 2,
        "title": "Mathematics Practice Problems",
        "subject": "Mathematics",
        "class": "10A",
        "type": "PDF",
        "upload_date": "2024-01-08",
        "teacher": "Mr. Brown",
        "description": "Practice problems for algebra and geometry"
    },
    {
        "id": 3,
        "title": "Chemistry Lab Manual",
        "subject": "Chemistry",
        "class": "10A",
        "type": "PDF",
        "upload_date": "2024-01-05",
        "teacher": "Dr. Wilson",
        "description": "Complete lab manual with safety guidelines"
    }
]

# Mock departments data
MOCK_DEPARTMENTS = [
    {"id": 1, "name": "Physics", "hod": "Prof. Johnson", "teachers": 8, "students": 120},
    {"id": 2, "name": "Chemistry", "hod": "Dr. Williams", "teachers": 6, "students": 95},
    {"id": 3, "name": "Mathematics", "hod": "Prof. Davis", "teachers": 7, "students": 150},
    {"id": 4, "name": "Biology", "hod": "Dr. Anderson", "teachers": 5, "students": 80},
    {"id": 5, "name": "Computer Science", "hod": "Prof. Wilson", "teachers": 4, "students": 60}
]

# Mock classes data
MOCK_CLASSES = [
    {"id": 1, "name": "10A", "strength": 35, "class_teacher": "Dr. Smith"},
    {"id": 2, "name": "10B", "strength": 32, "class_teacher": "Mr. Brown"},
    {"id": 3, "name": "11A", "strength": 30, "class_teacher": "Dr. Wilson"},
    {"id": 4, "name": "11B", "strength": 28, "class_teacher": "Ms. Davis"},
    {"id": 5, "name": "12A", "strength": 25, "class_teacher": "Prof. Johnson"}
]

# Mock functions for student panel
def get_student_info(user_id: int):
    """Get student information."""
    return MOCK_STUDENTS.get(user_id)

def get_timetable(user_id: int):
    """Get student timetable."""
    return MOCK_TIMETABLE.get(user_id, [])

def get_attendance(user_id: int):
    """Get student attendance."""
    return MOCK_ATTENDANCE.get(user_id, [])

def get_assignments(user_id: int):
    """Get student assignments."""
    return MOCK_ASSIGNMENTS.get(user_id, [])

def submit_assignment(user_id: int, assignment_id: int, submission_text: str, file_path: str = None):
    """Submit assignment (mock function)."""
    # In a real app, this would save to database
    st.success("Assignment submitted successfully!")
    return True

def get_performance(user_id: int):
    """Get student performance."""
    return MOCK_PERFORMANCE.get(user_id, {})

def get_announcements(user_id: int):
    """Get announcements."""
    return MOCK_ANNOUNCEMENTS

def get_study_materials(user_id: int):
    """Get study materials."""
    return MOCK_STUDY_MATERIALS

def update_password(user_id: int, old_password: str, new_password: str):
    """Update password (mock function)."""
    st.success("Password updated successfully!")
    return True

# Mock functions for teacher panel
def get_teacher_info(user_id: int):
    """Get teacher information."""
    return MOCK_TEACHERS.get(user_id)

def get_teacher_classes(user_id: int):
    """Get classes taught by teacher."""
    return MOCK_CLASSES

def get_teacher_students(user_id: int):
    """Get students in teacher's classes."""
    return [MOCK_STUDENTS[1]]  # Return sample student

def create_assignment(user_id: int, title: str, description: str, due_date: str, subject: str, class_name: str):
    """Create assignment (mock function)."""
    st.success("Assignment created successfully!")
    return True

def mark_attendance(user_id: int, class_name: str, date: str, attendance_data: dict):
    """Mark attendance (mock function)."""
    st.success("Attendance marked successfully!")
    return True

def enter_marks(user_id: int, class_name: str, subject: str, exam_type: str, marks_data: dict):
    """Enter marks (mock function)."""
    st.success("Marks entered successfully!")
    return True

def get_teacher_assignments(user_id: int):
    """Get assignments created by teacher."""
    return MOCK_ASSIGNMENTS.get(1, [])  # Return sample assignments

def get_teacher_announcements(user_id: int):
    """Get announcements for teacher."""
    return MOCK_ANNOUNCEMENTS

def create_announcement(user_id: int, title: str, content: str, priority: str):
    """Create announcement (mock function)."""
    st.success("Announcement created successfully!")
    return True

def upload_study_material(user_id: int, title: str, subject: str, class_name: str, description: str, file):
    """Upload study material (mock function)."""
    st.success("Study material uploaded successfully!")
    return True

def get_teacher_feedback(user_id: int):
    """Get feedback for teacher."""
    return [
        {"student": "John Doe", "feedback": "Great teaching method!", "date": "2024-01-10"},
        {"student": "Jane Smith", "feedback": "Very helpful explanations", "date": "2024-01-08"}
    ]

# Mock functions for HOD panel
def get_hod_info(user_id: int):
    """Get HOD information."""
    return MOCK_HODS.get(user_id)

def get_department_info(user_id: int):
    """Get department information."""
    return MOCK_DEPARTMENTS[0]  # Return first department as sample

def get_department_teachers(user_id: int):
    """Get teachers in HOD's department."""
    return [MOCK_TEACHERS[2]]  # Return sample teacher

def get_department_students(user_id: int):
    """Get students in HOD's department."""
    return [MOCK_STUDENTS[1]]  # Return sample student

def get_department_performance(user_id: int):
    """Get department performance."""
    return {
        "average_percentage": 82.5,
        "top_performer": "John Doe",
        "improvement_needed": ["Chemistry", "Biology"]
    }

def approve_leave(user_id: int, teacher_id: int, leave_data: dict):
    """Approve leave (mock function)."""
    st.success("Leave approved successfully!")
    return True

def generate_department_report(user_id: int):
    """Generate department report (mock function)."""
    st.success("Department report generated successfully!")
    return True

# Mock functions for admin panel
def get_admin_info(user_id: int):
    """Get admin information."""
    return MOCK_ADMINS.get(user_id)

def get_system_stats():
    """Get system statistics."""
    return {
        "total_students": 450,
        "total_teachers": 35,
        "total_departments": 5,
        "total_classes": 15,
        "active_users": 485
    }

def get_all_users():
    """Get all users."""
    return [
        {"id": 1, "name": "John Doe", "role": "Student", "department": "Physics", "status": "Active"},
        {"id": 2, "name": "Dr. Sarah Smith", "role": "Teacher", "department": "Physics", "status": "Active"},
        {"id": 3, "name": "Prof. Michael Johnson", "role": "HOD", "department": "Physics", "status": "Active"},
        {"id": 4, "name": "Admin User", "role": "Admin", "department": "-", "status": "Active"}
    ]

def create_user(user_data: dict):
    """Create user (mock function)."""
    st.success("User created successfully!")
    return True

def get_system_logs():
    """Get system logs."""
    return [
        {"timestamp": "2024-01-15 10:30:00", "user": "John Doe", "action": "Login", "status": "Success"},
        {"timestamp": "2024-01-15 10:25:00", "user": "Dr. Smith", "action": "Upload Assignment", "status": "Success"},
        {"timestamp": "2024-01-15 10:20:00", "user": "Admin", "action": "Create User", "status": "Success"}
    ]

def get_system_reports():
    """Get system reports."""
    return [
        {"name": "Monthly Attendance Report", "generated": "2024-01-15", "status": "Ready"},
        {"name": "Academic Performance Report", "generated": "2024-01-14", "status": "Ready"},
        {"name": "Teacher Evaluation Report", "generated": "2024-01-13", "status": "Processing"}
    ]

def backup_system():
    """Backup system (mock function)."""
    st.success("System backup completed successfully!")
    return True

def restore_system(backup_file):
    """Restore system (mock function)."""
    st.success("System restored successfully!")
    return True 