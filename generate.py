# Generates site by parsing `data.json` and using `index.template.html`

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

scores = {"w": 60, "f": 50, "sf": 40, "qf": 30}
placement_names = {
    "w": "Winning Alliance",
    "f": "Finalist Alliance",
    "sf": "Semi-Finalist Alliance",
    "qf": "Quarter-Finalist Alliance",
}
last_event = "2017stlouis"

# Iterate through each event and tally up points and placement lists for each team
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

            if placement in placement_names:
                placement = placement_names[placement]

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

            files = [
                f for f in os.listdir("./public/img/teams") if f.startswith(str(number))
            ]
            if len(files) == 0:
                img = "unknown.png"
            else:
                img = files[0]

            team["img"] = img

teams_old = copy.deepcopy(data["teams"])

for team in teams_old.values():
    team["score"] = 0
    team["placements"] = []

# Iterate through events starting from `last_event` to tally up previous points
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


teams = dict(sorted(teams.items(), key=lambda item: item[1]["score"], reverse=True))
teams_old = dict(
    sorted(teams_old.items(), key=lambda item: item[1]["score"], reverse=True)
)

# Use sorted `teams` and `teams_old` to find changes in team ranking from `last_event`
for number in teams_old.keys():
    curr_rank = list(teams).index(number)
    old_rank = list(teams_old).index(number)

    if curr_rank < old_rank:
        teams[number]["diff"] = old_rank - curr_rank

locations = {}

# Iterate through `teams` to tally up points for differetion locations
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
        locations[team_location] = {
            "name": location_name,
            "score": team["score"],
            "teams": [(number, team)],
        }

locations = dict(
    sorted(locations.items(), key=lambda item: item[1]["score"], reverse=True)
)
locations_list = [
    tuple(list(locations.items())[i : i + 3])
    for i in range(0, len(list(locations.items())), 3)
]

locations_old = {}

# Iterate through `teams_old` to tally up points for differetion locations starting from `last_event`
for team in teams_old.values():
    team_location = team["location"]

    if team_location == "??":
        continue

    if team_location in locations_old:
        locations_old[team_location]["score"] += team["score"]
    else:
        locations_old[team_location] = {"score": team["score"]}


locations_old = dict(
    sorted(locations_old.items(), key=lambda item: item[1]["score"], reverse=True)
)


# Use sorted `locations` and `locations_old` to find changes in location ranking from `last_event`
for location in locations_old.keys():
    curr_rank = list(locations).index(location)
    old_rank = list(locations_old).index(location)

    if curr_rank < old_rank:
        locations[location]["diff"] = old_rank - curr_rank


# print(json.dumps(teams, indent=4, sort_keys=True))
# print(json.dumps(teams_old, indent=4, sort_keys=True))
# print(json.dumps(locations, indent=4, sort_keys=True))

env = Environment(
    loader=FileSystemLoader(searchpath="."),
)

teams_list = list(
    teams.items()
)  # This and locations_list is kinda bad but I was too lazy to figure how to slice an iterator

template = env.get_template("index.template.html")
template.stream(
    events=data["events"],
    teams=teams,
    teams_list=teams_list,
    locations=locations,
    locations_list=locations_list,
    placement_names=placement_names,
).dump("public/index.html")
