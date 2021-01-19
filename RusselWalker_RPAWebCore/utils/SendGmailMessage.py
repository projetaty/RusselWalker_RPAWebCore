#!/usr/bin/python3
import smtplib, ssl

# Import the email modules we'll need
from email.message import EmailMessage

port    =   587
user    =   "email@gmail.com"
passwd  =   "********************"
context =   ssl.create_default_context()

with smtplib.SMTP("smtp.gmail.com", port) as gmail:
    print(gmail.noop())
    print(gmail.ehlo())
    gmail.ehlo()
    gmail.starttls(context=context)
    gmail.ehlo()
    gmail.login(user, passwd)
    print(gmail.ehlo())
    