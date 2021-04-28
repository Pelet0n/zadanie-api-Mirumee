import requests
import sqlite3
import csv
import sys

con = sqlite3.connect('dane.db')
cur = con.cursor()

try:
    cur.execute('''CREATE TABLE dane
                    (flight_number, mission_name,rocket_id,rocket_name, launch_date_utc, video_link)''')
except:
    print('Tabela już istnieje!')


response_json = requests.get('https://api.spacexdata.com/v3/launches').json()

def check_database():
    sql = 'SELECT * FROM dane'
    for row in cur.execute(sql):
        if(row):
            return True

if(check_database() == True):
    print('Dane już zostały dodane')
    for row in cur.execute("SELECT * FROM dane"):
        print(row)
    sys.exit()

for row in response_json:
   
   sql = f"INSERT INTO dane VALUES('{row['flight_number']}','{row['mission_name']}','{row['rocket']['rocket_id']}','{row['rocket']['rocket_name']}','{row['launch_date_utc']}','{row['links']['video_link']}')"

   cur.execute(sql) 

   with open('dane.csv','a+',newline='') as csvfile:
        napisz = csv.writer(csvfile)
        dane = [{'flight_number':row['flight_number'],'mission_name': row['mission_name'], 'rocket_id':row['rocket']['rocket_id'],'rocket_name':row['rocket']['rocket_name'],'launch_date_utc':row['launch_date_utc'],'video_link':row['links']['video_link']}]
        napisz.writerow(dane)


for row in cur.execute("SELECT * FROM dane"):
    print(row)


con.commit()   

con.close()
        