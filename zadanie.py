import requests
import sqlite3
import csv
import sys


def connect_db():
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    try:
        cur.execute('''CREATE TABLE data
                        (flight_number, mission_name,rocket_id,rocket_name, launch_date_utc, video_link, UNIQUE(flight_number,mission_name,rocket_id,rocket_name,launch_date_utc,video_link) ON CONFLICT IGNORE)''')
    except:
        print('Table data already exists')
    return cur,con

def fetch_data_spacex(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error \n{e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error \n{e}",)
    except requests.exceptions.Timeout as e:
        print(f"Timeout error \n{e}v")
    except requests.exceptions.RequestException as e:
        print(f"Something else is wrong \n{e}")
    
cur,con = connect_db()

response = fetch_data_spacex('https://api.spacexdata.com/v3/launches')

if(not response):
    sys.exit()

for row in response:
   
   sql = f"REPLACE INTO data VALUES('{row['flight_number']}','{row['mission_name']}','{row['rocket']['rocket_id']}','{row['rocket']['rocket_name']}','{row['launch_date_utc']}','{row['links']['video_link']}')"
   cur.execute(sql) 

   with open('data.csv','a+',newline='') as csvfile:
        napisz = csv.writer(csvfile)
        dane = [{'flight_number':row['flight_number'],'mission_name': row['mission_name'], 'rocket_id':row['rocket']['rocket_id'],'rocket_name':row['rocket']['rocket_name'],'launch_date_utc':row['launch_date_utc'],'video_link':row['links']['video_link']}]
        napisz.writerow(dane)


for row in cur.execute("SELECT * FROM data"):
    print(row)


con.commit()   

con.close()      