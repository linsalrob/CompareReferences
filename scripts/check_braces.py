"""
Check and find a record that has unbalanced braces
"""

import os
import sys
import argparse

__author__ = 'Rob Edwards'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-f', help='input file', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    last = None
    bropen = 0
    brclose = 0
    with open(args.f, 'r') as f:
        for l in f:
            if l.startswith('@'):
                if (bropen != brclose):
                    print(f"Record {last} has unbalanced braces. We opened {bropen} braces and closed {brclose} braces")
                bropen = l.count("{")
                brclose = l.count("}")
                last = l
            else:
                bropen += l.count("{")
                brclose += l.count("}")

if (bropen != brclose):
    print(f"Record {last} has unbalanced braces. We opened {bropen} braces and closed {brclose} braces")


