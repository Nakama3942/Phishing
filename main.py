import configparser
import smtplib
from email.message import EmailMessage


if __name__ == '__main__':
    email_sender = ""
    email_password = ""
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")

        email_sender = config["Mail"]["mail_login"]
        email_password = config["Mail"]["mail_password"]

    except KeyError:
        check_mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        while True:
            try:
                email_sender = input("Enter the login: ")
                email_password = input("Enter the password: ")
                check_mail.login(email_sender, email_password)
                break
            except:
                print("Login failed\nIncorrect login or password. Try again")

        config = configparser.ConfigParser()
        config.add_section('Mail')
        config.set('Mail', 'mail_login', email_sender)
        config.set('Mail', 'mail_password', email_password)
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    email_receiver = input("\nEnter the recipient's address: ")
    with open("subject.txt", "r", encoding="utf-8") as f1:
        subject = f1.read()
    with open("body.txt", "r", encoding="utf-8") as f2:
        body = f2.read()

    print("\nWait, the letter is being sent")

    message = EmailMessage()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = subject
    message.set_content(body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_receiver, message.as_string())

    print("\nThe letter was sent successfully")
