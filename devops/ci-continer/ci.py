from flask import Flask, render_template, request, redirect, url_for
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ratash3@gmail.com'
app.config['MAIL_PASSWORD'] = 'eksghxoohjkwcqck'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER']= 'ratash3@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

# Render index.html
@app.get("/triger")
def staff_are_pushed():
    request.data
    os.system("bash start_testing.sh")

    #send mail
    email_address="ratash3@gmail.com"
    msg = Message("CI RESULT", sender=app.config.get("MAIL_USERNAME"), recipients=['ratash3@gmail.com', 'pashutdvir@gmail.com', 'yota.benz@outlook.com'])
    msg.add_recipient(email_address)

    message=""
    with open("score.txt", "r") as file:
        for line in file:
            message+=f"{line}\n"
    msg.body=message
    msg.body="success!!!!!!"
    mail.send(msg)

    return "running script to pull the data... test will be sent by mail"

# Render index.html
@app.get("/")
def home_page():
    return render_template("index.html")

# Render index.html
@app.get("/health")
def health_check():
    return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)