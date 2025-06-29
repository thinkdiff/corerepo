import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# Import mock data functions
from mock_data import get_teacher_info, get_teacher_classes, get_teacher_students, create_assignment, mark_attendance, enter_marks, get_teacher_assignments, get_teacher_announcements, create_announcement, upload_study_material, get_teacher_feedback

def show_dashboard(user_id: int):
    # Get teacher information from mock data
    teacher = get_teacher_info(user_id)
    if not teacher:
        st.error("Unable to load teacher information")
        return
    
    st.title(f"Welcome, {teacher['first_name']} {teacher['last_name']}!")
    st.write(f"Department: {teacher['department']} | Employee ID: {teacher['employee_id']}")
    
    # Quick summary metrics
    col1, col2, col3 = st.columns(3)
    
    # Get mock data for metrics
    classes = get_teacher_classes(user_id)
    students = get_teacher_students(user_id)
    assignments = get_teacher_assignments(user_id)
    
    with col1:
        st.metric("Total Students", str(len(students)), None)
    with col2:
        st.metric("Classes Today", str(len(classes)), None)
    with col3:
        st.metric("Active Assignments", str(len(assignments)), None)
    
    # Today's Schedule
    st.subheader("Today's Schedule")
    schedule_data = [
        {"Time": "08:00 AM", "Class": "10A", "Subject": "Physics", "Topic": "Mechanics"},
        {"Time": "10:00 AM", "Class": "11B", "Subject": "Physics", "Topic": "Thermodynamics"},
        {"Time": "02:00 PM", "Class": "12A", "Subject": "Physics", "Topic": "Electromagnetism"}
    ]
    
    if schedule_data:
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df, use_container_width=True)
    else:
        st.info("No classes scheduled for today")

def manage_attendance(user_id: int):
    st.title("Attendance Management")
    
    # Get teacher's classes from mock data
    classes = get_teacher_classes(user_id)
    
    if not classes:
        st.warning("No classes assigned")
        return
    
    # Class Selection
    col1, col2 = st.columns(2)
    with col1:
        class_options = {c['name']: c['id'] for c in classes}
        selected_class = st.selectbox("Select Class", list(class_options.keys()))
        class_id = class_options[selected_class]
    
    with col2:
        selected_date = st.date_input("Date", datetime.now())
    
    # Get students in selected class (mock data)
    students = get_teacher_students(user_id)
    
    if not students:
        st.info("No students found in this class")
        return
    
    # Create attendance form
    with st.form("attendance_form"):
        for student in students:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"Roll No: {student['roll_number']}")
            with col2:
                st.write(f"{student['first_name']} {student['last_name']}")
            with col3:
                status = st.selectbox(
                    "",
                    ["Present", "Absent"],
                    index=0,
                    key=f"attendance_{student['id']}"
                )
        
        if st.form_submit_button("Save Attendance"):
            # Use mock function to mark attendance
            attendance_data = {}
            for student in students:
                attendance_data[student['id']] = st.session_state[f"attendance_{student['id']}"]
            
            if mark_attendance(user_id, selected_class, str(selected_date), attendance_data):
                st.success("Attendance marked successfully!")
            else:
                st.error("Error saving attendance")

def manage_assignments(user_id: int):
    st.title("Assignment Management")
    
    # Get teacher's classes from mock data
    classes = get_teacher_classes(user_id)
    
    if not classes:
        st.warning("No classes assigned")
        return
    
    # Create New Assignment
    with st.expander("Create New Assignment"):
        with st.form("new_assignment_form"):
            class_options = {c['name']: c['id'] for c in classes}
            selected_class = st.selectbox("Class", list(class_options.keys()))
            title = st.text_input("Title")
            description = st.text_area("Description")
            due_date = st.date_input("Due Date", min_value=datetime.now().date())
            subject = st.text_input("Subject")
            file = st.file_uploader("Upload Assignment File", type=['pdf', 'doc', 'docx'])
            
            if st.form_submit_button("Create Assignment"):
                if not all([title, description, due_date, subject]):
                    st.error("Please fill in all required fields")
                else:
                    # Use mock function to create assignment
                    if create_assignment(user_id, title, description, str(due_date), subject, selected_class):
                        st.success("Assignment created successfully!")
                    else:
                        st.error("Error creating assignment")
    
    # Review Submissions
    st.subheader("Active Assignments")
    
    assignments = get_teacher_assignments(user_id)
    
    for assignment in assignments:
        with st.expander(f"{assignment['subject']} - {assignment['title']} (Due: {assignment['due_date']})"):
            st.write(f"Description: {assignment['description']}")
            st.write(f"Max Marks: {assignment['max_marks']}")
            
            if assignment['is_submitted']:
                st.write("✅ Submitted")
                if assignment['marks_obtained'] is not None:
                    st.write(f"Marks: {assignment['marks_obtained']}/{assignment['max_marks']}")
            else:
                st.write("⏳ Pending")

def manage_marks(user_id: int):
    st.title("Marks Entry")
    
    # Get teacher's classes from mock data
    classes = get_teacher_classes(user_id)
    
    if not classes:
        st.warning("No classes assigned")
        return
    
    # Selection controls
    col1, col2, col3 = st.columns(3)
    with col1:
        class_options = {c['name']: c['id'] for c in classes}
        selected_class = st.selectbox("Select Class", list(class_options.keys()))
        class_id = class_options[selected_class]
    
    with col2:
        subjects = ["Physics", "Mathematics", "Chemistry", "Biology", "English"]
        selected_subject = st.selectbox("Select Subject", subjects)
    
    with col3:
        exam_types = ["Unit Test 1", "Mid Term", "Unit Test 2", "Final Term"]
        selected_exam = st.selectbox("Select Exam", exam_types)
    
    # Get students in selected class (mock data)
    students = get_teacher_students(user_id)
    
    if not students:
        st.info("No students found in this class")
        return
    
    # Create marks entry form
    with st.form("marks_entry_form"):
        st.subheader("Enter Marks")
        marks_data = {}
        
        for student in students:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"Roll No: {student['roll_number']}")
            with col2:
                st.write(f"{student['first_name']} {student['last_name']}")
            with col3:
                marks_data[student['id']] = st.number_input(
                    "",
                    min_value=0,
                    max_value=100,
                    value=0,
                    key=f"marks_{student['id']}"
                )
        
        if st.form_submit_button("Save Marks"):
            # Use mock function to enter marks
            if enter_marks(user_id, selected_class, selected_subject, selected_exam, marks_data):
                st.success("Marks saved successfully!")
            else:
                st.error("Error saving marks")
    
    # Show class statistics
    st.subheader("Class Statistics")
    marks_list = [85, 92, 78, 88, 90]  # Mock marks data
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Class Average", f"{sum(marks_list)/len(marks_list):.2f}")
    with col2:
        st.metric("Highest Mark", str(max(marks_list)))
    with col3:
        st.metric("Lowest Mark", str(min(marks_list)))

def manage_announcements(user_id: int):
    st.title("Manage Announcements")
    
    # Get teacher's classes from mock data
    classes = get_teacher_classes(user_id)
    
    if not classes:
        st.warning("No classes assigned")
        return
    
    # Create new announcement
    with st.expander("Create New Announcement", expanded=True):
        with st.form("announcement_form"):
            # Add "All Classes" option
            class_options = {"All Classes": None}
            class_options.update({c['name']: c['id'] for c in classes})
            
            selected_class = st.selectbox("Target Class", list(class_options.keys()))
            title = st.text_input("Announcement Title")
            content = st.text_area("Announcement Content")
            priority = st.selectbox("Priority", ["Normal", "Important", "Urgent"])
            
            if st.form_submit_button("Post Announcement"):
                if not all([title, content]):
                    st.error("Please fill in all required fields")
                else:
                    # Use mock function to create announcement
                    if create_announcement(user_id, title, content, priority):
                        st.success("Announcement posted successfully!")
                    else:
                        st.error("Error posting announcement")
    
    # View existing announcements
    st.subheader("Your Announcements")
    
    announcements = get_teacher_announcements(user_id)
    
    if not announcements:
        st.info("No announcements found")
        return
    
    for announcement in announcements:
        with st.expander(
            f"📢 {announcement['title']} - {announcement['date']}"
        ):
            st.write(f"**Priority:** {announcement['priority'].title()}")
            st.write("**Content:**")
            st.write(announcement['content'])

def manage_resources(user_id: int):
    st.title("Study Materials Management")
    
    # Get teacher's classes from mock data
    classes = get_teacher_classes(user_id)
    
    if not classes:
        st.warning("No classes assigned")
        return
    
    # Upload New Material
    with st.expander("Upload New Material", expanded=True):
        with st.form("upload_material_form"):
            selected_class = st.selectbox("Class", [c['name'] for c in classes])
            subjects = ["Physics", "Mathematics", "Chemistry", "Biology", "English"]
            selected_subject = st.selectbox("Subject", subjects)
            
            title = st.text_input("Title")
            description = st.text_area("Description")
            resource_type = st.selectbox(
                "Resource Type",
                ["PDF", "Video", "Link"]
            )
            
            if resource_type == "PDF":
                file = st.file_uploader("Upload Document", type=['pdf', 'doc', 'docx'])
                external_link = None
            else:
                file = None
                external_link = st.text_input("Resource Link")
            
            if st.form_submit_button("Upload Material"):
                if not all([title, description]):
                    st.error("Please fill in all required fields")
                elif resource_type == "PDF" and not file:
                    st.error("Please upload a document")
                elif resource_type in ["Video", "Link"] and not external_link:
                    st.error("Please provide a resource link")
                else:
                    # Use mock function to upload study material
                    if upload_study_material(user_id, title, selected_subject, selected_class, description, file):
                        st.success("Material uploaded successfully!")
                    else:
                        st.error("Error uploading material")
    
    # Manage Existing Materials
    st.subheader("Uploaded Materials")
    
    # Mock materials data
    materials = [
        {
            "title": "Physics Formula Sheet",
            "subject": "Physics",
            "class": "10A",
            "type": "PDF",
            "upload_date": "2024-01-10",
            "status": "Active"
        },
        {
            "title": "Mathematics Practice Problems",
            "subject": "Mathematics",
            "class": "10A",
            "type": "PDF",
            "upload_date": "2024-01-08",
            "status": "Active"
        }
    ]
    
    for material in materials:
        with st.expander(
            f"{material['title']} ({material['class']} - {material['subject']}) - {material['upload_date']}"
        ):
            st.write(f"**Type:** {material['type']}")
            st.write(f"**Status:** {material['status']}")
            
            if material['type'] == 'PDF':
                st.download_button(
                    "📥 Download",
                    "dummy_pdf_content",
                    file_name=f"{material['title']}.pdf"
                )

def view_feedback(user_id: int):
    st.title("Student Feedback")
    
    # Get feedback for teacher from mock data
    feedback_data = get_teacher_feedback(user_id)
    
    if not feedback_data:
        st.info("No feedback received yet")
        return
    
    # Display feedback
    for feedback in feedback_data:
        with st.expander(
            f"Feedback from {feedback['student']} - {feedback['date']}"
        ):
            st.write(f"**Feedback:** {feedback['feedback']}")
            
            # Response form
            with st.form(f"response_form_{feedback['student']}"):
                response = st.text_area(
                    "Reply",
                    key=f"response_{feedback['student']}"
                )
                
                if st.form_submit_button("Send Response"):
                    if not response:
                        st.error("Please enter a response")
                    else:
                        st.success("Response sent successfully!")

def show_profile(user_id: int):
    st.title("Teacher Profile")
    
    # Get teacher information from mock data
    teacher = get_teacher_info(user_id)
    
    if not teacher:
        st.error("Unable to load profile information")
        return
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            teacher.get('profile_image_url', "https://via.placeholder.com/150"),
            caption=f"{teacher['first_name']} {teacher['last_name']}"
        )
    with col2:
        st.write(f"**Name:** {teacher['first_name']} {teacher['last_name']}")
        st.write(f"**Department:** {teacher['department']}")
        st.write(f"**Employee ID:** {teacher['employee_id']}")
        st.write(f"**Designation:** {teacher['designation']}")
        st.write(f"**Qualification:** {teacher['qualification']}")
        if teacher.get('contact_number'):
            st.write(f"**Phone:** {teacher['contact_number']}")
        if teacher.get('joining_date'):
            st.write(f"**Joining Date:** {teacher['joining_date']}")
    
    # Update Profile Form
    with st.expander("Update Profile"):
        with st.form("profile_update_form"):
            phone = st.text_input("Phone Number", value=teacher.get('contact_number', ""))
            bio = st.text_area("Bio", value="")
            profile_image = st.file_uploader(
                "Update Profile Picture",
                type=['jpg', 'jpeg', 'png']
            )
            
            if st.form_submit_button("Save Changes"):
                st.success("Profile updated successfully!")
    
    # Change Password Form
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
                    st.success("Password updated successfully!")

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

    # Get teacher info for personalization
    teacher = get_teacher_info(user_id)
    if not teacher:
        st.error("Unable to load teacher information. Please contact administrator.")
        return

    # Sidebar navigation
    st.sidebar.title("Teacher Portal")
    st.sidebar.image(
        teacher.get('profile_image_url', "https://via.placeholder.com/150"),
        caption=f"{teacher['first_name']} {teacher['last_name']}"
    )
    menu = st.sidebar.radio("", [
        "📊 Dashboard",
        "📝 Attendance",
        "📚 Assignments",
        "🎯 Marks Entry",
        "📢 Announcements",
        "📖 Resources",
        "💬 Feedback",
        "👤 Profile"
    ])

    # Route to appropriate function based on menu selection
    if menu == "📊 Dashboard":
        show_dashboard(user_id)
    elif menu == "📝 Attendance":
        manage_attendance(user_id)
    elif menu == "📚 Assignments":
        manage_assignments(user_id)
    elif menu == "🎯 Marks Entry":
        manage_marks(user_id)
    elif menu == "📢 Announcements":
        manage_announcements(user_id)
    elif menu == "📖 Resources":
        manage_resources(user_id)
    elif menu == "💬 Feedback":
        view_feedback(user_id)
    elif menu == "👤 Profile":
        show_profile(user_id)