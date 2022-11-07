#  Copyright © 2022 Kalynovsky Valentin. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import configparser
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


if __name__ == '__main__':
    # Reading the login and password from which phishing will
    # be sent. If the data file is missing, then the program
    # is launched on the computer for the first time and the
    # authorization stage begins with saving the data.
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

    # Preparing the text of the letter for sending
    email_receiver = input("\nEnter the recipient's address: ")
    phish_link = input("\nEnter the phishing link: ")
    with open("message.txt", "r", encoding="utf-8") as msg:
        read_message = msg.read()
        subject, body = read_message.split("\n$separator$\n")
        body = body.replace("$date", str(datetime.datetime.today()).split(" ")[0])
        body = body.replace("$link", phish_link)
    print("Wait, the letter is being sent")

    # Formation of a letter package for sending
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    # Sending letter
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_receiver, message.as_string())
    print("The letter was sent successfully")
