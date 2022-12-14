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

    #Parsing Args
    id_input = id
    from_arg = request.args.get("from")
    to_arg = request.args.get("to")
    
    #Args are Ok for easy development

    #Query the Db for this is ID
    #track_Tara = dbconnection.run_sql_command(f"select truckTara from transactions where id={id_input}")
    
    return f"{id_input}:{from_arg}{to_arg}"


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


    