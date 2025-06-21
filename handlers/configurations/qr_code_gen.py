import qrcode
import io
import base64
import pyotp


def get_2fa_qr_uri(email, secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=email, issuer_name="Setekh Dashboard")
    return generate_qr_code(uri)


def generate_qr_code(uri):
    qr_image = qrcode.make(uri)
    buffer = io.BytesIO()
    qr_image.save(buffer, 'PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
