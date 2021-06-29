import smtplib
import time
import os
from email.message import EmailMessage

#https://myaccount.google.com/lesssecureapps needs to be turn off

# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()

sender_email = os.getenv('EMAIL_ACCOUNT')       #EMAIL_ACCOUNT and EMAIL_PASS should be set as enviroment variables 
reciever_email = os.getenv('EMAIL_ACCOUNT')     #    linux -> export EMAIL_ACCOUNT="email"
EMAIL_PASS = os.getenv('EMAIL_PASS')

#----------------------Ejemplo de email---------------------
# msg = EmailMessage()
# msg['FROM'] = sender_email
# msg['To'] = reciever_email
# msg['Subject'] = "texto"
# msg.set_content('texto')
#-----------------------------------------------------------

def send_mail(msg):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email,EMAIL_PASS)
    print("Logged In")
    server.send_message(msg)
    server.quit()
    print("Email sent")

def send_msg(subject, body):
    msg = EmailMessage()
    msg['FROM'] = sender_email
    msg['To'] = reciever_email
    msg['Subject'] = subject
    msg.set_content(body)
    send_mail(msg)



