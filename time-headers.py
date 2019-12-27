import argparse
import json
import subprocess
import os
import time
from subprocess import PIPE

parser = argparse.ArgumentParser(description="Measures parse overhead of all headers")
parser.add_argument("-r", dest="reps", default=3, help="number of repetitions for timing (default 3)")
parser.add_argument("-c", dest="compiler", help="overwrite the compiler used")

args = parser.parse_args()

assert os.path.exists("build.json"), "build.json file must exist"
assert os.path.exists("build-deps.json"), "build-deps.json file must exist"
with open('build.json') as json_file:
    build_info = json.load(json_file)
with open('build-deps.json') as json_file:
    build_deps = json.load(json_file)
build_folder = build_info['build-dir']
assert os.path.exists(build_folder), "build folder does not exist"

sources = set()

for cmd in build_info["commands"]:
    if cmd["type"] == "compile":
        sources.add(cmd["source"])

for dep in build_deps:
    if dep in sources:
        continue

    print("timing " + dep)

