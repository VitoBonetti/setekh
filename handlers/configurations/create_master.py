import json
import bcrypt
import uuid
import pymysql
import pyotp
import os
from utils.handle_db_connection import connect_to_db
from helpers.check_email import check_email
from helpers.hash_psw import hash_password, compare_password
from handlers.configurations.qr_code_gen import get_2fa_qr_uri
from queries.queries import CREATE_MASTER


def register_master(email, password1, password2, state, e):
    state.step2_info_progress.visible = True
    if not email or not password1 or not password2:
        state.step2_info_progress.visible = False
        state.step2_info_text.value = "Email and passwords are required."
        state.page.update()
        return

    if not check_email(email):
        state.step2_info_progress.visible = False
        state.step2_info_text.value = "Email is not valid."
        state.page.update()
        return

    if not compare_password(password1, password2):
        state.step2_info_progress.visible = False
        state.step2_info_text.value = "The password are not the same."
        state.page.update()
        return

    user_uuid = str(uuid.uuid4())
    twofa_secret = pyotp.random_base32()
    hashed_password = hash_password(password1)

    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute(CREATE_MASTER, (user_uuid, email, hashed_password, True, False, True, True, twofa_secret))
        conn.commit()
        qr_code_image = get_2fa_qr_uri(email, twofa_secret)
        state.qr_code_image_control.src = f"data:image/png;base64,{qr_code_image}"
        state.qr_code_image_control.visible = True
        state.step2_info_text.value = "Scan the QR code with Google Authenticator or similar app."
        state.step2_info_progress.visible = False
        state.verify_code_button.visible = True
        state.verify_code_text_field.visible = True
        state.page.update()

    except pymysql.MySQLError as err:
        print(err)
        state.step2_info_text.value = err.__str__()
        state.step2_info_progress.visible = False
        state.page.update()
    except Exception as e:
        print(e)
        state.step2_info_text.value = str(e)
        state.step2_info_progress.visible = False
        state.page.update()
    finally:
        cursor.close()
        conn.close()


def verify_code(state, e):
    code = state.verify_code_text_field.value
    if not code or not code.isdigit():
        state.step2_info_text.value = "Please enter a valid 6-digit code."
        state.step2_info_text.update()
        return

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Fetch latest user's 2FA secret (assuming you're registering just 1 user here)
        cursor.execute("SELECT uuid, 2fa_secret FROM users ORDER BY created_at DESC LIMIT 1")
        user = cursor.fetchone()
        if not user:
            state.step2_info_text.value = "No user found for verification."
            state.step2_info_text.update()
            return

        user_id, secret = user
        totp = pyotp.TOTP(secret)
        if totp.verify(code):
            # Enable account
            cursor.execute("UPDATE users SET is_active = TRUE WHERE uuid = %s", (user_id,))
            conn.commit()

            state.step2_info_text.value = "2FA code verified. User activated!"
            state.verify_code_button.visible = False
            state.verify_code_text_field.visible = False
            state.qr_code_image_control.visible = False

            config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
            try:
                with open(config_file_path) as config_file:
                    config_data = json.load(config_file)
            except FileNotFoundError:
                print(f"Error: The file '{config_file_path}' was not found.")
                # You might want to exit or handle this more gracefully, e.g., create a default config
                return
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from '{config_file_path}'. Check file format.")
                return

            config_data["step"] = "Done"
            try:
                with open(config_file_path, 'w') as f:
                    json.dump(config_data, f, indent=4)
            except IOError as e:
                print(f"Error saving file '{config_file_path}': {e}")

        else:
            state.step2_info_text.value = "Invalid 2FA code. Try again."

        state.page.update()

    except Exception as ex:
        state.step2_info_text.value = f"Error verifying code: {ex}"
        state.page.update()
        return
    finally:
        cursor.close()
        conn.close()

    state.page.go("/")
