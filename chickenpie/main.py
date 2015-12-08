#!/usr/bin/env python

from __future__ import print_function

import sys

from chickenpie.vm import Machine


def main():
    if len(sys.argv) < 2:
        print('Usage: chicken SCRIPT.CH [INPUT]', file=sys.stderr)
        return

    machina = Machine()

    script = sys.argv[1]
    if script == '-':
        machina.load_str(sys.stdin.read())
        machina.load_input('')
    else:
        machina.load_file(script)

    if len(sys.argv) >= 3:
        machina.load_input(sys.argv[2])
        if len(sys.argv) == 4:
            machina.bbq_compat = eval(sys.argv[3])

    print(machina.run())


if __name__ == '__main__':
    main()
