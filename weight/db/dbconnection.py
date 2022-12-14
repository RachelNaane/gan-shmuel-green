import mysql.connector

#Creating the connection and the cursor to the mysql data base
def db_connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
    #IF IN DEVELOPMENT
    # host=localhost,
    # port = 8082,
    host="weight-app-weaigt-db-1",
    user="root",
    password="password",
    port = 3306
    )   
    cursor = cnx.cursor()
    
#Creates the initial database table - Should run only once
def DB_INITIALIZATION():
    db_connect()
    
    print(" If this is the only message you see while running this file: Data Base is connected and runing")
    # cnx.commit()
    cnx.close()
    

#Run query on the DB
def run_sql_command(command):
    db_connect()
    cursor.execute("USE weight;")
    cursor.execute(command)

    results = cursor.fetchall()
    cnx.commit()
    cnx.close()
    return results

#TO INSERT DATA to the DB
def run_inset_query(command):
    db_connect()
    cursor.execute("USE weight;")
    cursor.execute(command)
    cnx.commit()
    cnx.close()


def health():
    run_sql_command("select 1;")
    try:
        run_sql_command("select 1;")
        print("DB Works and connected")
        return '1'
    except:
        return '0'


#Initialized the data base creates the basic tables
if __name__ == "__main__":
    DB_INITIALIZATION()
    health()

