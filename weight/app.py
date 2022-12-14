from flask import Flask, request, abort
from datetime import datetime, date
import datetime
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
@app.route("/weight", methods=["GET"])
def weightget():
    #ARGS PARSE from url
    #Time Looks like yyyymmddhhmmss
    
    date_start = request.args.get("from")
    date_end = request.args.get("to")
    #filter
    filt = request.args.get("filter")

    #Getting the date from the args
    if date_start is not None:
        timestamp = str(date_start)
        timestamp = timestamp.zfill(14)
        # Create a datetime object from the timestamp
        date_start = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S')
        date_start = date_start.strftime('%Y-%m-%d %H:%M:%S')

    if date_end is not None:
        timestamp_end = str(date_end)
        timestamp_end = timestamp_end.zfill(14)
        date_end = datetime.datetime.strptime(timestamp_end, '%Y%m%d%H%M%S')
        date_end = date_end.strftime('%Y-%m-%d %H:%M:%S')

    if date_start is None:
        #give value of 0000 and the date of today
        tmp1 = str(date.today())
        date_start = tmp1+" 00:00:00"

    if date_end is None:
        #value of now:
        current_time = datetime.datetime.now()
        date_end = current_time.strftime("%Y-%m-%d %H:%M:%S")

    #Adjust the query according to the filter
    if filt is None:
        query = dbconnection.run_sql_command(fr"select * from transactions where datetime >= '{date_start}' AND datetime <= '{date_end}';")
    else:
        times = fr"AND datetime >= '{date_start}' AND datetime <= '{date_end}'"
        query = []
        filter_all = filt.split(',')
        if "in" in filter_all:
            query += dbconnection.run_sql_command(f"select * from transactions where direction = 'in' {times}")
        if "out" in filter_all:
            query += dbconnection.run_sql_command(f"select * from transactions where direction = 'out' {times}")
        if "none" in filter_all:
            query += dbconnection.run_sql_command(f"select * from transactions where direction = 'none' {times}")

    item_list = []
    single_item = {}
   #PUTTING RESOLT INTO A LIST
    query = [i for i in query]
    

    for item in query:

        single_item = {
            "id":item[0],
            "direction":item[3],
            "bruto":item[4],
            "neto":item[5],
            "produce":item[6],
            "containers":item[7]
        }
        item_list.append(single_item)
   
    return item_list


#Possible to add select 1 and by that return ok
@app.route("/health")
def health():
    res = dbconnection.health()
    if res == '1':
        return "OK\n"
    else:
        return '0'



#starting of implemanation
#Shamir work
@app.route("/item/<id>", methods=["GET"])
def get_item(id):

    #Parsing Args From Function
    id_input = str(id)
    from_arg = request.args.get("from")
    to_arg = request.args.get("to")

    # ####DATA FOR TEST
    # dbconnection.run_inset_query("DELETE FROM transactions")
    # dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1225025', '12323', '2022-12-23 14:02:03', 'out', '123', '5423', '432', '542', '433', '431')")
    # dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1225024', '12323', '2022-12-23 14:02:03', 'out', '123', '5423', '432', '542', '433', '431')")
    # dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('122', '12323', '2022-11-23 14:02:03', 'out', '123', '5423', '432', '542', '433', '431')")
    # dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1225029', '12323', '2022-12-05 00:00:00', 'out', '123', '5423', '432', '542', '433', '431')")
    # dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('122502', '12323', '2022-12-13 13:02:03', 'out', '123', '5423', '432', '542', '433', '431')")
    # dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('12250', '12323', '2022-12-14 01:02:03', 'out', '123', '5423', '432', '542', '433', '431')")
    # dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1225', '12323', '2022-12-14 06:06:03', 'out', '123', '5423', '432', '542', '433', '431')")

    # ###########

    #Check The ID in the data base And Return 404 is non exeists 
    if id_input.startswith('T') or id_input.startswith('K'):
        isTruck = True
        checkID = dbconnection.run_sql_command(fr"select sessionid from transactions where truck = '{id_input}'")
        checkID = [i for i in checkID]
        if len(checkID) == 0:
            return abort(404)
    elif id_input.startswith('C'):
        isTruck = False
        checkID = dbconnection.run_sql_command(fr"select sessionid from transactions where containers = '{id_input}'")
        checkID = [i for i in checkID]
        if len(checkID) == 0:
            return abort(404)
    else:
        return "<h2>you must enter an id of a truch or container<h2>"
    

    #IN THIS Point We Got ID THAT IS VALID
    #ARG PARSING
    if from_arg is None and to_arg is None:
        tmp1 = str(date.today())
        date1 = tmp1+" 00:00:00"
        tmp2 = str(datetime.now())
        tmp2 = tmp2.split(".")
        date2 = tmp2[0]
    elif to_arg is None and from_arg is not None:
        tmp1 = str(from_arg)
        tmp1 = tmp1.zfill(14)
        
        date1 = datetime.strptime(tmp1, '%Y%m%d%H%M%S')
        date1 = date1.strftime('%Y-%m-%d %H:%M:%S')
        
        tmp2 = str(datetime.now())
        tmp2 = tmp2.split(".")
        date2 = tmp2[0]
    elif from_arg is None and to_arg is not None:
        return "no such option"
    else:
        tmp1 = str(from_arg)
        tmp1 = tmp1.zfill(14)
        date1 = datetime.strptime(tmp1, '%Y%m%d%H%M%S')
        date1 = date1.strftime('%Y-%m-%d %H:%M:%S')

        tmp2 = str(to_arg)
        tmp2 = tmp2.zfill(14)
        date2 = datetime.strptime(tmp2, '%Y%m%d%H%M%S')
        date2 = date2.strftime('%Y-%m-%d %H:%M:%S')
    

    #check if i got an container id or an truck id
    if isTruck:
        #doing the query
        query = dbconnection.run_sql_command(fr"select id, truckTara, sessionid from transactions where datetime >= '{date1}' and datetime <= '{date2}' and truck = '{id_input}'")
        
    else:
        checkifNone = dbconnection.run_sql_command(fr"select truck from transactions where containers = '{id_input}'")
        #checking if the container has history or not
        checkifNone = [i for i in checkifNone]
        if checkifNone[0][0] is None:
            query = dbconnection.run_sql_command(fr"select id, sessionid from transactions where datetime >= '{date1}' and datetime <= '{date2}' and containers = '{id_input}'")
            item_list = []
            single_item = {}
            for item in query:
                single_item = {
                    "id":item[0],
                    "tara":"na",
                    "sessionid":item[1]
                }
                item_list.append(single_item)
            return item_list
        else:
            #query the container
            query = dbconnection.run_sql_command(fr"select id, truckTara, sessionid from transactions where datetime >= '{date1}' and datetime <= '{date2}' and containers = '{id_input}'")
    #creating the json
    query = [i for i in query]
    if len(query) == 0:
        return "no data"
    item_list = []
    single_item = {}
    for item in query:
        single_item = {
            "id":item[0],
            "tara":item[1],
            "sessionid":item[2]
        }
        item_list.append(single_item)
    return item_list


#Return information about a Session Number
@app.route("/session/<id>", methods=["GET"])
def get_session(id):
    alldata = dbconnection.run_sql_command(f"select * from transactions where sessionid={id}")
    listdata = [i for i in alldata]
    print (listdata)
    # dict_out = {}
    if len(listdata) == 0:
        return abort(404)

    if listdata[-1][3] == 'out':
          dict_out = {"id":id , "truck":listdata[-1][4] , "bruto":listdata[0][6],"tara":listdata[-1][7],"neto":listdata[-1][8]}
    elif listdata[0][3] == 'in':
           dict_out = {"id":id , "truck":listdata[0][4] , "bruto":listdata[0][6]}
    else: 
          dict_out = {"id":id ,"truck":"N/A" ,"container":listdata[0][5] , "neto":listdata[0][8]}
         
    return dict_out

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
    app.run(host='0.0.0.0')


    