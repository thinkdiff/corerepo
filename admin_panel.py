import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# Import mock data functions
from mock_data import get_admin_info, get_system_stats, get_all_users, create_user, get_system_logs, get_system_reports, backup_system, restore_system

def show_dashboard(user_id: int):
    # Get admin information from mock data
    admin = get_admin_info(user_id)
    if not admin:
        st.error("Unable to load admin information")
        return
    
    st.title(f"Welcome, {admin['first_name']} {admin['last_name']}!")
    st.write("System Overview")
    
    # Get system statistics from mock data
    stats = get_system_stats()
    
    # System Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", str(stats['total_students']), "+50")
    with col2:
        st.metric("Total Teachers", str(stats['total_teachers']), "+2")
    with col3:
        st.metric("Departments", str(stats['total_departments']), "")
    with col4:
        st.metric("Active Users", str(stats['active_users']), "+25")
    
    # Quick Access
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("User Management", use_container_width=True):
            st.session_state.admin_menu = "👥 User Management"
    with col2:
        if st.button("System Settings", use_container_width=True):
            st.session_state.admin_menu = "⚙️ Settings"
    with col3:
        if st.button("Generate Reports", use_container_width=True):
            st.session_state.admin_menu = "📊 Reports"

def manage_users(user_id: int):
    st.title("User Management")
    
    # Add New User
    with st.expander("Add New User"):
        with st.form("new_user_form"):
            user_type = st.selectbox("User Type", ["Student", "Teacher", "HOD", "Admin"])
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
            with col2:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
            department = st.selectbox("Department", ["Physics", "Chemistry", "Mathematics", "Biology", "Computer Science"])
            if st.form_submit_button("Create User"):
                if not all([full_name, email, username, password, department]):
                    st.error("Please fill in all required fields")
                else:
                    # Use mock function to create user
                    user_data = {
                        "full_name": full_name,
                        "email": email,
                        "username": username,
                        "password": password,
                        "user_type": user_type,
                        "department": department
                    }
                    if create_user(user_data):
                        st.success("User created successfully!")
                    else:
                        st.error("Error creating user")
    
    # User Directory
    st.subheader("User Directory")
    users = get_all_users()
    
    if users:
        users_df = pd.DataFrame(users)
        st.dataframe(users_df, use_container_width=True)
    else:
        st.info("No users found")

def manage_departments(user_id: int):
    st.title("Department Management")
    
    # Add Department
    with st.expander("Add New Department"):
        dept_name = st.text_input("Department Name")
        dept_code = st.text_input("Department Code")
        description = st.text_area("Description")
        max_capacity = st.number_input("Maximum Capacity", min_value=0)
        if st.button("Create Department"):
            if not all([dept_name, dept_code]):
                st.error("Please fill in all required fields")
            else:
                st.success("Department created successfully!")
    
    # Department List
    st.subheader("Departments")
    dept_data = {
        "Name": ["Physics", "Chemistry", "Mathematics"],
        "HOD": ["Prof. Johnson", "Dr. Williams", "Dr. Brown"],
        "Teachers": [12, 10, 8],
        "Students": [320, 280, 250]
    }
    st.dataframe(pd.DataFrame(dept_data), use_container_width=True)

def system_settings(user_id: int):
    st.title("System Settings")
    
    # Academic Year Settings
    with st.expander("Academic Year Settings"):
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Start Date")
        with col2:
            st.date_input("End Date")
        st.multiselect("Holidays", ["New Year", "Independence Day", "Christmas"])
        if st.button("Update Academic Calendar"):
            st.success("Academic calendar updated!")
    
    # System Configuration
    with st.expander("System Configuration"):
        st.toggle("Enable Email Notifications")
        st.toggle("Enable SMS Alerts")
        st.number_input("Session Timeout (minutes)", value=30)
        st.selectbox("Default Theme", ["Light", "Dark"])
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

def manage_logs(user_id: int):
    st.title("System Logs")
    
    # Log Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        st.date_input("From Date ", key="log_from")
    with col2:
        st.date_input("To Date ", key="log_to")
    with col3:
        st.selectbox("Log Type", ["All", "Error", "Warning", "Info"])
    
    # Get system logs from mock data
    logs = get_system_logs()
    
    if logs:
        logs_df = pd.DataFrame(logs)
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("No logs found")

def generate_reports(user_id: int):
    st.title("Report Generation")
    
    # Get system reports from mock data
    reports = get_system_reports()
    
    # Report Configuration
    with st.form("report_form"):
        report_type = st.selectbox("Report Type", [
            "User Activity Report",
            "Academic Performance Report",
            "Attendance Summary Report",
            "Department Statistics Report"
        ])
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("From Date  ")
        with col2:
            st.date_input("To Date  ")
        st.multiselect("Include Sections", [
            "Student Statistics",
            "Teacher Statistics",
            "Academic Metrics",
            "System Usage"
        ])
        st.selectbox("Format", ["PDF", "Excel", "CSV"])
        if st.form_submit_button("Generate Report"):
            st.success("Report generated successfully!")
            st.download_button("Download Report", "dummy_data", "report.pdf")
    
    # Available Reports
    st.subheader("Available Reports")
    if reports:
        for report in reports:
            with st.expander(f"{report['name']} - {report['generated']}"):
                st.write(f"Status: {report['status']}")
                if report['status'] == 'Ready':
                    st.download_button(
                        "Download Report",
                        "dummy_data",
                        f"{report['name']}.pdf",
                        key=f"download_{report['name']}"
                    )

def manage_backup(user_id: int):
    st.title("Backup & Restore")
    
    # Backup
    st.subheader("Create Backup")
    col1, col2 = st.columns(2)
    with col1:
        backup_type = st.selectbox("Backup Type", ["Full Backup", "Incremental Backup"])
    with col2:
        storage_location = st.selectbox("Storage Location", ["Local Storage", "Cloud Storage"])
    if st.button("Start Backup"):
        # Use mock function to backup system
        if backup_system():
            st.success("Backup created successfully!")
        else:
            st.error("Error creating backup")
    
    # Restore
    st.subheader("Restore System")
    backup_file = st.file_uploader("Upload Backup File")
    if st.button("Restore System"):
        if backup_file:
            st.warning("This will override current system data. Are you sure?")
            if st.button("Confirm Restore"):
                # Use mock function to restore system
                if restore_system(backup_file):
                    st.success("System restored successfully!")
                else:
                    st.error("Error restoring system")
        else:
            st.error("Please upload a backup file")

def show_profile(user_id: int):
    st.title("Admin Profile")
    
    # Get admin information from mock data
    admin = get_admin_info(user_id)
    if not admin:
        st.error("Unable to load profile information")
        return
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            admin.get('profile_image_url', "https://via.placeholder.com/150"),
            caption=f"{admin['first_name']} {admin['last_name']}"
        )
    with col2:
        st.write(f"**Name:** {admin['first_name']} {admin['last_name']}")
        st.write(f"**Role:** {admin['designation']}")
        if admin.get('contact_number'):
            st.write(f"**Phone:** {admin['contact_number']}")
    
    with st.expander("Security Settings"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        if st.button("Update Password"):
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

    # Get admin info for personalization
    admin = get_admin_info(user_id)
    if not admin:
        st.error("Unable to load admin information. Please contact administrator.")
        return

    # Sidebar navigation
    st.sidebar.title("Admin Portal")
    st.sidebar.image(
        admin.get('profile_image_url', "https://via.placeholder.com/150"),
        caption=f"{admin['first_name']} {admin['last_name']}"
    )
    menu = st.sidebar.radio("", [
        "📊 Dashboard",
        "👥 User Management",
        "🏢 Departments",
        "⚙️ Settings",
        "📝 Logs",
        "📊 Reports",
        "�� Backup",
        "👤 Profile"
    ])

    # Route to appropriate function based on menu selection
    if menu == "📊 Dashboard":
        show_dashboard(user_id)
    elif menu == "👥 User Management":
        manage_users(user_id)
    elif menu == "🏢 Departments":
        manage_departments(user_id)
    elif menu == "⚙️ Settings":
        system_settings(user_id)
    elif menu == "📝 Logs":
        manage_logs(user_id)
    elif menu == "📊 Reports":
        generate_reports(user_id)
    elif menu == "💾 Backup":
        manage_backup(user_id)
    elif menu == "👤 Profile":
        show_profile(user_id)