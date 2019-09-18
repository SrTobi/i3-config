#!/bin/python3.7
import platform
import sys
import re

nodename = platform.node()

laptops = ["jetb", "thinky"]
towers = []

assert nodename in laptops + towers

vars = { name: (nodename == name) for name in laptops + towers }

vars["laptop"] = nodename in laptops







regex = r"^\s*(?P<cmd>!if|!else|!elif|!endif)\s*(?P<not>not)?\s+(?P<var>\w*)\s*$"
def parseline(line):
    matches = re.match(regex, line)
    if matches == None:
        return (False, None, None, None)
    return (True, matches.group("cmd"), matches.group("not") != None, matches.group("var"))



def generate(sourcepath, targetpath):
    print("Generate " + sourcepath + " -> " + targetpath)
    output = []
    with open(sourcepath, "r") as file:
        printLines = True
        cur = ""

        for line in file:
            (isCmd, cmd, negate, varname) = parseline(line)
            if isCmd:
                if cmd == "!if":
                    assert varname != ""
                    assert cur == ""
                    printLines = vars[varname]
                if cmd == "!elif":
                    assert varname != ""
                    assert cur == "!if" or cur == "!elif"
                    printLines = vars[varname]
                
                if negate:
                    printLines = not printLines

                if cmd == "!else":
                    assert not negate and varname == ""
                    assert cur == "!if" or cur == "!elif"
                    printLines = not printLines
                if cmd == "!endif":
                    assert not negate and varname == ""
                    assert cur != ""
                    printLines = True
                cur = cmd
            elif printLines:
                output.append(line)
        
    import os
    import stat

    if os.path.isfile(targetpath):
        os.chmod(targetpath, stat.S_IWRITE)

    with open(targetpath, "w") as file:
        file.writelines(output)
 
    os.chmod(targetpath, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)

print("name = " + nodename)
print("islaptop = " + str(vars["laptop"]))

generate("config.tmpl", "config")
generate("i3blocks.conf.tmpl", "i3blocks.conf")
