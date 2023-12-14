import smtplib
import ssl


def send_otp_by_email(receivers_mail, otp, message):
    sender_mail = "vishal262.rejoice@gmail.com"
    subject = f"Your OTP For {message}"

    # HTML template for the email body
    message = f"""
    <html>
    <head></head>
    <body style="font-family: Arial, sans-serif;">
        <div style="background-color: #f4f4f4; padding: 20px; border-radius: 8px;">
            <h2 style="color: #333;">Verification OTP</h2>
            <p style="font-size: 16px;">Hello there!</p>
            <p style="font-size: 16px;">
                Your OTP for verification is: <strong>{otp}</strong>
            </p>
            <p style="font-size: 16px;">
                Please use this OTP to complete the verification process.
            </p>
            <p style="font-size: 14px; color: #777;">
                This is an automated message. Please do not reply.
            </p>
        </div>
    </body>
    </html>
    """

    password = "qtqk xtzf jgzy raiu"
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender_mail, password)
            # Specify MIME type as text/html for HTML content
            msg = (
                f"Subject: {subject}\n"
                f"MIME-Version: 1.0\n"
                f"Content-type: text/html\n\n"
                f"{message}"
            )
            server.sendmail(sender_mail, receivers_mail, msg)
    except Exception as e:
        print("Error", e)
