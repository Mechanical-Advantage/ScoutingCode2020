import itertools
import numpy
import sqlite3 as sql
import xlsxwriter

# Config
data_path = "C:\\mascout\\AdvantageScout\\data_2020.db"
global_path = "C:\\mascout\\AdvantageScout\\global.db"
output_path = "C:\\mascout\\TableauInput\\balance.xlsx"
our_team = 6328
extra_weight = 23  # weight of bumpers and batteries

# Connect to db
conn_data = sql.connect(data_path)
cur_data = conn_data.cursor()
conn_global = sql.connect(global_path)
cur_global = conn_global.cursor()


def run_match(teams):
    # Get weights for teams
    team_weights = []
    for team in teams:
        result = cur_data.execute(
            "SELECT weight FROM pit WHERE team=? ORDER BY time DESC LIMIT 1", (team,)).fetchall()
        if len(result) == 0:
            print("Could not find weight for", team)
            exit(0)
        else:
            team_weights.append(result[0][0] + extra_weight)

    def get_solution(weights):
        # Calculate centers of mass
        positions = list(itertools.product(range(114), repeat=len(weights)))
        centers = []
        for i in positions:
            valid = True
            for test in i:
                if test >= 55 and test < 59:
                    valid = False
                    break

            if valid:
                total = 0
                for f in range(len(weights)):
                    total += weights[f] * i[f]
                centers.append(round(abs((total / sum(weights)) - 56.5)))
            else:
                centers.append(999)

        # Find best solutions
        best = min(centers)
        solutions = [positions[index]
                     for index, value in enumerate(centers) if value == best]

        # Calculate separations
        separations = []
        for i in solutions:
            ordered = sorted(i)
            separations.append(min(numpy.diff(ordered)))

        # Find best solutions by separation
        best = max(separations)
        final_solution = solutions[separations.index(best)]
        return list(final_solution)

    # Run calculations
    solutions = []
    solutions_teams = []
    solutions_weights = []
    solutions.append(get_solution(team_weights))
    solutions_teams.append(teams)
    solutions_weights.append(team_weights)
    for combo in itertools.combinations(range(3), 2):
        solutions.append(get_solution([team_weights[x] for x in combo]))
        solutions_teams.append([teams[x] for x in combo])
        solutions_weights.append([team_weights[x] for x in combo])
    return {"solutions": solutions, "teams": solutions_teams, "weights": solutions_weights}


# Run matches
matches = cur_global.execute(
    "SELECT match,r1,r2,r3 FROM schedule WHERE r1=? OR r2=? OR r3=?", (our_team, our_team, our_team)).fetchall()
matches += cur_global.execute(
    "SELECT match,b1,b2,b3 FROM schedule WHERE b1=? OR b2=? OR b3=?", (our_team, our_team, our_team)).fetchall()
matches.sort(key=lambda x: x[0])
match_results = {}
for match in matches:
    print("Balancing match", match[0])
    match_results[match[0]] = run_match(match[1:4])

# Write to excel sheet
workbook = xlsxwriter.Workbook(output_path)
worksheet = workbook.add_worksheet("balance")
worksheet.write("A1", "Position")
worksheet.write("B1", "Height")
worksheet.write("C1", "Team")
worksheet.write("D1", "Weight")
worksheet.write("E1", "Match")
row = 0
for match_number, result in match_results.items():
    for i in range(len(result["solutions"])):
        for x in range(len(result["solutions"][i])):
            row += 1
            worksheet.write(row, 0, (result["solutions"][i][x] - 56.5) / 12)
            worksheet.write(row, 1, 20 - (i * 5))
            worksheet.write(row, 2, result["teams"][i][x])
            worksheet.write(row, 3, result["weights"][i][x])
            worksheet.write(row, 4, match_number)
workbook.close()
print("Wrote to output file")

conn_data.close()
conn_global.close()
