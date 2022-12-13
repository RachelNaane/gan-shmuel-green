import mysql.connector

#Creating the connection and the cursor to the mysql data base
def db_connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
    #mysql container ip 
    host="localhost",
    user="root",
    password="password"
    )   
    cursor = cnx.cursor()
    
#Creates the initial database table - Should run only once
def DB_INITIALIZATION():
    db_connect()
    with open('weightdb.sql','r') as f:
        sql_command = f.read()
    cursor.execute(sql_command,multi=True)
    print(" If this is the only message you see while running this file: Data Base is connected and runing")
    cnx.commit()
    cnx.close()
    

def check_table_existence(table_name):
    
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    if cursor.fetchone():
        return True
    else:
        return False



def insert_message_to_table(table_name,message):
    cursor.execute("USE weight;")
    cursor.execute(f"INSERT INTO {table_name} (message) VALUES ('{message}');")


#return all the data from the mysql from a specific room
def get_messages(room_name):
    #check if the room(table) exists: 
    db_connect() 
    if check_table_existence(room_name):
        print("Table exists Returns message:")
        cursor.execute(f"SELECT * from {room_name};")
        results = cursor.fetchall()
        string_fromdb = ""
        for result in results:
            message = result[1]
            string_fromdb += f"Message: {message}\n"
        print(string_fromdb)
        return string_fromdb
    else:
        return 'No Chat Yet - You Welcome To send The First Message'
    cnx.commit()
    cnx.close()


def post_message(room_name,message):
    db_connect()
    if check_table_existence(room_name):
        #insert Data to the DB
        insert_message_to_table(room_name,message)
    else:
        #Create Table and then insert data to the DB
        cursor.execute(f"CREATE TABLE {room_name} (id INT AUTO_INCREMENT PRIMARY KEY,message TEXT);")
        insert_message_to_table(room_name,message)
    cnx.commit()
    cnx.close()

#Run query on the DB
def run_sql_command(command):
    db_connect()
    cursor.execute("USE weight;")
    cursor.execute(command)

    results = cursor.fetchall()
    
    result_str = ""

    for row in results:
        result_str += str(row)
    
    cnx.commit()
    cnx.close()
    return result_str

#TO INSERT DATA to the DB
def run_inset_query(command):
    db_connect()
    cursor.execute("USE weight;")
    cursor.execute(command)
    cnx.commit()
    cnx.close()





#Initialized the data base creates the basic tables
if __name__ == "__main__":
    DB_INITIALIZATION()

