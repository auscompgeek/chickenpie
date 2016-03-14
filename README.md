# chickenpie

A Python implementation of the [Chicken][] esoteric programming language.

This… mostly works. Of the example programs, deadfish doesn't work properly
at all. The others work fine.

## Usage
In the project root:
```console
$ python -m chickenpie examples/helloworld.ch
Hello world
$ python -m chickenpie.debugger examples/helloworld.ch
> b 38
> r
breakpoint at line 38, last instruction: BBQ
> s
38. push 1
> stack
[[...], 'd', 20, 20, 4, 9, 11, 7, 10, 16, 16, 4, 3, 10, 17, 3, 10, 10, 13, 11, 12, 6, 0, 3, 14, 4, 21, 13, 16, 10, 15, 13, 6, 0, 4, 18, 2, 2, 9, 11, 6, 0, 2, 11, 7, 12, 6, 0, 12, 3, 12, 7, 12, 6, 0, 10, 39, 3, 8, 11, 6, 0, None, -36, -7, 0, 0, 3, -76, 11, 3, 6, 'l', 1, 8]
> py 1 + 1
2
> quit
$ python -m chickenpie examples/99chickens.ch 9
9 chickens
8 chickens
7 chickens
6 chickens
5 chickens
4 chickens
3 chickens
2 chickens
1 chicken
no chickens
```

For all commands the debugger accepts, see its source code (and a list of the VM methods).

## Prior art
* [pychicken][] is an unrelated, incomplete, and probably dysfunctional implementation.
* [chicken-php][] is a full implementation in PHP, with a command line wrapper.
* ... and of course, the original chicken.js itself.

## License
[MIT](LICENSE).


[Chicken]: http://torso.me/chicken
[pychicken]: https://github.com/zjs/pychicken
[chicken-php]: https://github.com/igorw/chicken-php
