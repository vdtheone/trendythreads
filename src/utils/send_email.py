import smtplib
import ssl


def send_otp_by_email(receivers_mail, otp):
    sender_mail = "vishal262.rejoice@gmail.com"
    subject = "Your OTP For Varification"
    message = f"OTP = {otp}"
    password = "qtqk xtzf jgzy raiu"
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender_mail, password)
            msg = f"Subject: {subject}\n\n{message}"
            server.sendmail(sender_mail, receivers_mail, msg)
    except Exception as e:
        print("Error", e)
