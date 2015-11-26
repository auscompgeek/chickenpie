def parse(prog):
    """Parse a Chicken program into bytecode."""

    opcodes = []
    prog = prog.split('\n')

    for i, line in enumerate(prog, 1):
        count = 0
        for j, word in enumerate(line.split(), 1):
            if word != 'chicken':
                raise SyntaxError('line %d word %d: expected "chicken", found "%s"' % (i, j, word))
            count += 1
        opcodes.append(count)

    return opcodes
