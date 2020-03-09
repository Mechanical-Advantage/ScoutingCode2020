import tbapy
import sqlite3 as sql
conn = sql.connect("c:\\mascout\\advantagescout\\data_2020.db")
conn1 = sql.connect("c:\\mascout\\advantagescout\\global.db")
cur = conn.cursor()
cur1 = conn1.cursor()
tba = tbapy.TBA(
    'aYSnteXRFd60FJ6KkRgbeZbPNf7z5BWJbcizc9lpHHDcB9lDQYWNhgyMDHTzc5kW')
event = cur1.execute(
    "SELECT value FROM config WHERE key = event").fetchall()[0][0]
#event = "2020ctnct"
data = tba.event_matches(event)
for x in data:
    if x["comp_level"] == "qm":
        blue_score = int(x["alliances"]["blue"]["score"])
        red_score = int(x["alliances"]["red"]["score"])
        comp_level = (x["comp_level"])
        match_number = int(x["match_number"])
        cur.execute("UPDATE match SET points = ? WHERE event = ? AND match = ? AND alliancecolor = ?",
                    (blue_score, event, match_number, 1))
        cur.execute("UPDATE match SET points = ? WHERE event = ? AND match = ? AND alliancecolor = ?",
                    (red_score, event, match_number, 0))


conn.commit()
conn.close()
conn1.close()
