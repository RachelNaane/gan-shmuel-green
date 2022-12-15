from flask import Flask, request, abort, jsonify
from datetime import datetime, date
import datetime
from db import dbconnection
import json, re,csv,os



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
        'produce': produce if produce else "n/a",
        'time':int(datetime.now().strftime('%Y%m%d%H%M%S'))}


        allrows = dbconnection.run_sql_command('select * from transactions;')
        alltid = [i for i in allrows if i[4] == truck]

        if not alltid:
            alltid = ["id", data["sessionid"], data["time"], data["direction"], data["truck"], data["containers"], 20, None, None, 'apples']




        if data["direction"] == "None":


            resdict = dbconnection.run_sql_command(fr"SELECT * FROM containers_registered WHERE container_id = '{data['containers']}';")


            if resdict:
                dbconnection.run_inset_query(fr'INSERT INTO transactions (sessionid,datetime,direction,containers,bruto,produce) VALUES ({data["sessionid"]},{data["time"]},"{data["direction"]}","{data["containers"]}",{int(resdict[0][1])},"{data["produce"]}");')
                resdict = { "id":data["sessionid"], "containers": data["containers"],"bruto":resdict[0][1]}


            else:
                
                dbconnection.run_inset_query(fr'INSERT INTO transactions (sessionid,datetime,direction,containers,bruto,produce) VALUES ({data["sessionid"]},{data["time"]},"{data["direction"]}","{data["containers"]}",{data["weight"]},"{data["produce"]}");')
                resdict = { "id":data["sessionid"], "containers": data["containers"],"bruto":data["weight"]}

            return resdict


        elif data["direction"] == alltid[-1][3] and len(alltid) > 0:
            if data["force"] == "False":
                return f"Error: {allrows[-1][3]} followed by {data['direction']}"

            elif data["force"] == "True":


                dbconnection.run_sql_command(f'DELETE FROM transactions WHERE id = {alltid[-1][0]} ;')
                
                if alltid[-1][3] == "OUT":


                    

                    dbconnection.run_inset_query(fr'INSERT INTO transactions (sessionid,datetime,direction,truck,containers,truckTara,neto,produce) VALUES ({alltid[-1][1]},{data["time"]},"{data["direction"]}","{data["truck"]}","{data["containers"]}",{data["weight"]},{neto},"{data["produce"]}");')
                    [print(i) for i in dbconnection.run_sql_command('select * from transactions;')]

                    resdict = { "id":alltid[-1][1], "truck":data["truck"],"bruto":data["weight"]}
                    return resdict


                else:
                    dbconnection.run_inset_query(fr'INSERT INTO transactions (sessionid,datetime,direction,truck,containers,bruto,produce) VALUES ({alltid[-1][1]},{data["time"]},"{data["direction"]}","{data["truck"]}","{data["containers"]}",{data["weight"]},"{data["produce"]}");')
                    [print(i) for i in dbconnection.run_sql_command('select * from transactions;')]
                    #resdict = { "id":data["sessionid"], "containers": data["containers"],"bruto":data["weight"]}
                    #return resdict


                #resdict = { "id":data["sessionid"], "truck": data["truck"],"neto":alltid[-1][6]-data["weight"]}
                #return resdict


        elif data["direction"] == "IN":
            dbconnection.run_inset_query(fr'INSERT INTO transactions (sessionid,datetime,direction,truck,containers,bruto,produce) VALUES ({data["sessionid"]},{data["time"]},"{data["direction"]}","{data["truck"]}","{data["containers"]}",{data["weight"]},"{data["produce"]}");')

        elif data["direction"] == "OUT":

            
            conts = alltid[-1][5]
            conts = conts.split(",")

            sumc = 0
            for i in conts:
                contweight = dbconnection.run_sql_command(fr"SELECT weight FROM containers_registered WHERE container_id = '{i}';")

                sumc += int(contweight[0][0])

            neto = alltid[-1][6]-data["weight"] -sumc
            dbconnection.run_inset_query(fr'INSERT INTO transactions (sessionid,datetime,direction,truck,truckTara,neto,produce) VALUES ({alltid[-1][1]},{data["time"]},"{data["direction"]}","{data["truck"]}",{data["weight"]},{neto},"{data["produce"]}");')


        #[print(i) for i in dbconnection.run_sql_command('select * from transactions;')]
        


        return "\nOK"
        

"""
return a list of json object containing the following information:
id, direction, bruto, neto, produce, containers.
This information Goes to the billing team in order for them to keep in track with the supply.
"""
@app.route("/weight", methods=["GET"])
def weightget():

    #Parsing Query Parameters From the url
    date_start = request.args.get("t1")
    date_end = request.args.get("t2")
    filt = request.args.get("filter")

    #Checking If Query Parameter for the date was given and if so format it to the Y-%m-%d %H:%M:%S Format (2001-04-11 14:0:0)
    if date_start is not None:
        timestamp = pad_with_zeros(date_start)
        date_start = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S')
        date_start = date_start.strftime('%Y-%m-%d %H:%M:%S')

    if date_end is not None:
        timestamp_end = pad_with_zeros(date_end)
        date_end = datetime.datetime.strptime(timestamp_end, '%Y%m%d%H%M%S')
        date_end = date_end.strftime('%Y-%m-%d %H:%M:%S')

    if date_start is None:
        #Give value of 0000 and the date of today
        tmp1 = str(date.today())
        date_start = tmp1+" 00:00:00"

    if date_end is None:
        #Value of Now
        current_time = datetime.datetime.now()
        date_end = current_time.strftime("%Y-%m-%d %H:%M:%S")

    
    #Basic qurey for DB to
    basic_query = fr"SELECT id, direction, bruto, neto, produce, containers, truckTara, truck FROM transactions"

    #Adjust the query according to the filter
    if filt is None:
        query = dbconnection.run_sql_command(fr"{basic_query} where datetime >= '{date_start}' AND datetime <= '{date_end}';")
    else:
        times = fr"AND datetime >= '{date_start}' AND datetime <= '{date_end}'"
        query = []
        filter_all = filt.split(',')
        if "in" in filter_all:
            query += dbconnection.run_sql_command(f"{basic_query} where direction = 'in' {times}")
        if "out" in filter_all:
            query += dbconnection.run_sql_command(f"{basic_query} where direction = 'out' {times}")
        if "none" in filter_all:
            query += dbconnection.run_sql_command(f"{basic_query} where direction = 'none' {times}")
    
    #The sql query result in one big list with each result in a tuple so we need to fetch them out
    query = [i for i in query]
    print(query)

    item_list = []
    single_item = {}
    
    #Formating the items from the query to a diconary
    #id[[0]] direction[[1]] bruto[2] neto[[3]] produce[[4]] continers[5]
    for item in query:
        #getting list of containers
        if item[5] is not None:
            conteiners = item[5].split(',')
        else:
            containers=""
        ##Checking for containers with unkown tara
        neto = ""
        if item[6] is None:
            neto = "N/A"
        else:
            neto = item[3]     

        #Creation of the diconarary
        #Id is the ID of a truck
        single_item = {
            "id":item[7],
            "direction":item[1],
            "bruto":item[2],
            "neto":neto,
            "produce":item[4],
            "containers":conteiners
        }
        item_list.append(single_item)

    return jsonify(item_list)

@app.route("/batch", methods=["POST"])
def batch():
    if request.method == "POST":
        filename = request.form.get("filename")
        fext = os.path.splitext(filename)[1]
        passw = request.form.get("pass")
        if passw != 'pass123':
            return "\nWrong Password\n"


        with open(f'in/{filename}','r') as file:

            if fext == '.csv':
                reader = csv.reader(file)
                valist = list(reader)
                unit = valist[0][1]
                valist.pop(0)
        
            elif fext == '.json':
                data = json.load(file)
                valist = []
                for item in data:
                    valist.append((item['id'], item['weight'], item['unit']))

                unit = valist[0][2]


        allcid = dbconnection.run_sql_command(f'SELECT container_id FROM containers_registered;')
        allcid = [i[0] for i in allcid]
        

        for i in valist:
            if i[0] in allcid:
                dbconnection.run_inset_query(f"UPDATE containers_registered SET weight = {int(i[1])}, unit = '{unit}' WHERE container_id = '{i[0]}'")

            else:
                dbconnection.run_inset_query(f"INSERT INTO containers_registered (container_id,weight,unit) VALUES ('{i[0]}',{int(i[1])},'{unit}')")
            

        return 'OK'




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
    id_input = str(id_input)
    from_arg = request.args.get("from")
    to_arg = request.args.get("to")

    #checking if id is exist
    if id_input.startswith('T'):
        isTruck = True
        checkID = dbconnection.run_sql_command(fr"select sessionid from transactions where truck = '{id_input}'")
        checkID = [i for i in checkID]
        if len(checkID) == 0:
            return abort(404)
    elif id_input.startswith('C') or id_input.startswith('K'):
        isTruck = False
        checkID = dbconnection.run_sql_command(fr"select sessionid from transactions where containers like '%{id_input}%'")
        checkID = [i for i in checkID]
        if len(checkID) == 0:
            return abort(404)
    else:
        return "you must enter an id of a truch or container"
    

    #checking how many arguments I got and creating the dates for the query!
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
    sessions = []
    if isTruck:
        #doing the query
        temp = dbconnection.run_sql_command(fr"select distinct sessionid from transactions where datetime >= '{date1}' and datetime <= '{date2}' and truck = '{id_input}'")
        
        for item in temp:
            sessions.append(item[0])

        temp = dbconnection.run_sql_command(fr"select truckTara from transactions where sessionid = '{sessions[-1]}' and direction = 'out'")
        tara = temp[0][0]
    else:
        checkifNone = dbconnection.run_sql_command(fr"select truck from transactions where containers like '%{id_input}%'")
        #checking if the container has history or not
        # checkifNone = [i for i in checkifNone]
        if checkifNone[0][0] is None:
            temp = dbconnection.run_sql_command(fr"select distinct sessionid from transactions where datetime >= '{date1}' and datetime <= '{date2}' and containers like '%{id_input}%'")
            for item in temp:
                sessions.append(item[0])
            result = {
                "id": id_input,
                "tara": "na",
                "sessions": sessions
            }
            return jsonify(result)

        else:

            temp = dbconnection.run_sql_command(fr"select distinct sessionid from transactions where datetime >= '{date1}' and datetime <= '{date2}' and containers like '%{id_input}%'")
        
            for item in temp:
                sessions.append(item[0])
                print(item)
            print(sessions)
            temp = dbconnection.run_sql_command(fr"select truckTara from transactions where sessionid = '{sessions[-1]}' and direction = 'out'")
            tara = temp[0][0]
    #creating the json
    result = {
        "id": id_input,
        "tara": tara,
        "sessions": sessions
    }
    return jsonify(result)


#Return information about a Session Number, IN OUT of a truck, or a stand alone container
@app.route("/session/<id>", methods=["GET"])
def get_session(id):
    query = "select id, truck, bruto, truckTara, neto, direction, containers from transactions"
    alldata = dbconnection.run_sql_command(f"{query} where sessionid={id}")
    listdata = [i for i in alldata]
    # print(listdata)
    if len(listdata) == 0:
        return abort(404)
    if listdata[-1][5] == 'out':
          dict_out = {"id":str(listdata[0][0]) , "truck":listdata[0][1] , "bruto":listdata[0][2],"tara":listdata[-1][3],"neto":listdata[-1][4]}
    elif listdata[0][5] == 'in':
           dict_out = {"id":str(listdata[0][0]) , "truck":listdata[0][1] , "bruto":listdata[0][2]}
    else: 
          dict_out = {"id":str(listdata[0][0]) ,"truck":"N/A" ,"container":listdata[0][6] , "neto":listdata[0][8]}
         
    return jsonify(dict_out)

# Returns a list of all recorded containers that have unknown weight:
# ["id1","id2",...]
@app.route("/unknown")
def return_unkown_containers():
    containers = dbconnection.run_sql_command("select * from containers_registered")
    list_of_unkown = []
    for item in containers:
        if item[1] == None:
            list_of_unkown.append(item[0])
    return list_of_unkown

#This function help to be flexible with the way we get dates
def pad_with_zeros(num):
    num_str = str(num)
    num_zeros = 14 - len(num_str) 
    if num_zeros > 0:
        return num_str + "0" * num_zeros
    else:
        return num_str



if __name__ == "__main__":
    app.run(host='0.0.0.0')


    
