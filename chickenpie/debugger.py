#!/usr/bin/env python

from __future__ import print_function

import sys
import traceback

from chickenpie import opcodes
from chickenpie.vm import Machine


def boot(argv=sys.argv):
    m = Machine()
    m.load_file(argv[1])
    if len(argv) >= 3:
        m.load_input(argv[2])
    return m


def input_reader():
    EXIT_COMMANDS = 'bye', 'exit', 'quit', 'q'
    read = raw_input if sys.version_info[0] < 3 else input  # noqa

    try:
        inp = read('> ')
        while inp not in EXIT_COMMANDS:
            yield inp
            inp = read('> ')

    except EOFError:
        print('quit', file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print('Usage: chicken-debug SCRIPT.CH [INPUT]', file=sys.stderr)
        return

    machina = boot()
    breakpoints = set()

    for line in input_reader():
        if line:
            if ' ' in line:
                cmd, args = line.split(maxsplit=1)
            else:
                cmd, args = line, ''

        if cmd == 'py':
            try:
                try:
                    v = eval(args)
                    if v is not None:
                        print(v)
                except SyntaxError:
                    exec(args)
            except Exception:
                traceback.print_exc()

        elif cmd == 'r':
            for ip, opcode in machina:
                lineno = ip - 1
                if lineno in breakpoints:
                    print('breakpoint at line {0}, last instruction: {1}'.format(
                        lineno, opcodes.get_name(opcode)), file=sys.stderr)
                    break
            else:
                print(machina.look())

        elif cmd == 'restart':
            machina = boot()

        elif cmd in ('s', 'step', 'n', 'next'):
            v = machina.step()
            if v:
                print('{0}. {1}'.format(v[0] - 2, opcodes.get_name(v[1])))
            else:
                print('Program has finished executing.', file=sys.stderr)

        elif cmd in ('b', 'break'):
            breakpoints.add(int(args))

        elif cmd in ('ip', 'sp', 'stack'):
            print(getattr(machina, cmd))

        elif cmd in Machine.__dict__:
            f = getattr(machina, cmd)

            try:
                v = f(*map(eval, args.split()))
            except Exception:
                traceback.print_exc()

            if v is not None:
                print(v)

        else:
            print('huh?', file=sys.stderr)


if __name__ == '__main__':
    main()
