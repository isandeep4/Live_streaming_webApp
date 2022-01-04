import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendEmail:
    def __init__(self):
        self.subject = "An email with attachment from Python"
        self.body = "One movement is detected"
        self.sender_email = "sujoysaha.test@gmail.com"
        self.receiver_email = "sujoysaha.edu@gmail.com"
        self.password = "Sujoy@123"

    def sendmail(self):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject
        message["Bcc"] = self.receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(self.body, "plain"))

        # filename = "document.pdf"  # In same directory as script
        #
        # # Open PDF file in binary mode
        # with open(filename, "rb") as attachment:
        #     # Add file as application/octet-stream
        #     # Email client can usually download this automatically as attachment
        #     part = MIMEBase("application", "octet-stream")
        #     part.set_payload(attachment.read())
        #
        # # Encode file in ASCII characters to send by email
        # encoders.encode_base64(part)
        #
        # # Add header as key/value pair to attachment part
        # part.add_header(
        #     "Content-Disposition",
        #     f"attachment; filename= {filename}",
        # )
        #
        # # Add attachment to message and convert message to string
        # message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, text)