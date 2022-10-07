import smtplib, ssl
from tkinter import *

def send_email(receiver_email):  
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "pednekaronkar09@gmail.com"
    password = 'onky8692871530'
    message = """\
    Subject: Social Distancing
    
    You have not been following social distancing for more than 5 seconds.
    Kindly follow them"""
    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        messagebox.showinfo('Success','Email sent to {}'.format(receiver_email))