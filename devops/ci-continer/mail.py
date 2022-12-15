from flask import Flask
from flask_mail import Mail , Message

mail = Mail()

app = Flask(__name__)
mail.init_app(app) 

def send_mail(): # func that sends mail
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
        with app.open_resource("/app/test/gan-shmuel-green/billing/tests/score.txt") as fp:
            msg.attach("/app/test/gan-shmuel-green/billing/tests/score.txt", "text/plain", fp.read())
        with app.open_resource("/app/test/gan-shmuel-green/weight/tests/score.txt") as fp:
            msg.attach("/app/test/gan-shmuel-green/weight/tests/score.txt", "text/plain", fp.read())
        mail.send(msg) 
        
        
send_mail()