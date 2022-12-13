from flask import Flask, request, abort
from datetime import datetime
from db import dbconnection
import json, re



app = Flask(__name__)


#This is the Post Mehthod Implemented by yossi
@app.route("/weight", methods=["POST"])
def weightpost():
    if request.method == "POST":
        direction = request.form.get("direction")
        truck = request.form.get("truck")
        containers = request.form.get("containers")
        weight = request.form.get("weight")
        unit = request.form.get("unit")
        force = request.form.get("force")
        produce = request.form.get("produce")
        sid = dbconnection.run_sql_command(f'SELECT COUNT(*) AS row_count FROM transactions;')
        data = {
        #more eff
        'sessionid':int(sid[0][0])+1,
        'direction': direction.upper() if direction.upper() in ('IN', 'OUT') else 'None', 
        'truck': truck, 
        'containers': str(containers), 
        'weight': int(weight), 
        'unit': unit if unit in ('kg', 'lbs') else 'None',
        'force': force.title(), 
        'produce': produce if produce else "na",
        'time':int(datetime.now().strftime('%Y%m%d%H%M%S'))}
        
        if data["direction"] == "IN":
            dbconnection.run_inset_query(fr'INSERT INTO transactions (datetime,direction,truck,containers,bruto,produce) VALUES ({data["time"]},"{data["direction"]}","{data["truck"]}","{data["containers"]}",{data["weight"]},"{data["produce"]}");')
            dbconnection.run_inset_query(fr'INSERT INTO transactions (datetime,direction,truck,containers,bruto,produce) VALUES ({data["time"]},"OUT","{data["truck"]}","{data["containers"]}",{data["weight"]},"{data["produce"]}");')

        allrows = dbconnection.run_sql_command('select * from transactions;')
        [print(i) for i in allrows]
        alltid = [i for i in allrows if i[3] == truck]
        
        if alltid[-1][2] == data["direction"]:
            if data["force"] == "False":
                print(f"Error: {allrows[-1][2]} followed by {data['direction']}")
            else:
                dbconnection.run_sql_command(f'UPDATE transactions SET bruto = {data["weight"]} WHERE id = {alltid[-1][0]};')
                
        tracktara = 5
        neto = 5
        if data["direction"] == "OUT":
            dbconnection.run_inset_query(fr'INSERT INTO transactions (id,datetime,direction,truck,containers,bruto,truckTara,neto,produce) VALUES ({data["sessionid"]},{data["time"]},"{data["direction"]}","{data["truck"]}","{data["containers"]}",{data["weight"]},{tracktara},{neto},"{data["produce"]}");')

        
        # if data["direction"] == "OUT" and truckidlist[-1][6] == "None":
        #     print('out followed by None')
        # #print(dbconnection.run_sql_command('select * from transactions;'))
        # print(truckidlist[-1])
        return "allrows"
        
#Get Weight return json of the last time according to a time zone
#need to improve so it works with time
#need to improve the Filt so it works with all options
@app.route("/weight", methods=["GET"])
def weightget():
    date = request.args.get("from")
    hour = request.args.get("to")
    filt = request.args.get("filter")
    
    #geting the values from the database
    id1 = dbconnection.run_sql_command("select id from transactions")
    print(filt)
    if filt is None:
        query = dbconnection.run_sql_command("select * from transactions")
    elif "in" in filt:
        query = dbconnection.run_sql_command("select * from transactions where direction = in")
    elif filt == "out":
        query = dbconnection.run_sql_command("select * from transactions where direction = out")

    item_list = []
    single_item = {}
    for item in query:
        # tracklist.append(item[3])
        single_item.update({
            "id":item[0],
            "direction":item[1],
            "bruto":item[2],
            "neto":item[3],
            "produce":item[4],
            "containers":item[5]
        })
        item_list.append(single_item)
    return item_list


#Possible to add select 1 and by that return ok
@app.route("/health")
def health():
    return "OK\n"



#starting of implemanation
#Shamir work
@app.route("/item/<id>", methods=["GET"])
def get_item(id):

    #Parsing Args
    id_input = id
    from_arg = request.args.get("from")
    to_arg = request.args.get("to")
    
    #Args are Ok for easy development


    #Query the Db for this is ID
    #track_Tara = dbconnection.run_sql_command(f"select truckTara from transactions where id={id_input}")
    

    return f"{id_input}:{from_arg}{to_arg}"




###############################################################################################
# GET /session/<id>
# - id is for a weighing session. 404 will be returned if non-existent
# Returns a json:
#  { "id": <str>,
#    "truck": <truck-id> or "na",
#    "bruto": <int>,
#    ONLY for OUT:
#    "truckTara": <int>,
#    "neto": <int> or "na" // na if some of containers unknown
#  }
# GET /session/<id>

#Missons:
# Return without tuples (only the string in the dictonary )
@app.route("/session/<id>", methods=["GET"])
def get_session(id):

    return_dict = {}
    #Check for id in the db IF not return 404
    # dbconnection.run_sql_command(f"select id from transactions where id={id}")
    res = dbconnection.run_sql_command(f"select id from transactions where id={id}")
    if res == []:
        return abort(404)


    ##values for the json
    truck_id = dbconnection.run_sql_command(f"select truck from transactions where id={id}")
    bruto = dbconnection.run_sql_command(f"select bruto from transactions where id={id}")

    #Check for in and out
    state = dbconnection.run_sql_command(f"select direction from transactions where id={id}")
    print(f"{truck_id} {bruto} {state}")
    return_dict.update({
        "id":f"{id}",
        "truck":f"{truck_id}",
        "bruto":f"{bruto}"
    })

    print(state)
    #format state
    if "out" in state:
        #should add more values to the json tracktar,neto
        track_tara = dbconnection.run_sql_command(f"select truckTara from transactions where id={id}")
        neto = dbconnection.run_sql_command(f"select neto from transactions where id={id}")
        return_dict.update({
            "truckTara":track_tara,
            "neto":neto
        })

    print(f"{truck_id}{bruto}")


    return json.dumps(return_dict)

# GET /unknown
# Returns a list of all recorded containers that have unknown weight:
# ["id1","id2",...]
@app.route("/unknown")
def return_unkown_containers():
    containers = dbconnection.run_sql_command("select * from containers_registered")
    list_of_unkown = []
    for item in containers:
        if item[1] == None:
            list_of_unkown.append(item[0])
    print(list_of_unkown)


    return list_of_unkown





if __name__ == "__main__":
    app.run(debug=True)


    