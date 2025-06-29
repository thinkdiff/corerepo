import streamlit as st
import hashlib
from datetime import datetime, timedelta

# Mock data modules will be created to replace database connections
import student_panel
import teacher_panel
import hod_panel
import admin_panel

# Page configuration
st.set_page_config(
    page_title="School Management System",
    page_icon="🏫",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.role-selector {
    text-align: center;
    padding: 2rem;
    background-color: #f0f2f6;
    border-radius: 1rem;
    margin: 2rem 0;
}
.stButton>button {
    width: 100%;
    margin-top: 1rem;
}
.title-container {
    text-align: center;
    padding: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_role = None
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.login_time = None
    st.session_state.login_attempts = 0
    st.session_state.last_attempt_time = None

def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(email: str, password: str) -> tuple[bool, str, int]:
    """Verify user credentials and return login status, role and user_id."""
    try:
        # Mock user data
        mock_users = {
            "student@test.com": {"id": 1, "role": "student", "password_hash": hash_password("test123"), "is_active": True},
            "teacher@test.com": {"id": 2, "role": "teacher", "password_hash": hash_password("test123"), "is_active": True},
            "hod@test.com": {"id": 3, "role": "hod", "password_hash": hash_password("test123"), "is_active": True},
            "admin@test.com": {"id": 4, "role": "admin", "password_hash": hash_password("test123"), "is_active": True},
            "inactive@test.com": {"id": 5, "role": "student", "password_hash": hash_password("test123"), "is_active": False}
        }
        
        # Check if email exists in mock data
        if email not in mock_users:
            return False, None, None
        
        user = mock_users[email]
        
        # Check if account is active
        if not user['is_active']:
            st.error("Account is inactive. Please contact administrator.")
            return False, None, None
        
        # Verify password
        if user['password_hash'] == hash_password(password):
            # In a real app, we would update last login time and log the attempt
            return True, user['role'], user['id']
        
        return False, None, None
        
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False, None, None

# Logout Function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_role = None
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.login_time = None

# Main App Logic
if not st.session_state.logged_in:
    # Title and Welcome Message
    st.markdown("<div class='title-container'>", unsafe_allow_html=True)
    st.title("🏫 School Management System")
    st.write("Welcome! Please select your role to continue.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Role Selection
    with st.container():
        st.markdown("<div class='role-selector'>", unsafe_allow_html=True)
        role = st.radio(
            "Select Your Role:",
            ["Student", "Teacher", "HOD", "Admin"],
            horizontal=True,
            key="role_selector"
        )
        
        # Login form
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if email and password:
                # Check for too many failed attempts
                if st.session_state.login_attempts >= 5:
                    if st.session_state.last_attempt_time:
                        time_diff = datetime.now() - st.session_state.last_attempt_time
                        if time_diff < timedelta(minutes=15):
                            st.error(
                                "Too many failed attempts. "
                                f"Please try again in {15 - int(time_diff.total_seconds() / 60)} minutes"
                            )
                            st.stop()
                        else:
                            # Reset attempts after timeout
                            st.session_state.login_attempts = 0
                
                is_valid, user_role, user_id = verify_login(email, password)
                
                if is_valid and user_role.lower() == role.lower():
                    # Successful login
                    st.session_state.logged_in = True
                    st.session_state.current_role = role
                    st.session_state.user_id = user_id
                    st.session_state.user_email = email
                    st.session_state.login_time = datetime.now()
                    st.session_state.login_attempts = 0
                    st.session_state.last_attempt_time = None
                    st.rerun()
                else:
                    # Failed login
                    st.session_state.login_attempts += 1
                    st.session_state.last_attempt_time = datetime.now()
                    st.error(
                        "Invalid credentials or unauthorized role access. "
                        f"Attempts remaining: {5 - st.session_state.login_attempts}"
                    )
            else:
                st.error("Please enter both email and password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Help text
        st.markdown("""
        <div style='text-align: center; color: #666;'>
        <small>Please contact your administrator if you need help accessing your account.</small>
        </div>
        """, unsafe_allow_html=True)

else:
    # Show logout button in sidebar
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
    
    # Session timeout check (8 hours)
    if st.session_state.login_time:
        session_age = datetime.now() - st.session_state.login_time
        if session_age > timedelta(hours=8):
            st.warning("Your session has expired. Please login again.")
            logout()
            st.rerun()
    
    # Route to appropriate panel based on role with user context
    if st.session_state.current_role == "Student":
        student_panel.show_panel(
            user_id=st.session_state.user_id,
            email=st.session_state.user_email
        )
    elif st.session_state.current_role == "Teacher":
        teacher_panel.show_panel(
            user_id=st.session_state.user_id,
            email=st.session_state.user_email
        )
    elif st.session_state.current_role == "HOD":
        hod_panel.show_panel(
            user_id=st.session_state.user_id,
            email=st.session_state.user_email
        )
    elif st.session_state.current_role == "Admin":
        admin_panel.show_panel(
            user_id=st.session_state.user_id,
            email=st.session_state.user_email
        )