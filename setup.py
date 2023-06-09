#!/usr/bin/env python3
import argparse
import pathlib
import shlex
import subprocess
import time
from subprocess import PIPE, Popen

parser = argparse.ArgumentParser()

parser.add_argument("-r", dest="uninstall", action="store_true", help="uninstall kinto")
parser.add_argument(
    "--remove", dest="uninstall", action="store_true", help="uninstall kinto"
)

args = parser.parse_args()

homedir = pathlib.Path("~").expanduser()
kintotype = 0


def use_x11() -> bool:
    cmd = "(env | grep -i x11 || loginctl show-session \"$XDG_SESSION_ID\" -p Type) | awk -F= '{print $2}'"
    output = cmdline(cmd)
    return bool(output.strip())


def cmdline(command):
    process = Popen(args=command, stdout=PIPE, universal_newlines=True, shell=True)
    return process.communicate()[0]


def mkdir_config():
    config_dir = homedir / ".config/kinto"
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        time.sleep(0.5)


def main():
    if not use_x11():
        print("You are not using x11, please logout and back in using x11/Xorg")
        return
    mkdir_config()
    cmdline("git fetch")
    kintover = cmdline(
        'echo "$(git describe --tag --abbrev=0 | head -n 1)" "build" "$(git rev-parse --short HEAD)"'
    )
    print(f"\nKinto {kintover} Type in Linux like it's a Mac.\n")

    if args.uninstall:
        subprocess.check_call(shlex.split("./xkeysnail_service.sh uninstall"))
    else:
        subprocess.check_call(shlex.split("./xkeysnail_service.sh"))


main()
