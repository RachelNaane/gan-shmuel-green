from flask import Flask, render_template, redirect, url_for, request, make_response, send_from_directory
import os.path
import mysql.connector
import pandas as pd


app = Flask(__name__)


@app.route("/truck/<id>", methods=["PUT"])
def update_provider_id(id):
    new_provider_id = request.json["provider_id"]
    
    db_connect()
    cursor.execute("USE billdb;")
    cursor.execute(f"SELECT * from Provider where id = {int(new_provider_id)};")
    is_a_known_provider = cursor.fetchone()
    if not is_a_known_provider:
        return make_response("<h1>Unown Provider</h1>",500)

    try:
        cursor.execute(f"UPDATE Trucks SET provider_id = {int(new_provider_id)} where id = '{id}';")
        return make_response("<h1>Updated</h1>",200)  
    except:
        return make_response("<h1>Failure</h1>",500)


@app.route("/truck", methods=["POST"])
def truck():
    provider_id = request.json["provider"]
    truck_id = request.json["id"]
    db_connect()
    cursor.execute("USE billdb;")
    cursor.execute(f"SELECT * from Provider where id = {int(provider_id)};")
    is_a_known_provider = cursor.fetchone()
    if not is_a_known_provider:
        return make_response("<h1>Unown Provider</h1>",500)
    try:
        cursor.execute(f"INSERT INTO Trucks VALUES ('{truck_id}',{int(provider_id)});")
    except:
        return make_response("<h1>Failure</h1>",500)
    return make_response("<h1>Registerd</h1>",200)


@app.route("/")
def home():
    return make_response("<h1>WELCOME TO GAN SHMUEL'S JUICE PRODUCTION'S BILLING CLASS</h1>",200)


@app.route("/health")
def health():
    try:
        db_connect()
        cursor.execute("SELECT 1;")
    except:
        return make_response("<h1>Failure</h1>",500)
    return make_response("<h1>OK</h1>",200)


@app.route("/rates", methods=["GET","POST"])
def get_rates():
    if request.method=="GET":
        file_to_get = request.json["filename"]  
        if not os.path.isfile(f"in/{file_to_get}"):
            return make_response("<h1>Sorry, The File Doesn't Exist</h1>",500)
        uploads = os.path.join(app.root_path,"in")
        respone = make_response(send_from_directory(path="rates.xlsx",directory=uploads))
        respone.status_code = 200
        return respone 

    else:
        file_name = request.json["filename"]
        if not os.path.isfile(f"in/{file_name}"):        
            return make_response("<h1>Sorry, The File Doesn't Exist</h1>",500) 
        db_connect()
        cursor.execute("USE billdb;") 

        d1 = pd.read_excel(f"in/{file_name}")
        for index, row in d1.iterrows():
            curr_prod = row["Product"]
            curr_rate = row["Rate"]
            curr_scope = row["Scope"]
            cursor.execute(f"select * from Rates where product_id = '{curr_prod}';") 
            is_a_doc_product = cursor.fetchall() 
            if is_a_doc_product: 
                cursor.execute(f"select * from Rates WHERE (product_id='{curr_prod}' AND scope='{curr_scope}');")
                need_to_update_rate = cursor.fetchall() 
                if need_to_update_rate:
                    cursor.execute(f"UPDATE Rates SET rate = {curr_rate}  WHERE product_id = '{curr_prod}' AND scope='{curr_scope}';")
                else:
                    cursor.execute(f"insert into Rates values ('{curr_prod}',{curr_rate},'{curr_scope}');")
            else:
                cursor.execute(f"insert into Rates values ('{curr_prod}',{curr_rate},'{curr_scope}');")
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


@app.route("/provider", methods=["POST"])  
def register_provider():
    provider_name= request.json["name"]
    db_connect()
    cursor.execute("USE billdb;") 
    cursor.execute(f"select * from Provider where name = '{provider_name}';") #checks if providers exists
    is_a_known_provider = cursor.fetchone() #checks if there is any output from the requested query
    if is_a_known_provider: #checks the variable if it has a context or not (no context - means that provider doesn't exist yet)
        return make_response("<h1>Provider already registered</h1>",500)
    cursor.execute(f"INSERT INTO Provider (name) VALUES ('{provider_name}');")
    cursor.execute(f"select id from Provider where name = '{provider_name}';")
    new_id = cursor.fetchone()
    return {
        "id": new_id
    }
    


def db_connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
    host="bill-db",
    user="root",
    password="password",
    port=3306
    )   
    cursor = cnx.cursor(buffered=True)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
