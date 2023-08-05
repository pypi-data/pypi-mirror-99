#!/bin/env python3
"""A command-line interface for LADOK 3"""

import appdirs
import argcomplete, argparse
import json
import os
import re
import sys
import traceback

import ladok3.data

dirs = appdirs.AppDirs("ladok", "dbosk@kth.se")

def err(rc, msg):
  print(f"{sys.argv[0]}: error: {msg}", file=sys.stderr)
  traceback.print_exc(file=sys.stderr)
  sys.exit(rc)

def warn(msg):
  print(f"{sys.argv[0]}: {msg}", file=sys.stderr)
def load_credentials(filename):
  """Load credentials from environment or file named filename"""
  try:
    user = os.environ["LADOK_USER"]
    passwd = os.environ["LADOK_PASS"]
    return user, passwd
  except:
    pass

  try:
    with open(filename) as conf_file:
      config = json.load(conf_file)
    return config["username"], config["password"]
  except:
    raise Exception("Cannot find credentials.")
def main():
  """Run the command-line interface for the ladok command"""
  argp = argparse.ArgumentParser(
    description="Command-line interface for LADOK3",
    epilog="Web: https://github.com/dbosk/ladok3"
  )
  argp.add_argument("-f", "--config-file",
    default=f"{dirs.user_config_dir}/config.json",
    help=f"Path to configuration file, default: {dirs.user_config_dir}/config.json")
  subp = argp.add_subparsers(required=True)
  ladok3.data.add_command_options(subp)
  argcomplete.autocomplete(argp)
  args = argp.parse_args()
  LADOK_USER, LADOK_PASS = load_credentials(args.config_file)
  ls = ladok3.LadokSessionKTH(LADOK_USER, LADOK_PASS)
  if "func" in args:
    args.func(ls, args)

if __name__ == "__main__":
  try:
    main()
    sys.exit(0)
  except Exception as e:
    err(-1, e)
