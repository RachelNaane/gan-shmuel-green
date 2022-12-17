from flask import Flask, render_template, redirect, url_for, request, make_response, send_from_directory
import requests
import os.path
import mysql.connector
import pandas as pd
import jsonify
from datetime import datetime


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

@app.route('/truck/<id>', methods=['GET'])
def get_truck_data(id):
    curr_host = "3.9.66.97"

    def_year = datetime.now().year
    def_month = datetime.now().month
    default_start = f"{def_year}{def_month}01000000"
    now = datetime.now()
    date_time = now.strftime("%Y%m%d")
    t1 = request.args.get('from', default= default_start)
    t2 = request.args.get('to', default= datetime)

    response = requests.get(f"http://{curr_host}:8086/item/{id}?t1={t1}")
    if response.status_code == 200:
        data = response.json()
        return data  
        
    elif response.status_code == 400:
        return 'Truck not found', 404
    else:
        return("Error: API request unsuccessful"), 500

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
    
@app.route("/bill/<id>",methods=["GET"])
def bill(id):
    today=datetime.now()
    default_now=today.strftime("%Y%m%d%H%M%S")
    default_day= default_now[:6]+"01000000"

    
    to = request.args.get("to", default= default_now)
    start = request.args.get("from",default= default_day)

    db_connect()
    cursor.execute("USE billdb;") 
    cursor.execute(f"SELECT name from Provider WHERE id = {id};")
    provider_name = cursor.fetchone()
    if not provider_name:
        return make_response("<h1>Unregistered Provider</h1>",400)
    provider_name = provider_name[0]

    
    cursor.execute(f"SELECT id from Trucks WHERE provider_id = {id};")
    truck_list = cursor.fetchall()
    if not truck_list:
        return make_response("<h1>The current provider doesn't have trucks assigned to him</h1>",500)
    
    total_trucks = []
    current_providers_trucks = []
    for truck in truck_list:
        current_providers_trucks.append(truck[0])
    
    curr_host = "3.9.66.97"
    weight_json_array = requests.get(f"http://{curr_host}:8086/weight?t1={start}&t2={to}")
    weight_json_array = weight_json_array.json()
    if weight.status_code == 400:
        return "Bill From That Date Range Wasn't Not Found", 404
    elif weight.status_code == 500:
        return "Error: API request unsuccessful", 500

    rev = {"id":id,"name": provider_name,"from": convert_int_to_correct_date_format(start),
            "to": convert_int_to_correct_date_format(to),"truckcount":0,"sessioncount":0,"products":[],"total":0}

    
    for weight in weight_json_array:
        if weight["id"] not in(current_providers_trucks):
            continue
        else:
            if weight["id"] not in total_trucks:
                total_trucks.append(weight["id"])
        
        if weight["direction"]=="OUT":
            cursor.execute(f"SELECT rate from Rates where scope = '{id}' and product_id = '{weight['produce']}';")
            current_rate = cursor.fetchone()
            if not current_rate:
                cursor.execute(f"SELECT rate from Rates where scope = 'ALL' and product_id = '{weight['produce']}';")
                current_rate = cursor.fetchone()
                current_rate = current_rate[0]
            else:
                current_rate = current_rate[0]

            current_sessions_num = 0
            for container in weight["containers"]:

                temp = requests.get(f"http://{curr_host}:8086/item/{container}?t1={start}")
                temp_container = temp.json()
                current_sessions_num += len(temp_container["sessions"])


            rev["products"].append({"product":weight["produce"],"count":current_sessions_num,"amount":weight["neto"],"rate":current_rate,"pay":(current_rate*int(weight["neto"]))})

    total_sessions_count = 0
    total_pay = 0

    for item in rev["products"]:
        total_sessions_count += item["count"]
        total_pay += item["pay"]

    rev["truckcount"]=len(total_trucks)
    rev["total"] = total_pay
    rev["sessioncount"] = total_sessions_count
    return rev


def convert_int_to_correct_date_format(somenum):
    rev = str(somenum)
    while len(rev) < 14:
        rev+='0'
    rev = f"{rev[:4]}-{rev[4:6]}-{rev[6:8]} {rev[8:10]}:{rev[10:12]}:{rev[10:12]}"
    return rev

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
