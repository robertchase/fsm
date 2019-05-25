"""
A demonstration of a DEFAULT event.

A slight modification of example.exception.fsm which adds a DEFAULT 'error'
event. When the EXCEPTION handler runs, it emits an 'error' event which
is handled in both the 'init' and 'error' states.
"""


def yay():
    print('ACTION', 'yay!')


def boo():
    print('ACTION', 'boo!')
    raise Exception('boo')


def ohno():
    print('ACTION', 'ohno!')


def on_exception(e):
    print('EXCEPTION', e)
    return 'error'


if __name__ == '__main__':
    from fsm.parser import Parser

    def trace(*args):
        print('TRACE state=%s event=%s, default=%s internal=%s' % args)

    def state_change(*args):
        print('STATE CHANGE', ' -> '.join(args))

    fsm = Parser.load('example.default.fsm')
    fsm.trace = trace
    fsm.on_state_change = state_change

    fsm.handle('yay')
    fsm.handle('boo')
    fsm.handle('yay')
