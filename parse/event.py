# This was used to get info off the website and is now useless

import json


def placement(p):
    p = int(p)
    if p == 1:
        return "w"
    elif p == 2:
        return "f"
    elif p <= 4:
        return "sf"
    else:
        return "qf"


lines = open("restinfo", "r").readlines()

events = {}

for line in lines:

    line = line.strip()
    if line == "":
        continue
    print(line)

    name_end = line.find("(")

    if len(line) == 4:
        year = line
        events[line] = {"name": "World Championship " + line, "placement": []}
    elif name_end == -1 and line != "<br/>":
        place = placement(line[0])

        e = {"place": place}
        events[year]["placement"].append(e)

        rank = 0
    elif name_end != -1:
        team_number = line[: line.find(" ")]

        e[rank] = int(team_number)

        rank += 1

print(events)
print(json.dumps(events, indent=4))
