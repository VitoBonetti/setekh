import uuid
import bcrypt
import pyotp
from datetime import datetime, timedelta
from utils.handle_db_connection import connect_to_db
from queries.queries import UPDATE_SESSION, CHECK_SESSION, DELETE_SESSION

SESSIONS = {}
SESSION_DURATION_MINUTES = 60


def login(email, password, state, e):
    try:
        conn = connect_to_db(state)
        cursor = conn.cursor()
        cursor.execute("SELECT uuid, password, is_active, is_master, 2fa_secret FROM users WHERE email = %s", (email,))
        user_profile = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user_profile:
            state.login_info_text.value = "Invalid credentials."
            state.email_login_text_field.focus()
            state.page.update()
            return False

        user_id, hashed_pw, is_active, is_master, secret = user_profile

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

        if is_master:
            state.current_role = "Master"

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
    state.email_login_text_field.value = ""
    state.password_login_text_field = ""
    state.verify_code_login_text_field.value = ""
    state.page.update()
    if not pyotp.TOTP(secret).verify(otp_code):
        state.login_info_text.value = "Invalid 2FA code."
        state.page.update()
        return False

    session_id = create_session(state)

    state.page.client_storage.set("session_id", session_id)
    state.page.client_storage.set("user_uuid", state.temp_user_id)

    state.page.go("/")
    return None


def create_session(state):
    session_id = str(uuid.uuid4())
    state.session_id = session_id
    state.session_user_uuid = state.temp_user_id
    expires_at = datetime.now() + timedelta(minutes=SESSION_DURATION_MINUTES)
    try:
        conn = connect_to_db(state)
        cursor = conn.cursor()
        cursor.execute(UPDATE_SESSION, (session_id, expires_at, state.temp_user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return session_id
    except Exception as e:
        print(f"create_session: {e}")
        return None



def is_session_valid(state):
    if not state.session_id or not state.session_user_uuid:
        return False
    try:
        conn = connect_to_db(state)
        cursor = conn.cursor()
        cursor.execute(CHECK_SESSION, (state.session_user_uuid, state.session_id))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"is_session_valid: {e}")
        return False

    if not row:
        return False

    if row[1]:
        state.current_role = "Master"

    expires_at = row[0]
    if expires_at > datetime.now():
        return True
    else:
        return False


def logout(state, e):
    print("logout called")
    try:
        conn = connect_to_db(state)
        cursor = conn.cursor()
        cursor.execute(DELETE_SESSION, (state.session_user_uuid,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"logout: {e}")
    state.session_id = None
    state.session_user_uuid = None
    state.temp_user_id = None
    state.temp_user_email = None
    state.temp_user_secret = None
    state.page.client_storage.clear()
    state.page.go("/300")
