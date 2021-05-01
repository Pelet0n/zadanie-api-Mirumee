import requests
import sqlite3
import csv
import sys

class Error(Exception):
    pass


con = sqlite3.connect('dane.db')
cur = con.cursor()

try:
    cur.execute('''CREATE TABLE dane
                    (flight_number, mission_name,rocket_id,rocket_name, launch_date_utc, video_link)''')
except:
    print('Tabela już istnieje!')


def fetch_data_spacex(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Nie udało się połączyć z serwerem")
    return response.json()


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

for row in fetch_data_spacex('https://api.pacexdata.com/v3/launches'):
   
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
        