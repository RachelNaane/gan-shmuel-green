import mysql.connector
import dbconnection
# dbconnection.run_inset_query(fr"INSERT INTO transactions (id, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1825025', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
# dbconnection.run_inset_query(fr"INSERT INTO transactions (id, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1925025', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
# dbconnection.run_inset_query(fr"INSERT INTO transactions (id, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1125025', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
# dbconnection.run_inset_query(fr"INSERT INTO transactions (id, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1025025', '2022-11-11', 'in', '123', '5423', '432', '542', '433', '431')")
# dbconnection.run_inset_query(fr"INSERT INTO transactions (id, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1225025', '2022-11-11', 'out', '123', '5423', '432', '542', '433', '431')")
# print(dbconnection.run_sql_command("select * from transactions"))




query = "select * from transactions"