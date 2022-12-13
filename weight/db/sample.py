import mysql.connector
import dbconnection

dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1825025', '12323', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1925025', '12323', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1125025', '12323', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1025025', '12323', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
dbconnection.run_inset_query(fr"INSERT INTO transactions (id, sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1225025', '12323', '2022-11-11', 'out', '123', '5423', '432', '542', '433', '431')")




dbconnection.run_inset_query(fr"INSERT INTO containers_registered (container_id, weight, unit) VALUES ('C-35334', '296', 'kg');")
dbconnection.run_inset_query(fr"INSERT INTO containers_registered (container_id, unit) VALUES ('C-23134', 'kg');")
dbconnection.run_inset_query(fr"INSERT INTO containers_registered (container_id, unit) VALUES ('C-28884', 'kg');")




print(dbconnection.run_sql_command("select * from containers_registered"))

query = "select * from transactions"