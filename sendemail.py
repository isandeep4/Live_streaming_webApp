import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail:
    def __init__(self):
        self.subject = 'Security Alert From Your Webcam!'
        self.body = 'This email was sent by our security system. There might be someone/something moving ' \
                   'in your room. ' \
                   'Please check the video and ensure your safety. Thank you.'
        #Please enter your email id and password to receive the notification
        self.sender_email = ""
        self.receiver_email = ""
        self.password = ""

    def sendmail(self):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject
        message["Bcc"] = self.receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(self.body, "plain"))
        filename = 'screenshot.png'
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)

        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, text)