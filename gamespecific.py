import numpy as np
import sqlite3 as sql

#Defines the fields stored in the "Scout" table of the database. This database stores the record for each match scan
SCOUT_FIELDS = {
    "Team": 0,
    "Match": 0,
    "Fouls": 0,
    "TechFouls": 0,
    "AutoCross": 0,
    "AutoSwitch": 0,
    "AttemptAutoSwitch": 0,
    "AutoScale": 0,
    "AttemptAutoScale": 0,
    "AutoXchange": 0,
    "AttemptAutoXchange": 0,
    "AllianceColor": 0,
    "StartPos": 0,
    "NumDelToScale": 0,
    "NumDelToSwitch":0,
    "NumDelToXchange": 0,
    "NumDelToOppSwitch": 0,
    "Climb": 0,
    "AttemptClimb": 0,
    "SupportOthers": 0,
    "FieldScaleLeft": 0,
    "FieldScaleRight": 0,
    "FieldSwitchLeft": 0,
    "FieldSwitchRight": 0,
    "AutoCrossField": 0,
    "SpareField1": 0,
    "SpareField2": 0,
    "Replay": 0,
    "Flag": 0,
    "wonMatch": 0,
    "troubleWithField": 0,
    "disabled": 0,
    "botPark": 0,
    "intakeEfficiency": 0,
    "switchEfficiency": 0,
    "scaleEfficiency": 0,
    "xchngEfficiency": 0,
    "driveEfficiency" :0,
    "cantIntake": 0,
    "cantDelToSwitch": 0,
    "cantDelToScale": 0,
    "cantDelToXchng": 0
}

#Defines the fields that are stored in the "averages" and similar tables of the database. These are the fields displayed on the home page of the website.
AVERAGE_FIELDS = {
    "team": 0,
    "apr":0,
    "NumDelToScale": 0,
    "NumDelToSwitch": 0,
    "NumDelToXchange": 0,
    "NumDelToOppSwitch": 0
}

#Defines the fields displayed on the charts on the team and compare pages
CHART_FIELDS = {
    "match": 0,
    "NumDelToScale": 0,
    "NumDelToSwitch": 0,
    "NumDelToXchange": 0,
    "NumDelToOppSwitch": 0
}


# Main method to process a full-page sheet
# Submits three times, because there are three matches on one sheet
# The sheet is developed in Google Sheets and the coordinates are defined in terms on the row and column numbers from the sheet.
def processSheet(scout):
    for s in (0, 16, 32):
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

        scout.set("AutoCross", scout.boolfield('I-11'))
        scout.set("AutoSwitch", scout.boolfield('I-12'))
        scout.set("AttemptAutoSwitch", scout.boolfield('J-12'))
        aswitch = scout.boolfield('I-12')
        scout.set("AutoScale", scout.boolfield('I-13'))
        scout.set("AttemptAutoScale", scout.boolfield('J-13'))
        ascale = scout.boolfield('I-13')
        scout.set("AutoXchange", scout.boolfield('I-14'))
        scout.set("AttemptAutoXchange", scout.boolfield('J-14'))
        scout.set("AllianceColor", scout.rangefield('M-11', 0, 1))
        scout.set("StartPos", scout.rangefield('M-13', 0, 2))
        stpos = scout.rangefield('O-13', 0, 2)

        scout.set("NumDelToScale", scout.rangefield('AB-13', 0, 9))
        scout.set("NumDelToXchange", scout.rangefield('AB-14', 0, 9))


        numallsw1 = scout.rangefield('AB-9', 0, 9)
        numallsw2 = scout.rangefield('AB-10', 0, 9)
        scout.set("NumDelToSwitch", numallsw1 * 10 + numallsw2)

        numoppsw1 = scout.rangefield('AB-11', 0, 9)
        numoppsw2 = scout.rangefield('AB-12', 0, 9)
        scout.set("NumDelToOppSwitch", numoppsw1 * 10 + numoppsw2)

        scout.set("Climb", scout.boolfield('AC-16'))
        scout.set("AttemptClimb", scout.boolfield('AB-16'))
        scout.set("botPark", scout.boolfield('AC-17'))
        scout.set("wonMatch", scout.boolfield('AC-18'))
        scout.set("SupportOthers", scout.boolfield('AJ-16'))
        scout.set("troubleWithField", scout.boolfield('AJ-17'))
        scout.set("disabled", scout.boolfield('AJ-18'))
        scout.set("intakeEfficiency", scout.rangefield('S-10', 1, 3))
        scout.set("switchEfficiency", scout.rangefield('R-11', 0, 3))
        scout.set("scaleEfficiency", scout.rangefield('R-12', 0, 3))
        scout.set("xchngEfficiency", scout.rangefield('R-13', 0, 3))
        scout.set("driveEfficiency", scout.rangefield('R-14', 1, 5))
        scout.set("cantIntake", scout.boolfield('V-10'))
        scout.set("cantDelToSwitch", scout.boolfield('V-11'))
        scout.set("cantDelToScale", scout.boolfield('V-12'))
        scout.set("cantDelToXchng", scout.boolfield('V-13'))
        scout.set("FieldScaleLeft", scout.boolfield('I-17'))
        fscleft = scout.boolfield('I-17')
        scout.set("FieldScaleRight", scout.boolfield('J-17'))
        fscright = scout.boolfield('J-17')
        scout.set("FieldSwitchLeft", scout.boolfield('I-18'))
        fswleft = scout.boolfield('I-18')
        scout.set("FieldSwitchRight", scout.boolfield('J-18'))
        fswright = scout.boolfield('J-18')
        scout.set("AutoCrossField", 0)
        across = 0
        print(stpos, ascale, aswitch, fscleft, fscright, fswleft, fswright)
        if stpos == 0 and ascale and fscright:
            across = 1
        if stpos == 0 and aswitch and fswright:
            across = 1
        if stpos == 2 and ascale and fscleft:
            across = 1
        if stpos == 2 and aswitch and fswleft:
            across = 1
        scout.set("AutoCrossField", across)

        scout.set("Replay", scout.boolfield('AK-5'))

#        sideAttempt = scout.boolfield('F-11') and not scout.boolfield('O-11')
#        centerAttempt = scout.boolfield('J-11') and not scout.boolfield('O-11')
#        sideSuccess = scout.boolfield('F-11') and scout.boolfield('O-11')
#        centerSuccess = scout.boolfield('J-11') and scout.boolfield('O-11')
#        scout.set("AutoSideAttempt", int(sideAttempt))
#        scout.set("AutoCenterAttempt", int(centerAttempt))
#        scout.set("AutoSideSuccess", int(sideSuccess))
#        scout.set("AutoCenterSuccess", int(centerSuccess))

        scout.submit()


#Takes an entry from the Scout database table and generates text for display on the team page. This page has 4 columns, currently used for auto, 2 teleop, and other (like fouls and end game)
def generateTeamText(e):
    text = {'auto': "", 'teleop1': "", 'teleop2': "", 'other': ""}
    text['auto'] += 'baseline, ' if e['AutoCross'] else ''
    text['auto'] += 'Switch try, ' if e['AutoSwitch'] else ''
    text['auto'] += 'Scale try, ' if e['AutoScale'] else ''
    text['auto'] += 'Exchange try, ' if e['AutoXchange'] else ''

    text['teleop1'] += str(
        e['NumDelToScale']) + 'x to scale, ' if e['NumDelToScale'] else ''

    text['teleop2'] += str(
        e['NumDelToSwitch']) + 'to switch, ' if e['NumDelToSwitch'] else ''
    text['teleop2'] += str(
        e['NumDelToOppSwitch']) + 'to opp switch, ' if e['NumDelToOppSwitch'] else ''

    text['other'] = 'Climb, ' if e['Climb'] else ' '


    return text


#Takes an entry from the Scout database table and generates chart data. The fields in the returned dict must match the CHART_FIELDS definition at the top of this file
def generateChartData(e):
    dp = dict(CHART_FIELDS)
    dp["match"] = e['match']

    dp['NumDelToScale'] += e['NumDelToScale']
    dp['NumDelToSwitch'] += e['NumDelToSwitch']
    dp['NumDelToOppSwitch'] += e['NumDelToOppSwitch']
    dp['NumDelToXchange'] += e['NumDelToXchange']

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
        sums['NumDelToScale'].append(e['NumDelToScale'])
        sums['NumDelToSwitch'].append(e['NumDelToSwitch'])
        sums['NumDelToXchange'].append(e['NumDelToXchange'])
        sums['NumDelToOppSwitch'].append(e['NumDelToOppSwitch'])

        if i < 3:
            lastThree['NumDelToScale'] += e['NumDelToScale']
            lastThree['NumDelToSwitch'] += e['NumDelToSwitch']
            lastThree['NumDelToXchange'] += e['NumDelToXchange']
            lastThree['NumDelToOppSwitch'] += e['NumDelToOppSwitch']
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
