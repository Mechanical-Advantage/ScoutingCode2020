import csv
import sqlite3 as sql
from fpdf import FPDF
pdf = FPDF()
conn1 = sql.connect("c:\coding\AdvantageScout\global.db")
cur1 = conn1.cursor()
cur1.execute("SELECT value FROM config WHERE key = 'event'")
Event = cur1.fet    chall()[0][0]
conn = sql.connect("data_2020.db")
cur = conn.cursor()
#event_name
cur.execute("SELECT * FROM pit WHERE Event = ? order by Team",(Event,))
Pitscout = cur.fetchall()
name_lookup = {
    8: {
        "section": "auto",
        "value": "can move from initiation line"
    },
    9: {
        "section": "auto",
        "value": "can deliver upper"
    },
    10: {
        "section": "auto",
        "value": "can deliver lower"
    },
    11: {
        "section": "shoot_to",
        "value": "upper goal"
    },
    12: {
        "section": "shoot_to",
        "value": "lower goal"
    },
    13: {
        "section": "wheel",
        "value": "can do rotation control"
    },
    14: {
        "section": "wheel",
        "value": "can do position control"
    },
    17: {
        "section": "shoot_from",
        "value": "wall"
    },
    18: {
        "section": "shoot_from",
        "value": "opponent side"
    },
    19: {
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

name_lookup = {
    8: {
        "section": "auto",
        "value": "can move from initiation line"
    },
    9: {
        "section": "auto",
        "value": "can deliver upper"
    },
    10: {
        "section": "auto",
        "value": "can deliver lower"
    },
    11: {
        "section": "shoot_to",
        "value": "upper goal"
    },
    12: {
        "section": "shoot_to",
        "value": "lower goal"
    },
    13: {
        "section": "wheel",
        "value": "can do rotation control"
    },
    14: {
        "section": "wheel",
        "value": "can do position control"
    },
    17: {
        "section": "shoot_from",
        "value": "wall"
    },
    18: {
        "section": "shoot_from",
        "value": "opponent side"
    },
    19: {
        "section": "shoot_from",
        "value": "own side"
    }
}
lists = {
    "auto": [],
    "shoot_to": [],
    "shoot_from": [],
    "wheel": []
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

    pdf.add_page()
    pdf.set_font('Arial', 'B', 30)
    pdf.cell(40, 10, 'Team ' + str(row[1]), ln=1)
    pdf.set_font('Arial', '', 14)
    pdf.cell(40, 10, 'Drive Train: ' + row[6], ln=1)
    pdf.cell(40, 10, 'Weight: ' + str(row[7]), ln = 1)
    pdf.cell(40, 10, 'Max Reach: ' + str(row[15]), ln = 1) 
    pdf.cell(40, 10, 'Can Lift Others: ' + str(row[16]), ln=1)
    pdf.cell(40, 10, 'Auto Capabilities: ' + ", ".join(lists["auto"]),  ln = 1)
    pdf.cell(40, 10, 'Shooting Capabilities: ' + ", ".join(lists["shoot_to"]),  ln = 1)
    pdf.cell(40, 10, 'Shooting Positions: ' + ", ".join(lists["shoot_from"]),  ln = 1)
    pdf.cell(40, 10, 'Wheel Capabilities: ' + ", ".join(lists["wheel"]),  ln = 1)
    pdf.cell(40, 10, 'Comments: ' + row[20], ln=1)
    
    if len(row[21]) >= 1:
        pdf.image("c:\coding\\AdvantageScout\\" + row[21], 10,120, 125)
pdf.output('pitscout.pdf', 'F')
conn.close()    
conn1.close()