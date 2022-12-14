from flask import Flask, render_template, request, redirect, url_for
import os
from flask_mail import Mail, Message
import re

app = Flask(__name__)



def find_mail(content): # crazy complex function that do some magic on a string 
	lst = str(re.findall('\S+@\S+', content))  
	email_address = re.sub(r'[,,\']', '',lst[-1])
	return email_address


def send_mail(content): # func that sends mail
        # mail conf
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
        #send
        email_to = ['ratash3@gmail.com', 'pashutdvir@gmail.com', 'yota.benz@outlook.com', 'Elior1001@gmail.com', 'roei.keisar@gmail.com']
        msg = Message("CI RESULT", sender=app.config.get("MAIL_USERNAME"), recipients=email_to)
        with app.open_resource("../../billing/score.txt") as fp:
            msg.attach("./../billing/score.txt", "text/plain", fp.read())
        with app.open_resource("../../weight/score.txt") as fp:
            msg.attach("../../weight/score.txt", "text/plain", fp.read())
        mail.send(msg) 
       

# post requestt
@app.post("/triger")
def staff_are_pushed():
    content = str(request.get_json(silent=True)) #add the jason content to a string we can run tests on 
    to_check = str(re.search("refs/heads/main", str(content))) #find the branch of the push
    if to_check != "None": # if barnch = main send emails and run tests
        print("merge to main!!!!!.... \n starting testings")  
        #os.system("bash phase1.sh")
        send_mail(content)                                         #########   figure out the place for us to send
    return "push recived ... mails will be sent when merged with main"
    

# home page(not required but nice to have)
@app.get("/")
def home_page():
    return render_template("index.html")


# helth checks(return ok... daaaaa)
@app.get("/health")
def health_check():
    return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
