from flask import Flask, render_template, request, redirect, url_for
import os
from flask_mail import Mail, Message
import re

app = Flask(__name__)


# post requestt
@app.post("/triger")
def staff_are_pushed():
    content = str(request.get_json(silent=True)) #add the jason content to a string we can run tests on 
    to_check = str(re.search("refs/heads/main", str(content))) #find the branch of the push
    if to_check != "None": # if barnch = main send emails and run tests
        print("merge to main!!!!!.... \n starting testings")  
        os.system("bash phase1.sh")
        #send_mail(content)                                         #########   figure out the place for us to send
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
    app.run(host="0.0.0.0",debug=True)
