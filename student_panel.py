import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# Import mock data functions
from mock_data import get_student_info, get_timetable, get_attendance, get_assignments, submit_assignment, get_performance, get_announcements, get_study_materials, update_password

def show_dashboard(user_id: int):
    student = get_student_info(user_id)
    if not student:
        st.error("Student information not found")
        return
    
    st.title(f"Welcome, {student['first_name']} {student['last_name']}!")
    st.write(f"Class: {student['class']} | Roll Number: {student['roll_number']}")

    
    # Quick summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Attendance", "85%", "+2%")
    with col2:
        st.metric("Average Score", "87.5%", "+3.2%")
    with col3:
        st.metric("Pending Assignments", "3", "-2")
    
    # Recent announcements
    st.subheader("Recent Announcements")
    with st.container():
        st.info("📌 Parent-Teacher Meeting scheduled for next Friday")
        st.warning("⚠️ Physics assignment deadline extended to 15th March")
        st.success("✅ Mid-term examination results declared")

def show_timetable(user_id: int):
    st.title("Class Timetable")
    
    # Get student's class timetable from mock data
    result = get_timetable(user_id)
    
    if not result:
        st.warning("No timetable available")
        return
    
    # Process timetable data for display
    timetable_data = {"Time": [], "Monday": [], "Tuesday": [], 
                     "Wednesday": [], "Thursday": [], "Friday": []}
    
    # Group by time slots
    time_slots = {}
    for row in result:
        time_key = row['time']
        day = row['day']
        subject = row['subject']
        
        if time_key not in time_slots:
            time_slots[time_key] = {'Monday': '-', 'Tuesday': '-', 'Wednesday': '-', 'Thursday': '-', 'Friday': '-'}
        
        time_slots[time_key][day] = subject
    
    # Convert to display format
    for time_slot, subjects in time_slots.items():
        timetable_data["Time"].append(time_slot)
        timetable_data["Monday"].append(subjects['Monday'])
        timetable_data["Tuesday"].append(subjects['Tuesday'])
        timetable_data["Wednesday"].append(subjects['Wednesday'])
        timetable_data["Thursday"].append(subjects['Thursday'])
        timetable_data["Friday"].append(subjects['Friday'])
    
    st.dataframe(pd.DataFrame(timetable_data), use_container_width=True)

def show_attendance(user_id: int):
    st.title("Attendance Records")
    
    # Get attendance records from mock data
    result = get_attendance(user_id)
    
    if not result:
        st.warning("No attendance records found")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(result)
    st.dataframe(df, use_container_width=True)
    
    # Show attendance summary
    if not df.empty:
        attendance_summary = df.groupby('subject')['status'].value_counts().unstack(fill_value=0)
        st.subheader("Attendance Summary by Subject")
        st.dataframe(attendance_summary, use_container_width=True)

def manage_assignments(user_id: int):
    st.title("Assignments")
    
    # Get student's assignments from mock data
    assignments = get_assignments(user_id)
    
    if not assignments:
        st.info("No assignments available")
        return
    
    for assignment in assignments:
        with st.expander(f"{assignment['subject']} - {assignment['title']}"):
            st.write(f"Due Date: {assignment['due_date']}")
            st.write(f"Status: {'Submitted' if assignment['is_submitted'] else 'Pending'}")
            st.write(f"Description: {assignment['description']}")
            
            if assignment['is_submitted'] and assignment['marks_obtained'] is not None:
                st.write(f"Marks Obtained: {assignment['marks_obtained']}/{assignment['max_marks']}")
            
            if not assignment['is_submitted']:
                uploaded_file = st.file_uploader(
                    "Submit Assignment",
                    key=f"assignment_{assignment['id']}"
                )
                submission_text = st.text_area(
                    "Comments (optional)",
                    key=f"text_{assignment['id']}"
                )
                
                if st.button("Submit", key=f"submit_{assignment['id']}"):
                    if uploaded_file or submission_text:
                        # Handle file upload and submission using mock data
                        file_path = None
                        if uploaded_file:
                            # Mock file upload handling
                            file_path = f"/uploads/submissions/{assignment['id']}_{uploaded_file.name}"
                        
                        # Use mock function to submit assignment
                        submit_assignment(user_id, assignment['id'], submission_text, file_path)
                        st.success("Assignment submitted successfully!")
                        st.rerun()
                    else:
                        st.error("Please provide either a file or comments")

def show_performance(user_id: int):
    st.title("Academic Performance")
    
    # Get performance data from mock data
    result = get_performance(user_id)
    
    if not result:
        st.warning("No performance records found")
        return
    
    # Display overall performance
    if 'overall_percentage' in result:
        st.metric("Overall Percentage", f"{result['overall_percentage']}%")
    
    # Display subject-wise performance
    if 'subjects' in result:
        st.subheader("Subject-wise Performance")
        subjects_df = pd.DataFrame(result['subjects'])
        st.dataframe(subjects_df, use_container_width=True)
        
        # Create performance chart
        if not subjects_df.empty:
            chart_data = subjects_df.set_index('subject')['percentage']
            st.bar_chart(chart_data)
    
    # Display recent tests
    if 'recent_tests' in result:
        st.subheader("Recent Tests")
        tests_df = pd.DataFrame(result['recent_tests'])
        st.dataframe(tests_df, use_container_width=True)

def show_announcements(user_id: int):
    st.title("Announcements & Notices")
    
    # Get announcements from mock data
    announcements = get_announcements(user_id)
    
    if not announcements:
        st.info("No announcements available")
        return
    
    tab1, tab2 = st.tabs(["Recent", "Archive"])
    
    with tab1:
        recent = [a for a in announcements if a.get('is_active', True)]
        for announcement in recent:
            st.info(f"📌 {announcement['title']}")
            st.write(announcement['content'])
            st.write(f"Posted on: {announcement['date']}")
            st.divider()
    
    with tab2:
        archived = [a for a in announcements if not a.get('is_active', True)]
        for announcement in archived:
            with st.expander(announcement['title']):
                st.write(announcement['content'])
                st.write(f"Posted on: {announcement['date']}")

def show_study_materials(user_id: int):
    st.title("Study Materials")
    
    # Get student's class materials from mock data
    materials = get_study_materials(user_id)
    
    if not materials:
        st.info("No study materials available")
        return
    
    # Group materials by subject
    subjects = {}
    for material in materials:
        subject = material['subject']
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(material)
    
    # Display materials by subject
    for subject, subject_materials in subjects.items():
        with st.expander(subject):
            for material in subject_materials:
                st.subheader(material['title'])
                st.write(material['description'])
                st.write(f"Uploaded by: {material['teacher']}")
                st.write(f"Date: {material['upload_date']}")
                
                if material['type'] == 'PDF':
                    st.download_button(
                        "📚 Download Material",
                        "dummy_pdf_content",
                        file_name=f"{material['title']}.pdf"
                    )

def show_feedback():
    st.title("Feedback & Queries")
    
    with st.form("feedback_form"):
        subject = st.selectbox("Subject", ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"])
        feedback_type = st.radio("Type", ["Query", "Feedback", "Complaint"])
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            st.success("Feedback submitted successfully!")
    
    st.subheader("Previous Responses")
    with st.expander("Response 1"):
        st.write("Query: When will the next assignment be posted?")
        st.write("Response: The assignment will be posted next week.")

def show_profile(user_id: int, email: str):
    st.title("Student Profile")
    
    # Get detailed student information from mock data
    student = get_student_info(user_id)
    
    if not student:
        st.error("Unable to load profile information")
        return
    
    # Add email to student data
    if 'email' not in student:
        student['email'] = email
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            student.get('profile_image_url', "https://via.placeholder.com/150"),
            caption=f"{student['first_name']} {student['last_name']}"
        )
    with col2:
        st.write(f"**Name:** {student['first_name']} {student['last_name']}")
        st.write(f"**Class:** {student['class']}")
        st.write(f"**Roll Number:** {student['roll_number']}")
        st.write(f"**Email:** {student['email']}")
        if student.get('date_of_birth'):
            st.write(f"**Date of Birth:** {student['date_of_birth']}")
        if student.get('contact_number'):
            st.write(f"**Phone:** {student['contact_number']}")
        if student.get('address'):
            st.write(f"**Address:** {student['address']}")
    
    with st.expander("Change Password"):
        with st.form("password_change_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Update Password"):
                if not all([current_password, new_password, confirm_password]):
                    st.error("Please fill in all password fields")
                elif new_password != confirm_password:
                    st.error("New passwords do not match")
                else:
                    # Use mock function to update password
                    if update_password(user_id, current_password, new_password):
                        st.success("Password updated successfully!")
                    else:
                        st.error("Current password is incorrect")

def show_panel(user_id: int, email: str):
    # Custom CSS
    st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button { width: 100%; }
    .css-1d391kg { padding-top: 1rem; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Get student info for personalization
    student = get_student_info(user_id)
    if not student:
        st.error("Unable to load student information. Please contact administrator.")
        return
    
    # Sidebar navigation
    st.sidebar.title("Student Portal")
    st.sidebar.image(
        student.get('profile_image_url', "https://via.placeholder.com/150"),
        caption=f"{student['first_name']} {student['last_name']}"
    )
    menu = st.sidebar.radio("", [
        "📊 Dashboard",
        "📅 Timetable",
        "📝 Attendance",
        "📚 Assignments",
        "🎯 Performance",
        "📢 Announcements",
        "📖 Study Materials",
        "💬 Feedback",
        "👤 Profile"
    ])

    # Route to appropriate function based on menu selection
    if menu == "📊 Dashboard":
        show_dashboard(user_id)
    elif menu == "📅 Timetable":
        show_timetable(user_id)
    elif menu == "📝 Attendance":
        show_attendance(user_id)
    elif menu == "📚 Assignments":
        manage_assignments(user_id)
    elif menu == "🎯 Performance":
        show_performance(user_id)
    elif menu == "📢 Announcements":
        show_announcements(user_id)
    elif menu == "📖 Study Materials":
        show_study_materials(user_id)
    elif menu == "💬 Feedback":
        show_feedback()
    elif menu == "👤 Profile":
        show_profile(user_id, email)