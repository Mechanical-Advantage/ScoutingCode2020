import numpy as np
import sqlite3 as sql

#Defines the fields stored in the "Scout" table of the database. This database stores the record for each match scan
SCOUT_FIELDS = {
    "Team": 0,
    "Match": 0,
    "Fouls": 0,
    "TechFouls": 0,
    "Replay": 0,
    "Flag": 0,
    "Filler1": 0,
    "Filler2": 0,
    "Filler3": 0,
    "Filler4": 0,
    "AllianceColor": 0,
    "StartPos": 0,
    "CrossedLine": 0,
    "AutoLowerSuccess": 0,
	"AutoOuterSuccess": 0,
	"AutoInnerSuccess": 0,
	"AutoLowerFailures": 0,
    "AutoUpperFailures": 0,
	"LowerSuccess": 0,
    "OuterSuccess": 0,
	"InnerSuccess": 0,
    "LowerFailures": 0,
	"UpperFailures": 0,
    "ClimbAttempted": 0,
	"ClimbSuccess": 0,
    "LiftedOthersAttempted": 0,
	"LiftedOthersSuccess": 0,
    "ParkedAttempted": 0,
	"ParkedSuccess": 0,
    "WheelRotationAttempted": 0,
	"WheelRotationSuccess": 0,
    "WheelPositionAttempted": 0,
	"WheelPositionSuccess": 0,
    "WonMatch": 0,
	"Disabled": 0,
    "DriverRating": 0,
	"IntakeRating": 0,
    "DefenseRating": 0,
	"AvoidDefenseRating": 0
}

#Defines the fields that are stored in the "averages" and similar tables of the database. These are the fields displayed on the home page of the website.
AVERAGE_FIELDS = {
    "team": 0,
    "apr":0,
    "Filler1": 0,
    "Filler2": 0,
    "Filler3": 0,
    "Filler4": 0
}

#Defines the fields displayed on the charts on the team and compare pages
CHART_FIELDS = {
    "match": 0,
    "Filler1": 0,
    "Filler2": 0,
    "Filler3": 0,
    "Filler4": 0
}


# Main method to process a full-page sheet
# Submits three times, because there are three matches on one sheet
# The sheet is developed in Google Sheets and the coordinates are defined in terms on the row and column numbers from the sheet.
def processSheet(scout):
    for s in (0, 23):
        #Sets the shift value (used when turning cell coordinates into pixel coordinates)
        scout.shiftDown(s)

        num1 = scout.rangefield('J-5', 0, 9)
        num2 = scout.rangefield('J-6', 0, 9)
        num3 = scout.rangefield('J-7', 0, 9)
        num4 = scout.rangefield('J-8', 0, 9)
        scout.set("Team", 1000 * num1 + 100 * num2 + 10 * num3 + num4)

        match1 = scout.rangefield('AB-5', 0, 1)
        match2 = scout.rangefield('AB-6', 0, 9)
        match3 = scout.rangefield('AB-7', 0, 9)
        scout.set("Match", 100 * match1 + 10 * match2 + match3)

        scout.set("Fouls", int(0))
        scout.set("TechFouls", int(0))


        scout.set("AllianceColor", scout.rangefield('L-10', 0, 1))
        scout.set("StartPos", scout.rangefield('F-10', 1, 3)-1)
        scout.set("CrossedLine", scout.boolfield('H-12'))
        scout.set("AutoLowerSuccess", scout.countfield('T-12', 1, 5))
        scout.set("AutoOuterSuccess", scout.countfield('T-11', 1, 5))
        scout.set("AutoInnerSuccess", scout.countfield('T-10', 1, 5))
        scout.set("AutoLowerFailures", scout.countfield('AC-11', 1, 5))
        scout.set("AutoUpperFailures", scout.countfield('AC-10', 1, 5))
        
        scout.set("LowerSuccess", scout.countfield('H-16', 1, 28))
        scout.set("OuterSuccess", scout.countfield('H-15', 1, 28))
        scout.set("InnerSuccess", scout.countfield('H-14', 1, 28))
        scout.set("LowerFailures", scout.countfield('H-19', 1, 28))
        scout.set("UpperFailures", scout.countfield('H-18', 1, 28))

        scout.set("ClimbAttempted", scout.boolfield('H-21'))
        scout.set("ClimbSuccess", scout.boolfield('H-22'))
        scout.set("LiftedOthersAttempted", scout.boolfield('I-21'))
        scout.set("LiftedOthersSuccess", scout.boolfield('I-22'))
        scout.set("ParkedAttempted", scout.boolfield('J-21'))
        scout.set("ParkedSuccess", scout.boolfield('J-22'))
        
        scout.set("WheelRotationAttempted", scout.boolfield('L-21'))
        scout.set("WheelRotationSuccess", scout.boolfield('L-22'))
        scout.set("WheelPositionAttempted", scout.boolfield('M-21'))
        scout.set("WheelPositionSuccess", scout.boolfield('M-22'))

        scout.set("WonMatch", scout.boolfield('R-21'))
        scout.set("Disabled", scout.boolfield('R-22'))
        scout.set("DriverRating", scout.rangefield('U-21', 0, 5))
        scout.set("IntakeRating", scout.rangefield('U-22', 0, 5))
        scout.set("DefenseRating", scout.rangefield('AD-21', 0, 5))
        scout.set("AvoidDefenseRating", scout.rangefield('AD-22', 0, 5))

        scout.set("Replay", scout.boolfield('AK-5'))

        scout.submit()


#Takes an entry from the Scout database table and generates text for display on the team page. This page has 4 columns, currently used for auto, 2 teleop, and other (like fouls and end game)
def generateTeamText(e):
    text = {'auto': "", 'teleop1': "", 'teleop2': "", 'other': ""}
    text['auto'] += 'baseline, ' if e['Filler1'] else ''
    text['auto'] += 'Switch try, ' if e['Filler2'] else ''
    text['auto'] += 'Scale try, ' if e['Filler3'] else ''
    text['auto'] += 'Exchange try, ' if e['Filler4'] else ''

    text['teleop1'] += str(
        e['Filler1']) + 'x to scale, ' if e['Filler1'] else ''

    text['teleop2'] += str(
        e['Filler1']) + 'to switch, ' if e['Filler1'] else ''
    text['teleop2'] += str(
        e['Filler1']) + 'to opp switch, ' if e['Filler1'] else ''

    text['other'] = 'Climb, ' if e['Climb'] else ' '


    return text


#Takes an entry from the Scout database table and generates chart data. The fields in the returned dict must match the CHART_FIELDS definition at the top of this file
def generateChartData(e):
    dp = dict(CHART_FIELDS)
    dp["match"] = e['match']

    dp['Filler1'] += e['Filler1']
    dp['Filler2'] += e['Filler2']
    dp['Filler3'] += e['Filler3']
    dp['Filler4'] += e['Filler4']

    return dp


#Takes a set of team numbers and a string indicating quals or playoffs and returns a prediction for the alliances score and whether or not they will achieve any additional ranking points
def predictScore(datapath, teams, level='quals'):
    conn = sql.connect(datapath)
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    ballScore = []
    endGame = []
    autoGears = []
    teleopGears = []
    for n in teams:
        average = cursor.execute('SELECT * FROM averages WHERE team=?',
                                 (n, )).fetchall()
        assert len(average) < 2
        if len(average):
            entry = average[0]
        else:
            entry = [0] * 8
        autoGears.append(entry[2])
        teleopGears.append(entry[3])
        ballScore.append((entry[5] + entry[6]))
        endGame.append((entry[7]))
    retVal = {'score': 0, 'gearRP': 0, 'fuelRP': 0}
    score = sum(ballScore[0:3]) + sum(endGame[0:3])
    if sum(autoGears[0:3]) >= 1:
        score += 60
    else:
        score += 40
    if sum(autoGears[0:3]) >= 3:
        score += 60
    elif sum(autoGears[0:3] + teleopGears[0:3]) >= 2:
        score += 40
    if sum(autoGears[0:3] + teleopGears[0:3]) >= 6:
        score += 40
    if sum(autoGears[0:3] + teleopGears[0:3]) >= 12:
        score += 40
        if level == 'playoffs':
            score += 100
        else:
            retVal['gearRP'] == 1
    if sum(ballScore[0:3]) >= 40:
        if level == 'playoffs':
            score += 20
        else:
            retVal['fuelRP'] == 1
    retVal['score'] = score
    return retVal


#Takes an entry from the Scout table and returns whether or not the entry should be flagged based on contradictory data.
def autoFlag(entry):
#    if (entry['AutoHighBalls']
#            or entry['TeleopHighBalls']) and (entry['AutoLowBalls']
#                                              or entry['AutoHighBalls']):
#        return 1
#    if entry['Hang'] and entry['FailedHang']:
#        return 1
    return 0


#Takes a list of Scout table entries and returns a nested dictionary of the statistical calculations (average, maxes, median, etc.) of each field in the AVERAGE_FIELDS definition
def calcTotals(entries):
    sums = dict(AVERAGE_FIELDS)
    noDefense = dict(AVERAGE_FIELDS)
    lastThree = dict(AVERAGE_FIELDS)
    noDCount = 0
    lastThreeCount = 0
    for key in sums:
        sums[key] = []
    #For each entry, add components to the running total if appropriate
    for i, e in enumerate(entries):
        sums['Filler1'].append(e['Filler1'])
        sums['Filler2'].append(e['Filler2'])
        sums['Filler3'].append(e['Filler3'])
        sums['Filler4'].append(e['Filler4'])

        if i < 3:
            lastThree['Filler1'] += e['Filler1']
            lastThree['Filler2'] += e['Filler2']
            lastThree['Filler3'] += e['Filler3']
            lastThree['Filler4'] += e['Filler4']
            lastThreeCount += 1

    #If there is data, average out the last 3 or less matches
    if (lastThreeCount):
        for key, val in lastThree.items():
            lastThree[key] = round(val / lastThreeCount, 2)

    #If there were matches where the team didn't play D, average those out
    if (noDCount):
        for key, val in noDefense.items():
            noDefense[key] = round(val / noDCount, 2)

    average = dict(AVERAGE_FIELDS)
    median = dict(AVERAGE_FIELDS)
    maxes = dict(AVERAGE_FIELDS)
    for key in sums:
        if key != 'team' and key != 'apr':
            average[key] = round(np.mean(sums[key]), 2)
            median[key] = round(np.median(sums[key]), 2)
            maxes[key] = round(np.max(sums[key]), 2)
    retVal = {
        'averages': average,
        'median': median,
        'maxes': maxes,
        'noDefense': noDefense,
        'lastThree': lastThree
    }

    #Calculate APRs. This is an approximate average points contribution to the match
    for key in retVal:
        apr = 100
#        apr = retVal[key]['autoballs'] + retVal[key]['teleopballs'] + retVal[key]['end']
#        if retVal[key]['autogear']:
#            apr += 20 * min(retVal[key]['autogear'], 1)
#        if retVal[key]['autogear'] > 1:
#            apr += (retVal[key]['autogear'] - 1) * 10
#
#            min(retVal[key]['teleopgear'], 2 - retVal[key]['autogear']) * 20,
#            0)
#        if retVal[key]['autogear'] + retVal[key]['teleopgear'] > 2:
#            apr += min(retVal[key]['teleopgear'] + retVal[key]['autogear'] - 2,
#                       4) * 10
#        if retVal[key]['autogear'] + retVal[key]['teleopgear'] > 6:
#            apr += min(retVal[key]['teleopgear'] + retVal[key]['autogear'] - 6,
#                       6) * 7
        apr = int(apr)
        retVal[key]['apr'] = apr

    return retVal
