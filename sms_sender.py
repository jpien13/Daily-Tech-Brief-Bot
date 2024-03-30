import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_sms_via_email(recipient_email, subject, message):
    
    # Set up the MIME message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject
    body = MIMEText(message, 'plain')
    msg.attach(body)
    
    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, recipient_email, text)
        server.quit()
        print(f"Message successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Example usage
if __name__ == "__main__":
    recipient_number = "9083777981"  # The recipient's phone number
    carrier_gateway = "vtext.com"    # Verison gateway
    recipient_email = f"{recipient_number}@{carrier_gateway}"
    send_sms_via_email(recipient_email, "Subject", "Hello! This is a test message from Email to SMS gateway.")
