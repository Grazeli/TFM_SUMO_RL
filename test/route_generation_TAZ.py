import os
import subprocess

import argparse
import sys

#subprocess.run(["ls", "-la"])

parser = argparse.ArgumentParser(description='Generate SUMO routes based on TAZ and TAZ relations')
parser.add_argument('--tazgrid', type=str, help='Tazgrid definitions')
parser.add_argument('--relations', type=str, help='Tazgrid relations')
parser.add_argument('--network', type=str, help='Sumo network')
parser.add_argument('--output', type=str, help='Name of the route name')

args = parser.parse_args(sys.argv[1:])
print(args)




print('Done')