import argparse
import json
import subprocess
import os
import time
from subprocess import PIPE

parser = argparse.ArgumentParser(description="creates build-deps.json containing per-source header dependencies")
parser.add_argument("-c", dest="compiler", help="overwrite the compiler used")

args = parser.parse_args()

assert os.path.exists("build.json"), "build.json file must exist"
with open('build.json') as json_file:
    data = json.load(json_file)
build_folder = data['build-dir']
assert os.path.exists(build_folder), "build folder does not exist"

deps = {}

rec_deps = set()

second_pass = []

total_headers = 0
total_sources = 0

def get_deps(src, args):    
    global build_folder
    print("analyze " + src)
    print(" ".join(args))
    p = subprocess.run(args, cwd=build_folder, stdout=PIPE)
    assert p.returncode == 0, "command failed"

    incs = []

    for line in p.stdout.decode("utf-8").splitlines()[1:]:
        line = line.strip(" \\")
        for l in line.split():
            l = os.path.abspath(l)        
            assert os.path.exists(l), "include " + l + "does not exist"
            if l == src:
                continue
            incs.append(l)

    return incs

for cmd in data["commands"]:
    if cmd["type"] != "compile":
        continue

    cc = cmd["compiler"] if args.compiler is None else args.compiler
    cargs = cmd["args"]

    if "-M" in cargs:
        cargs.remove("-M")
    if "-MD" in cargs:
        cargs.remove("-MD")
    if "-o" in cargs:
        cargs.pop(cargs.index("-o") + 1)
        cargs.pop(cargs.index("-o"))
    if "-MF" in cargs:
        cargs.pop(cargs.index("-MF") + 1)
        cargs.pop(cargs.index("-MF"))
    if "-MT" in cargs:
        cargs.pop(cargs.index("-MT") + 1)
        cargs.pop(cargs.index("-MT"))
    if "-c" in cargs:
        cargs.pop(cargs.index("-c") + 1)
        cargs.pop(cargs.index("-c"))
    cargs.append("-MM")
    cargs.append("-c")
    cargs.append(cmd["source"])

    incs = get_deps(cmd["source"], [cc] + cargs)

    for i in incs:
        if i not in rec_deps:
            rec_deps.add(i)
            a = cargs.copy()
            a[-1] = i
            second_pass.append([cc] + a)
            total_headers += 1

    total_sources += 1

    deps[cmd["source"]] = incs

for cmd in second_pass:
    incs = get_deps(cmd[-1], cmd)
    deps[cmd[-1]] = incs

with open('build-deps.json', 'w') as outfile:
    json.dump(deps, outfile, indent=4)

print("analyzed {} sources, found a total of {} dependencies".format(total_sources, total_headers))
