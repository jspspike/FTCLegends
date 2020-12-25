# This was used to get info off the website and is now useless

import json

lines = open("rawinfo", "r").readlines()

teams = {}

for line in lines:
    name_start = line.find(" ")
    name_end = line.find("(")
    location_end = line.find(")")

    if name_end == -1 or "Detroit" in line or "Houston" in line:
        continue

    number = line[:name_start]
    name = line[name_start + 1 : name_end].strip()
    location = line[name_end + 1 : location_end].strip()

    print(line)
    print(number)
    print(name)
    print(location)

    teams[int(number)] = {"name": name, "location": location}

print(teams)
print(json.dumps(teams, indent=4, sort_keys=True))

# output = open('data.json', 'w')
# json.dump(teams, output, indent=4, sort_keys=True)
