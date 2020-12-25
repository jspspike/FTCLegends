import copy
import os
import itertools
from jinja2 import Environment, FileSystemLoader
import json

data = json.load(open("data.json", "r"))

teams = copy.deepcopy(data["teams"])

for team in teams.values():
    team["score"] = 0
    team["placements"] = []

scores = {"w": 50, "f": 40, "sf": 30, "qf": 20}
last_event = "2017detroit"

for event_name, event in data["events"].items():
    for alliance in event["placement"]:
        for rank, number in alliance.items():
            if rank == "place":
                points = scores[number]
                placement = number
                continue

            if int(rank) == 2:
                points //= 2

            team = teams[str(number)]
            team["score"] += points

            if placement == "w":
                placement = "Winning Alliance"
            elif placement == "f":
                placement = "Finalist Alliance"
            elif placement == "sf":
                placement = "Semi-Finalist Alliance"
            elif placement == "qf":
                placement = "Quarter-Finalist Alliance"

            if rank == "0":
                rank = "Captain"
            elif rank == "1":
                rank = "1st Pick"
            elif rank == "2":
                rank = "2nd Pick"

            if "short" in event:
                event_name_short = event["short"]
            else:
                event_name_short = event_name
            
            team["placements"].append(
                {"event": event_name_short, "placement": placement, "rank": rank}
            )

            files = [f for f in os.listdir('./public/img/teams') if f.startswith(str(number))]
            if len(files) == 0:
                img = 'unknown.png'
            else:
                img = files[0]

            team["img"] = img

teams_old = copy.deepcopy(data["teams"])

for team in teams_old.values():
    team["score"] = 0
    team["placements"] = []

started = False
for event_name, event in data["events"].items():
    if event_name == last_event:
        started = True
    if not started:
        continue

    for alliance in event["placement"]:
        for rank, number in alliance.items():
            if rank == "place":
                points = scores[number]
                placement = number
                continue

            if int(rank) == 2:
                points //= 2

            team = teams_old[str(number)]
            team["score"] += points


teams = dict(sorted(teams.items(), key = lambda item: item[1]["score"], reverse=True))
teams_old = dict(sorted(teams_old.items(), key = lambda item: item[1]["score"], reverse=True))

for number in teams_old.keys():
    curr_rank = list(teams).index(number)
    old_rank = list(teams_old).index(number)

    if curr_rank < old_rank:
        teams[number]["diff"] = old_rank - curr_rank

locations = {}

for number, team in teams.items():
    team_location = team["location"]

    if team_location == "??":
        continue

    if team_location in data["locations"]:
        location_name = data["locations"][team_location]
    else:
        location_name = team_location

    if team_location in locations:
        locations[team_location]["score"] += team["score"]

        locations[team_location]["teams"].append((number, team))
    else:
        locations[team_location] = {"name": location_name, "score": team["score"], "teams": [(number, team)]}

locations = dict(sorted(locations.items(), key = lambda item: item[1]["score"], reverse=True))

print(json.dumps(teams, indent=4, sort_keys=True))
#print(json.dumps(teams_old, indent=4, sort_keys=True))
print(json.dumps(locations, indent=4, sort_keys=True))

env = Environment(
    loader=FileSystemLoader(searchpath="."),
)

teams = list(teams.items())

template = env.get_template("index.template.html")
template.stream(events=data["events"], teams=teams, locations=locations).dump(
    "public/index.html"
)
