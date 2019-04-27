import sqlite3 as sql
import tbapy
from pathlib import Path

TBAkey = "yZEr4WuQd0HVlm077zUI5OWPfYsVfyMkLtldwcMYL6SkkQag29zhsrWsoOZcpbSj"

database = input("Database name: ")
#Check database exists
tempPath = Path(database)
if not tempPath.is_file():
    print("That database does not exist")
    exit(1)
conn = sql.connect(database)
cur = conn.cursor()

eventKey = input("Event key: ")
tba = tbapy.TBA(TBAkey)
try:
    matchlistRaw = tba.event_matches(eventKey)
except:
    print("Failed to retrieve matches from TBA")
    exit(1)

for i in range(len(matchlistRaw)):
    if matchlistRaw[i].comp_level == "qm":
        if matchlistRaw[i].winning_alliance == "red":
            redWon = 1
            blueWon = 0
        else:
            redWon = 0
            blueWon = 1
        cur.execute("UPDATE scout SET WonMatch=? WHERE Match=? AND AllianceColor=?", (redWon, matchlistRaw[i].match_number, 0))
        cur.execute("UPDATE scout SET WonMatch=? WHERE Match=? AND AllianceColor=?", (blueWon, matchlistRaw[i].match_number, 1))
conn.commit()
conn.close()
print("Update successful")
