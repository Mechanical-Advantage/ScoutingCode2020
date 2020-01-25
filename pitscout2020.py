import csv
import sqlite3 as sql
from fpdf import FPDF
pdf = FPDF()
conn1 = sql.connect("c:\coding\AdvantageScout\global.db")
cur1 = conn1.cursor()
cur1.execute("SELECT value FROM config WHERE key = 'event'")
Event = cur1.fetchall()[0][0]
conn = sql.connect("data_2020.db")
cur = conn.cursor()
#event_name
cur.execute("SELECT * FROM pit WHERE Event = ? order by Team",(Event,))
Pitscout = cur.fetchall()
name_lookup = {
    10: {    
        "section": "auto",
        "value": "can move from initiation line"
    },
    12: {
        "section": "auto",
        "value": "can deliver upper"
    },
    13: {
        "section": "auto",
        "value": "can deliver lower"
    },
    14: {
        "section": "shoot_to",
        "value": "upper goal"
    },
    15: {
        "section": "shoot_to",
        "value": "lower goal"
    },
    16: {
        "section": "wheel",
        "value": "can do rotation control"
    },
    17: {
        "section": "wheel",
        "value": "can do position control"
    },
    20: {
        "section": "shoot_from",
        "value": "wall"
    },
    21: {
        "section": "shoot_from",
        "value": "opponent side"
    },
    22: {
        "section": "shoot_from",
        "value": "own side"
    }
}
# THE LOOKUP
# if row[column] == 1:
#     lists[name_lookup[column]["section"]].append(name_lookup[column]["value"])
#
# THE JOIN
# ", ".join(lists[list_name])

for row in Pitscout:
    lists = {
        "auto": [],
        "shoot_to": [],
        "shoot_from": [],
        "wheel": []
    }
    for column in name_lookup.keys():
        if row[column] == 1:
            lists[name_lookup[column]["section"]].append(name_lookup[column]["value"])
    if row[18] == 0:
        canliftoutput = "No"
    else:
        canliftoutput = "Yes"
    if row[22] == 0:
        multipledriveteamoutput = "No"
    else:
        multipledriveteamoutput = "Yes"

    pdf.add_page()
    pdf.set_font('Arial', 'B', 30)
    pdf.cell(40, 10, 'Team ' + str(row[1]), ln=1)
    pdf.set_font('Arial', '', 14)
    pdf.cell(40, 10, 'Drive Train: ' + row[7], ln=1)
    pdf.cell(40, 10, 'Weight: ' + str(row[8]))
    pdf.cell(40, 10, 'Height: ' + str(row[9]), ln = 1)
    pdf.cell(40, 10, 'Max Reach: ' + str(row[17])) 
    pdf.cell(50, 10, 'Can Lift Others: ' + canliftoutput)
    pdf.cell(40, 10, 'Multiple Drive Teams: ' + multipledriveteamoutput, ln=1)
    pdf.cell(40, 10, 'Auto Delay/How?: ' + row[11], ln=1)
    pdf.cell(40, 10, 'Auto Capabilities: ' + ", ".join(lists["auto"]),  ln = 1)
    pdf.cell(40, 10, 'Shooting Capabilities: ' + ", ".join(lists["shoot_to"]),  ln = 1)
    pdf.cell(40, 10, 'Shooting Positions: ' + ", ".join(lists["shoot_from"]),  ln = 1)
    pdf.cell(40, 10, 'Wheel Capabilities: ' + ", ".join(lists["wheel"]),  ln = 1)
    pdf.cell(40, 10, 'Comments: ' + str(row[24]), ln=1)
    


    if len(row[25]) >= 1:
        pdf.image("c:\coding\\AdvantageScout\\" + row[25], 10,120, 125)
pdf.output('pitscout.pdf', 'F')
conn.close()    
conn1.close()