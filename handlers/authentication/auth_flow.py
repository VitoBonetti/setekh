import uuid
import bcrypt
import pyotp
from datetime import datetime, timedelta
from utils.handle_db_connection import connect_to_db

SESSIONS = {}
SESSION_DURATION_MINUTES = 60


def login(email, password, state, e):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT uuid, password, is_active, 2fa_secret FROM users WHERE email = %s", (email,))
        user_profile = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user_profile:
            state.login_info_text.value = "Invalid credentials."
            state.email_login_text_field.focus()
            state.page.update()
            return False

        user_id, hashed_pw, is_active, secret = user_profile

        if not is_active:
            state.login_info_text.value = "Account not active."
            state.email_login_text_field.focus()
            state.page.update()
            return False

        if not bcrypt.checkpw(password.encode(), hashed_pw.encode()):
            state.login_info_text.value = "Invalid credentials."
            state.email_login_text_field.focus()
            state.page.update()
            return False

        state.temp_user_id = user_id
        state.temp_user_secret = secret
        state.temp_user_email = email

        state.login_info_text.value = "Password valid, 2FA required."
        state.verify_code_login_text_field.visible = True
        state.verify_code_login_button.visible = True
        state.page.update()

        return True
    except Exception as e:
        state.login_info_text.value = str(e)
        state.email_login_text_field.focus()
        state.page.update()
        return False


def otp_login(otp_code, state, e):
    secret = state.temp_user_secret
    if not pyotp.TOTP(secret).verify(otp_code):
        state.login_info_text.value = "Invalid 2FA code."
        state.page.update()
        return False

    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "user_id": state.temp_user_id,
        "email": state.temp_user_email,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(minutes=SESSION_DURATION_MINUTES)
    }
    state.email_login_text_field.value = ""
    state.password_login_text_field = ""
    state.verify_code_login_text_field.value = ""
    state.verify_code_login_text_field.visible = False
    state.verify_code_login_button.visible = False
    state.page.update()

    state.session_id = session_id
    state.page.go("/1")


def is_session_valid(state):
    session = SESSIONS.get(state.session_id)
    if not session:
        return False
    if session["expires_at"] < datetime.now():
        del SESSIONS[state.session_id]
        return False
    return True


def logout(state, e):
    print("logout called")
    if state.session_id in SESSIONS:
        del SESSIONS[state.session_id]
    state.session_id = None
    state.temp_user_id = None
    state.temp_user_email = None
    state.temp_user_secret = None
    state.page.go("/200")
