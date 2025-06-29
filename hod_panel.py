import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# Import mock data functions
from mock_data import get_hod_info, get_department_info, get_department_teachers, get_department_students, get_department_performance, approve_leave, generate_department_report

def show_dashboard(user_id: int):
    # Get HOD information from mock data
    hod = get_hod_info(user_id)
    if not hod:
        st.error("Unable to load HOD information")
        return
    
    st.title(f"Welcome, {hod['first_name']} {hod['last_name']}!")
    st.write(f"Head of Department - {hod['department']}")
    
    # Department Overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Teachers", "12", "+1")
    with col2:
        st.metric("Total Classes", "8", "")
    with col3:
        st.metric("Total Students", "320", "+15")
    
    # Department Performance
    st.subheader("Department Performance")
    performance_data = {
        "Class": ["XI-A", "XI-B", "XII-A", "XII-B"],
        "Average Score": [85, 82, 88, 86],
        "Attendance %": [92, 90, 94, 91]
    }
    st.dataframe(pd.DataFrame(performance_data), use_container_width=True)

def manage_teachers(user_id: int):
    st.title("Teacher Management")
    
    # Get department teachers from mock data
    teachers = get_department_teachers(user_id)
    
    if not teachers:
        st.info("No teachers found in department")
        return
    
    # Teacher Directory
    teachers_data = []
    for teacher in teachers:
        teachers_data.append({
            "ID": teacher['employee_id'],
            "Name": f"{teacher['first_name']} {teacher['last_name']}",
            "Specialization": teacher['qualification'],
            "Classes": "XII-A, XI-B"  # Mock data
        })
    
    st.dataframe(pd.DataFrame(teachers_data), use_container_width=True)
    
    # Assign Classes
    with st.expander("Assign Classes"):
        teacher_names = [f"{t['first_name']} {t['last_name']}" for t in teachers]
        st.selectbox("Select Teacher", teacher_names)
        st.multiselect("Assign Classes", ["XI-A", "XI-B", "XII-A", "XII-B"])
        if st.button("Update Assignments"):
            st.success("Class assignments updated successfully!")

def manage_curriculum(user_id: int):
    st.title("Curriculum Planning")
    
    # Course Structure
    with st.expander("Course Structure"):
        st.selectbox("Select Class", ["XI", "XII"])
        topics = [
            "Mechanics",
            "Thermodynamics",
            "Electrostatics",
            "Wave Optics"
        ]
        for topic in topics:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text_input("Topic", topic, key=f"topic_{topic}")
            with col2:
                st.number_input("Hours", value=10, key=f"hours_{topic}")
    
    # Academic Calendar
    st.subheader("Academic Calendar")
    calendar_data = {
        "Month": ["March", "April", "May"],
        "Topics": ["Wave Optics", "Quantum Physics", "Revision"],
        "Assessments": ["Unit Test", "Mid Term", "Final Term"]
    }
    st.dataframe(pd.DataFrame(calendar_data), use_container_width=True)

def view_performance(user_id: int):
    st.title("Department Performance")
    
    # Get department performance from mock data
    performance = get_department_performance(user_id)
    
    # Class-wise Performance
    st.subheader("Class Performance Analysis")
    performance_data = {
        "Class": ["XI-A", "XI-B", "XII-A", "XII-B"],
        "Physics": [85, 82, 88, 86],
        "Attendance": [92, 90, 94, 91],
        "Assignments": [88, 85, 90, 87]
    }
    df = pd.DataFrame(performance_data)
    st.line_chart(df.set_index("Class"))
    
    # Department Statistics
    if performance:
        st.subheader("Department Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Percentage", f"{performance['average_percentage']}%")
        with col2:
            st.metric("Top Performer", performance['top_performer'])
        with col3:
            st.metric("Improvement Needed", ", ".join(performance['improvement_needed']))
    
    # Teacher Performance
    st.subheader("Teacher Performance")
    teacher_metrics = {
        "Teacher": ["Dr. Smith", "Mrs. Williams", "Mr. Davis"],
        "Classes Taken": [45, 42, 44],
        "Avg Student Score": [86, 84, 85],
        "Student Feedback": [4.5, 4.3, 4.4]
    }
    st.dataframe(pd.DataFrame(teacher_metrics), use_container_width=True)

def manage_resources(user_id: int):
    st.title("Resource Management")
    
    # Lab Equipment
    with st.expander("Laboratory Equipment"):
        equipment_data = {
            "Equipment": ["Oscilloscope", "Spectrometer", "Wave Apparatus"],
            "Quantity": [5, 8, 10],
            "Status": ["Working", "2 Under Repair", "All Working"]
        }
        st.dataframe(pd.DataFrame(equipment_data), use_container_width=True)
        
        st.subheader("Request Equipment")
        st.text_input("Equipment Name")
        st.number_input("Quantity Required", min_value=1)
        st.text_area("Justification")
        if st.button("Submit Request"):
            st.success("Equipment request submitted!")

def manage_reports(user_id: int):
    st.title("Department Reports")
    
    report_types = [
        "Monthly Performance Report",
        "Teacher Attendance Report",
        "Student Progress Report",
        "Lab Usage Report"
    ]
    
    for report in report_types:
        with st.expander(report):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("From Date", key=f"from_{report}")
            with col2:
                st.date_input("To Date", key=f"to_{report}")
            if st.button("Generate Report", key=f"gen_{report}"):
                # Use mock function to generate report
                if generate_department_report(user_id):
                    st.success("Report generated successfully!")
                    st.download_button("Download Report", "dummy_data", f"{report}.pdf", key=f"download_{report}")

def manage_meetings(user_id: int):
    st.title("Department Meetings")
    
    # Schedule Meeting
    with st.form("schedule_meeting"):
        st.text_input("Meeting Title")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Date")
        with col2:
            st.time_input("Time")
        st.multiselect("Participants", ["All Teachers", "Dr. Smith", "Mrs. Williams", "Mr. Davis"])
        st.text_area("Agenda")
        if st.form_submit_button("Schedule Meeting"):
            st.success("Meeting scheduled successfully!")
    
    # Upcoming Meetings
    st.subheader("Upcoming Meetings")
    meetings = [
        {"title": "Monthly Review", "date": "2024-03-15", "time": "10:00 AM"},
        {"title": "Curriculum Planning", "date": "2024-03-20", "time": "2:00 PM"}
    ]
    for meeting in meetings:
        with st.expander(f"{meeting['title']} - {meeting['date']}"):
            st.write(f"Time: {meeting['time']}")
            st.write("Participants: All Teachers")
            st.write("Status: Scheduled")

def show_profile(user_id: int):
    st.title("HOD Profile")
    
    # Get HOD information from mock data
    hod = get_hod_info(user_id)
    if not hod:
        st.error("Unable to load profile information")
        return
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            hod.get('profile_image_url', "https://via.placeholder.com/150"),
            caption=f"{hod['first_name']} {hod['last_name']}"
        )
    with col2:
        st.write(f"**Name:** {hod['first_name']} {hod['last_name']}")
        st.write(f"**Department:** {hod['department']}")
        st.write(f"**Position:** {hod['designation']}")
        st.write(f"**Employee ID:** {hod['employee_id']}")
        st.write(f"**Qualification:** {hod['qualification']}")
        if hod.get('contact_number'):
            st.write(f"**Phone:** {hod['contact_number']}")
        if hod.get('joining_date'):
            st.write(f"**Joining Date:** {hod['joining_date']}")
    
    # Get department information
    dept_info = get_department_info(user_id)
    if dept_info:
        with st.expander("Department Information"):
            st.write(f"**Department:** {dept_info['name']}")
            st.write(f"**HOD:** {dept_info['hod']}")
            st.write(f"**Total Teachers:** {dept_info['teachers']}")
            st.write(f"**Total Students:** {dept_info['students']}")

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

    # Get HOD info for personalization
    hod = get_hod_info(user_id)
    if not hod:
        st.error("Unable to load HOD information. Please contact administrator.")
        return

    # Sidebar navigation
    st.sidebar.title("HOD Portal")
    st.sidebar.image(
        hod.get('profile_image_url', "https://via.placeholder.com/150"),
        caption=f"{hod['first_name']} {hod['last_name']}"
    )
    menu = st.sidebar.radio("", [
        "📊 Dashboard",
        "👩‍🏫 Teachers",
        "📚 Curriculum",
        "📈 Performance",
        "🔧 Resources",
        "📑 Reports",
        "📅 Meetings",
        "👤 Profile"
    ])

    # Route to appropriate function based on menu selection
    if menu == "📊 Dashboard":
        show_dashboard(user_id)
    elif menu == "👩‍🏫 Teachers":
        manage_teachers(user_id)
    elif menu == "📚 Curriculum":
        manage_curriculum(user_id)
    elif menu == "📈 Performance":
        view_performance(user_id)
    elif menu == "🔧 Resources":
        manage_resources(user_id)
    elif menu == "📑 Reports":
        manage_reports(user_id)
    elif menu == "📅 Meetings":
        manage_meetings(user_id)
    elif menu == "👤 Profile":
        show_profile(user_id)