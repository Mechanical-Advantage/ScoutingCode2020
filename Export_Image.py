import shutil
import sqlite3 as sql
conn1 = sql.connect("c:\mascout\AdvantageScout\global.db")
cur1 = conn1.cursor()
cur1.execute("SELECT value FROM config WHERE key = 'event'")
Event = cur1.fetchall()[0][0]
conn = sql.connect("c:\mascout\AdvantageScout\data_2020.db")
cur = conn.cursor()
teams = cur.execute(
    "SELECT DISTINCT Team,Image FROM pit WHERE Event=?", (Event,)).fetchall()

for Team in teams:
    if Team[1] != "":
        new_name = "D:\\Images\\" + Event + "_" + str(Team[0]) + ".jpg"
        shutil.copyfile("c:\\mascout\\AdvantageScout\\" + Team[1], new_name)
conn1.close()
conn.close()
