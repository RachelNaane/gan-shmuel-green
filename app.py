from flask import Flask, request, abort
from db import dbconnection
import json



app = Flask(__name__)


#This is the Post Mehthod Implemented by yossi
@app.route("/weight", methods=["POST"])
def weightpost():
        return data


#Noams
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
    
    # print(query)
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
    


@app.route("/health")
def health():
    return "OK\n"




##Day 2 

# ?from=t1&to=t2


# GET /item/<id>?from=t1&to=t2
# - id is for an item (truck or container). 404 will be returned if non-existent
# - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
# default t1 is "1st of month at 000000". default t2 is "now".
# Returns a json:
# { "id": <str>,
#   "tara": <int> OR "na", // for a truck this is the "last known tara"
#   "sessions": [ <id1>,...]
# }


#starting of implemanation
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
@app.route("/session/<id>", methods=["GET"])
def get_session(id):

    return_dict = {}
    #Check for id in the db IF not return 404
    print('test')
    dbconnection.run_sql_command(f"select id from transactions where id={id}")
    # try:
    #     dbconnection.run_sql_command(f"select id from transactions where id={id}")
    # except:
    #     return abort(404)
    

    ##values for the json
    truck_id = dbconnection.run_sql_command(f"select truck from transactions where id={id}")
    bruto = dbconnection.run_sql_command(f"select bruto from transactions where id={id}")

    #Check for in and out
    state = dbconnection.run_sql_command(f"select direction from transactions where id={id}")

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



if __name__ == "__main__":
    app.run(debug=True)


    