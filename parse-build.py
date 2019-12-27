import argparse
import json
import subprocess
import os
from subprocess import PIPE

cxx_compilers = [
    "g++",
    "clang++",
    "zapcc++"
]

parser = argparse.ArgumentParser(description="parses a ninja build and creates a build.json")
parser.add_argument("build_folder", metavar="D", help="build folder (must contain a build.ninja)")

args = parser.parse_args()

build_folder = args.build_folder
assert os.path.isdir(build_folder), "build folder must exist"
assert os.path.exists(build_folder), "build folder must exist"

p = subprocess.run(["ninja", "-t", "commands"], cwd=build_folder, stdout=PIPE)
assert p.returncode == 0, "ninja failed"

cmds = []

def is_cxx_compiler(s):
    for c in cxx_compilers:
        if s.endswith(c):
            return True
    return False

def is_archive_packing(line):
    return "cmake -E remove" in line \
        and "ar qc " in line \
        and ".a &&" in line

def is_compile_command(cmd):
    return ("-c" in cmd) and ("-o" in cmd)

def is_link_command(cmd):
    return ("-c" not in cmd) and ("-o" in cmd)

compile_cmds = 0
link_cmds = 0
pack_cmds = 0

for line in p.stdout.splitlines():
    line = line.decode("utf-8")
    if line.startswith(": && "):
        line = line.replace(": && ", "")
        line = line.replace(" && :", "")
    line = line.strip()
    cmd = line.split()

    if len(cmd) == 0:
        continue

    if is_cxx_compiler(cmd[0]):
        if is_compile_command(cmd): # COMPILE
            cmds.append({
                "type": "compile",
                "source": cmd[cmd.index("-c") + 1],
                "output": cmd[cmd.index("-o") + 1],
                "compiler": cmd[0],
                "args": cmd[1:],
                "cmd": line
            })
            compile_cmds += 1

        elif is_link_command(cmd): # LINK
            cmds.append({
                "type": "link",
                "output": cmd[cmd.index("-o") + 1],
                "compiler": cmd[0],
                "args": cmd[1:],
                "cmd": line
            })
            link_cmds += 1

        else:
            assert False, "unknown compile command: " + line

    elif is_archive_packing(line): # PACK
        cmds.append({
            "type": "pack",
            "output": cmd[cmd.index("remove") + 1],
            "cmd": line
        })
        pack_cmds += 1

    else:
        assert False, "unknown command: " + line

data = {
    'build-dir': build_folder,
    'commands': cmds
}

with open('build.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

print("found {} commands".format(len(cmds)))
print("  {} compile commands".format(compile_cmds))
print("  {} link commands".format(link_cmds))
print("  {} pack commands".format(pack_cmds))
