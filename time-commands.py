import argparse
import json
import subprocess
import os
import time
from subprocess import PIPE

parser = argparse.ArgumentParser(description="creates timings for all commands in the build.json and creates a command-timing.json")
parser.add_argument("-r", dest="reps", default=3, help="number of repetitions for timing (default 3)")
parser.add_argument("-c", dest="compiler", help="overwrite the compiler used for timing")

args = parser.parse_args()

assert os.path.exists("build.json"), "build.json file must exist"
with open('build.json') as json_file:
    data = json.load(json_file)
build_folder = data['build-dir']
assert os.path.exists(build_folder), "build folder does not exist"

result = []
tsum = 0.0

for cmd in data['commands']:
    type = cmd["type"]
    shell = True
    pcmd = cmd["cmd"]
    rcmd = pcmd

    if type == "compile":
        target = cmd["source"]
        cc = cmd["compiler"] if args.compiler is None else args.compiler
        pcmd = [cc] + cmd["args"]
        rcmd = " ".join(pcmd)
        shell = False
    elif type == "link":
        target = cmd["output"]
        cc = cmd["compiler"] if args.compiler is None else args.compiler
        pcmd = [cc] + cmd["args"]
        rcmd = " ".join(pcmd)
        shell = False
    elif type == "pack":
        target = cmd["output"]
        if not os.path.isabs(target):
            target = build_folder + "/" + target
    else:
        assert False, "unknown command type"

    print("[{}] {}".format(type, target))

    tmin = 1e30

    for i in range(args.reps):
        start = time.time()
        p = subprocess.run(pcmd, cwd=build_folder, shell=shell, stdout=PIPE)
        assert p.returncode == 0, "command failed"
        end = time.time()
        t = end - start
        print("    {} ms".format(t * 1000))
        if t < tmin:
            tmin = t
    tsum += tmin

    result.append({
        "type": type,
        "target": target,
        "time": tmin,
        "cmd": rcmd
    })
    
with open('command-timing.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)

print("{} commands in {} sec".format(len(result), tsum))
