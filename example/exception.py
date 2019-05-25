"""
A demonstration of an Exception handler.

When the 'boo' action is run, it throws an exception. The on_exception
handler is automatically invoked, emitting an 'error' event, transitioning
the machine to the 'error' state.
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

    fsm = Parser.load('example.exception.fsm')
    fsm.trace = trace
    fsm.on_state_change = state_change

    fsm.handle('yay')
    fsm.handle('boo')
    fsm.handle('yay')
