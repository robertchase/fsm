"""
A two-state machine that toggles between states on a single event.

Each time the 'press' event is handled by the machine, it runs an
action routine ('turn_on' or 'turn_off') and transitions to the other
state.

The machine is created using the Parser's load method, which parses
the machine description and handler paths, and binds them together
returning an initialzed finite state machine.
"""


def turn_on():
    print('the light is on')


def turn_off():
    print('the light is off')


if __name__ == '__main__':
    from fsm.parser import Parser

    fsm = Parser.load('example.light.fsm')

    fsm.handle('press')
    fsm.handle('press')
    fsm.handle('press')
