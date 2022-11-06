import configparser
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    with open("message.txt", "r", encoding="utf-8") as msg:
        read_message = msg.read()
        subject, body = read_message.split("\n$separator$\n")
        body = body.replace("$date", str(datetime.datetime.today()).split(" ")[0])

    print("Wait, the letter is being sent")

    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_receiver, message.as_string())

    print("The letter was sent successfully")
