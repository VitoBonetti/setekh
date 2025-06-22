import smtplib
import ssl


def check_smtp(server_ip, port, email, password):
    if not server_ip or not port or not email or not password:
        print("Missing something")
        return

    try:
        server = smtplib.SMTP(server_ip, port)
        server.set_debuglevel(0)

        server.starttls(context=ssl._create_unverified_context())

        server.login(email, password)
        print("Login successful")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP authentication failed for {email}: {e}. App password might be incorrect or revoked.")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"SMTP connection failed: {e}. Check server address or port.")
        return False
    except smtplib.SMTPException as e:
        print(f"An SMTP error occurred: {e}")
        return False
    except ssl.SSLError as e:
        print(f"SSL error: {e}. Check your network or server certificate.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    finally:
        try:
            if 'server' in locals():
                server.quit() # close the connection
        except Exception as e:
            print(f"Error closing SMTP connection: {e}")