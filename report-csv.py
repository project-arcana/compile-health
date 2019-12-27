import csv
import os
import json

if os.path.exists("command-timing.json"):
    with open('command-timing.json') as json_file:
        data = json.load(json_file)

    with open('command-timing.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(["idx", "type", "target", "time (ms)", "cmd"])
        for i, cmd in enumerate(data):
            csv_writer.writerow([str(i), cmd["type"], cmd["target"], str(cmd["time"] * 1000), cmd["cmd"]])

    print("generated command-timing.csv")
