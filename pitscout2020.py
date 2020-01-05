import csv
import sqlite3 as sql
from fpdf import FPDF
pdf = FPDF()
conn = sql.connect("data_2019.db")
cur = conn.cursor()
event_name
cur.execute("SELECT * FROM pit order by Team ")
Pitscout = cur.fetchall()

for row in Pitscout:
    print(row)
        
    pdf.add_page()
    pdf.set_font('Arial', 'B', 30)
    pdf.cell(40, 10, 'Team ' + str(row[1]), ln=1)
    pdf.set_font('Arial', '', 20)
    pdf.cell(40, 10, 'Drive Train: ' + row[6], ln=1)
    pdf.cell(40, 10, 'Auto/Semi Auto: ' + row[7], ln=1)
    pdf.cell(40, 10, 'Comments: ' + row[8], ln=1)
    pdf.image(row[9], 10, 60, 175)
pdf.output('pitscout.pdf', 'F')
conn.close()