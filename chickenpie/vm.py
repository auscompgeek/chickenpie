from . import opcodes
from .parser import parse


class Machine(object):
    """A Chicken VM.

    Attributes:
    - ip - instruction pointer
    - sp - stack pointer
    - stack
    """

    ip = None
    sp = -1

    def __init__(self, input_: str = None, code: str = None):
        self.stack = []
        self.push(self.stack)
        self.push(input_)
        if code:
            self.load_str(code)

    def __iter__(self):
        return self

    def __next__(self):
        x = self.step()
        if x is None:
            raise StopIteration
        return x

    next = __next__

    def exec_op(self, opcode: int):
        """Execute an opcode."""

        if opcode == opcodes.CHICKEN:
            self.push('chicken')

        elif opcode == opcodes.ADD:
            a, b = self.pop(), self.pop()

            # JavaScript's + operator coerces to string if either operand is string
            if isinstance(a, str):
                b = str(b)
            elif isinstance(b, str):
                a = str(a)

            self.push(b + a)

        elif opcode == opcodes.FOX:
            a, b = self.pop(), self.pop()

            # JavaScript's - operator coerces both operands to numbers
            if isinstance(b, str):
                b = int(b)
            if isinstance(a, str):
                a = int(a)

            self.push(b - a)

        elif opcode == opcodes.ROOSTER:
            a, b = self.pop(), self.pop()
            self.push(a * b)
        elif opcode == opcodes.COMPARE:
            a, b = self.pop(), self.pop()
            self.push(a == b)

        elif opcode == opcodes.PICK:
            where = self.next_op()
            if where == 1:
                source = self.get_input()
            else:
                source = self.stack[where]
            addr = self.pop()

            #self.push(source[addr])
            try:
                if source is self.stack and addr == 1:
                    self.push(self.get_input())
                else:
                    self.push(source[addr])
            except (IndexError, TypeError):
                self.push(None)

        elif opcode == opcodes.PECK:
            addr = self.pop()
            self.set(addr, self.pop())

        elif opcode == opcodes.FR:
            offset = self.pop()
            if self.pop():
                self.ip += offset

        elif opcode == opcodes.BBQ:
            self.push(chr(self.pop()))
        else:
            self.push(opcode - 10)

    def get_input(self):
        """Get input, either previously loaded or from stdin."""

        if self.stack[1] is None:
            self.stack[1] = input()
        return self.stack[1]

    def has_loaded(self):
        """Check whether a Chicken program has been loaded."""
        return self.ip is not None

    def is_end(self):
        """Check whether we have finished executing."""
        return self.ip >= len(self.stack) or not self.peek()

    def load_file(self, filename: str):
        """Load a Chicken program from a file."""

        with open(filename) as f:
            self.load_str(f.read())

    def load_input(self, inp: str):
        """Load input from a string."""
        self.stack[1] = inp

    def load_str(self, code: str):
        """Load a Chicken program from a string."""
        bytecode = parse(code)
        self.stack += bytecode
        self.sp = len(self.stack)
        if self.ip is None:
            self.ip = 2

    def look(self):
        """Get the top value on the stack."""
        return self.stack[self.sp]

    def next_op(self) -> int:
        """Get the next instruction, advancing the instruction pointer."""

        opcode = self.peek()
        self.ip += 1
        return opcode

    def peek(self) -> int:
        """Get the next instruction."""
        return self.stack[self.ip]

    def push(self, val):
        """Push a value onto the stack."""

        self.sp += 1
        self.set(self.sp, val)

    def pop(self):
        """Pop a value off the stack."""

        val = self.stack[self.sp]
        self.sp -= 1
        return val

    def run(self):
        """Execute the loaded Chicken program."""

        for _ in self:
            pass
        return self.look()

    def set(self, addr, value):
        l = len(self.stack)
        if addr == l:
            self.stack.append(value)
        elif addr > l:
            self.stack += [None] * (addr - l + 1)
            self.stack[addr] = value
        else:
            self.stack[addr] = value

    def step(self):
        """Execute the next instruction.

        Returns the advanced IP and the last executed opcode."""

        if not self.has_loaded():
            raise RuntimeError('No Chicken program has been loaded.')

        if self.is_end():
            return None

        opcode = self.next_op()
        self.exec_op(opcode)
        return self.ip, opcode
