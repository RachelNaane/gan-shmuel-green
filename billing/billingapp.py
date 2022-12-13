from flask import Flask, render_template, redirect, url_for, request, make_response
import os.path
import mysql.connector


app = Flask(__name__)

@app.route("/")
def home():
    return make_response("<h1>HELLO</h1>",200)

@app.route("/health")
def health():
    try:
        db_connect()
        cursor.execute("SELECT 1;")
    except:
        return make_response("<h1>Failure</h1>",500)
    return make_response("<h1>OK</h1>",200)


@app.route("/provider/<provider_id>", methods=["PUT"])
def update_provider(provider_id):
    name_to_change = request.json["name"]
    print(name_to_change,provider_id)
    try:
        db_connect()
        cursor.execute("USE billdb;")
        cursor.execute(f"UPDATE Provider SET name = '{name_to_change}' where id = {provider_id};")
        return make_response("<h1>OK</h1>",200)
    except:
        return make_response("<h1>Unable to update</h1>",500)



def db_connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
    )   
    cursor = cnx.cursor()
    

def DB_INITIALIZATION():
    db_connect()
    with open("db/billingdb.sql","r") as f:
        sql_command = f.read()
    cursor.execute(sql_command,multi=True)
    #cnx.commit is overloading the server for some reason ffs
    cnx.close()
    

if __name__ == "__main__":
    DB_INITIALIZATION()
    app.run(host='0.0.0.0')
