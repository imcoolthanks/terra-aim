import sqlite3 as sql

def create_examples_gyroscope():
    #Create database file/connect to it
    conn = sql.connect("data.db")

    #Create table
    conn.execute("""CREATE TABLE gyroscope (time datetime, yaw float, pitch float) """)

    print("table created")

    conn.close()

def insert_gyroscope_database(currentTime, yaw, pitch):
    conn = sql.connect("data.db")
    cur = conn.cursor()

    #Load all rows
    insert_query = """INSERT INTO gyroscope (time, yaw, pitch) 
                                        VALUES (?,?,?)"""
    cur.execute(insert_query, (currentTime, yaw, pitch))

    #Save changes
    conn.commit()

    conn.close()
    print("Loading completed")

def create_examples_position():
    #Create database file/connect to it
    conn = sql.connect("data.db")

    #Create table
    conn.execute("""CREATE TABLE position (time datetime, dx float, dy float) """)

    print("table created")

    conn.close()

def insert_position_database(currentTime, dx, dy):
    conn = sql.connect("data.db")
    cur = conn.cursor()

    #Load all rows
    insert_query = """INSERT INTO position (time, dx, dy) 
                                        VALUES (?,?,?)"""
    cur.execute(insert_query, (currentTime, dx, dy))

    #Save changes
    conn.commit()

    conn.close()
    print("Loading completed")

# ---- DEBUGGING ---------
def list_gyroscope(): 
    conn = sql.connect("data.db")
    cur = conn.cursor()

    cur.execute("select * from gyroscope")
    
    rows = list(cur.fetchall())

    conn.close()

    return rows

def list_position(): 
    conn = sql.connect("data.db")
    cur = conn.cursor()

    cur.execute("select * from position")
    
    rows = list(cur.fetchall())

    conn.close()

    return rows
# -------------------------


