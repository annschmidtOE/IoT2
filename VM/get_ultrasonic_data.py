import sqlite3
from random import randint
from datetime import datetime

def get_distance_data(number_of_rows):
    query = """SELECT * FROM ultrasonic ORDER BY datetime DESC;"""
    datetimes = []
    distances = []
    try:
        conn = sqlite3.connect("skraldespand.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            datetimes.append(row[0])
            distances.append(row[1])
        return datetimes, distances
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

get_distance_data(20)
    
