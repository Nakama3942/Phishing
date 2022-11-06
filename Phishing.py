import os
import smtplib, ssl
from email.message import EmailMessage

email_password = '...'  # Specially cut out the original
email_sender = "..."  # Specially cut out the original
email_receiver = input("\n   Enter the recipient's address: ")  # address
with open("subject.txt", "r", encoding="utf-8") as f1:
    subject = f1.read()
with open("body.txt", "r", encoding="utf-8") as f2:
    body = f2.read()

print("\n   Wait, the letter is being sent")

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
print("\n   The letter was sent successfully")
os.system("pause")
