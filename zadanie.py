import requests
import sqlite3

con = sqlite3.connect('dane.db')
cur = con.cursor()

try:
    cur.execute('''CREATE TABLE dane
                    (flight_number, mission_name,rocket_id,rocket_name, launch_date_utc, video_link)''')
except:
    print('Tabela już istnieje!')


response_json = requests.get('https://api.spacexdata.com/v3/launches').json()

for row in response_json:
   sql = f"INSERT INTO dane VALUES('{row['flight_number']}','{row['mission_name']}','{row['rocket']['rocket_id']}','{row['rocket']['rocket_name']}','{row['launch_date_utc']}','{row['links']['video_link']}')"

   cur.execute(sql) 

   
con.commit()   

con.close()
        