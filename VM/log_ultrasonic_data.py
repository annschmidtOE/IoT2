import sqlite3
import random
from datetime import datetime
from time import sleep
import paho.mqtt.subscribe as subscribe


print("Subscribe MQTT script running!")


def create_table():
    query = """CREATE TABLE IF NOT EXISTS ultrasonic(datetime TEXT NOT NULL, distance REAL NOT NULL)"""
    try:
        conn = sqlite3.connect("skraldespand.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"sqlite error: {e}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        conn.close()



create_table()


def get_data(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    query = """INSERT INTO ultrasonic(datetime, distance) VALUES (?,?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    distance_data = message.payload.decode()
    distance_list = distance_data.split()
    distance = distance_list[1]
    print(distance)
    data = (now, distance)
    try:
        conn = sqlite3.connect("skraldespand.db")
        cur = conn.cursor()
        cur.execute(query,data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"sqlite3 error: {e}")
        conn.rollback() 
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    sleep(1)
        
subscribe.callback(get_data, "8c/sensor", hostname="13.74.244.39", userdata={"message_count": 0})

