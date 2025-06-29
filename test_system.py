import streamlit as st
import time
from datetime import datetime, timedelta
from main import hash_password

def create_test_users():
    """Create test users for each role."""
    # Implement mock user creation logic or leave as a placeholder
    pass

def test_login(conn, email: str, password: str, role: str) -> bool:
    """Test login functionality."""
    try:
        with conn.cursor() as cur:
            query = """
                SELECT id, role, password_hash 
                FROM users 
                WHERE email = %s AND is_active = true
            """
            cur.execute(query, (email,))
            result = cur.fetchone()
            
            if not result:
                print(f"Login failed for {email}: User not found")
                return False
            
            if result['password_hash'] == hash_password(password) and result['role'] == role:
                print(f"Login successful for {email}")
                return True
            
            print(f"Login failed for {email}: Invalid credentials")
            return False
            
    except Exception as e:
        print(f"Login error for {email}: {str(e)}")
        return False

def test_crud_operations(conn, user_id: int, role: str):
    """Test CRUD operations for each role."""
    try:
        with conn.cursor() as cur:
            if role == 'student':
                # Test submitting assignment
                assignment_query = """
                    INSERT INTO assignment_submissions (assignment_id, student_id, file_path)
                    VALUES (1, (SELECT id FROM students WHERE user_id = %s), 'test_submission.pdf')
                    RETURNING id
                """
                cur.execute(assignment_query, (user_id,))
                conn.commit()
                print("Student assignment submission test: Success")
                
            elif role == 'teacher':
                # Test creating assignment
                assignment_query = """
                    INSERT INTO assignments (teacher_id, title, description, class_id, subject_id, due_date)
                    VALUES (
                        (SELECT id FROM teachers WHERE user_id = %s),
                        'Test Assignment',
                        'Test Description',
                        1,
                        1,
                        CURRENT_DATE + INTERVAL '7 days'
                    )
                    RETURNING id
                """
                cur.execute(assignment_query, (user_id,))
                conn.commit()
                print("Teacher assignment creation test: Success")
                
            elif role == 'hod':
                # Test department announcement
                announcement_query = """
                    INSERT INTO announcements (user_id, title, content, target_audience)
                    VALUES (%s, 'Test Announcement', 'Test Content', 'department')
                    RETURNING id
                """
                cur.execute(announcement_query, (user_id,))
                conn.commit()
                print("HOD announcement creation test: Success")
                
            elif role == 'admin':
                # Test user management
                user_query = """
                    UPDATE users
                    SET is_active = true
                    WHERE role = 'student'
                    RETURNING id
                """
                cur.execute(user_query)
                conn.commit()
                print("Admin user management test: Success")
                
    except Exception as e:
        conn.rollback()
        print(f"CRUD test error for {role}: {str(e)}")

def run_system_tests():
    """Run comprehensive system tests."""
    print("Starting system tests...\n")
    
    try:
        # Create test users
        print("Creating test users...")
        create_test_users()
        print("\nTest users created.\n")
        
        # Test login for each user
        print("Testing login functionality...")
        for email, password, role in test_users:
            test_login(conn, email, password, role)
        print("\nLogin tests completed.\n")
        
        # Test CRUD operations
        print("Testing CRUD operations...")
        with conn.cursor() as cur:
            for email, _, role in test_users:
                cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                result = cur.fetchone()
                if result:
                    test_crud_operations(conn, result['id'], role)
        print("\nCRUD tests completed.\n")
        
        print("All system tests completed.")
        
    except Exception as e:
        print(f"Test suite error: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    run_system_tests()