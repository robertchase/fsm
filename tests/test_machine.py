from fsm.parser import Parser


class LightBulb:
    def __init__(self):
        self.is_on = False
        self.error = False


def turn_on(bulb):
    bulb.is_on = True


def turn_off(bulb):
    bulb.is_on = False


def test_toggle():

    fsm = Parser.load([
        'STATE off',
        '  EVENT press on',
        '    ACTION turn_on',
        'STATE on',
        '  EVENT press off',
        '    ACTION turn_off',
        'CONTEXT tests.test_machine.LightBulb',
        'HANDLER turn_on tests.test_machine.turn_on',
        'HANDLER turn_off tests.test_machine.turn_off',
    ])

    assert not fsm.context.is_on
    fsm.handle('press')
    assert fsm.context.is_on
    fsm.handle('press')
    assert not fsm.context.is_on


def turn_off_exception(bulb):
    raise Exception('oh no')


def on_exception(bulb, e):
    bulb.error = True


def test_exception():

    fsm = Parser.load([
        'STATE off',
        '  EVENT press on',
        '    ACTION turn_on',
        'STATE on',
        '  EVENT press off',
        '    ACTION turn_off_exception',
        'CONTEXT tests.test_machine.LightBulb',
        'HANDLER turn_on tests.test_machine.turn_on',
        'HANDLER turn_off_exception tests.test_machine.turn_off_exception',
        'EXCEPTION tests.test_machine.on_exception',
    ])

    assert not fsm.context.is_on
    fsm.handle('press')
    assert fsm.context.is_on
    assert not fsm.context.error
    fsm.handle('press')
    assert fsm.context.is_on
    assert fsm.context.error


def on_exception_error(bulb, e):
    return 'error'


def set_error(bulb):
    bulb.error = True


def test_default():

    fsm = Parser.load([
        'STATE off',
        '  EVENT press on',
        '    ACTION turn_on',
        'STATE on',
        '  EVENT press off',
        '    ACTION turn_off_exception',
        'DEFAULT error',
        '    ACTION set_error',
        'CONTEXT tests.test_machine.LightBulb',
        'HANDLER turn_on tests.test_machine.turn_on',
        'HANDLER turn_off_exception tests.test_machine.turn_off_exception',
        'HANDLER set_error tests.test_machine.set_error',
        'EXCEPTION tests.test_machine.on_exception_error',
    ])

    assert not fsm.context.is_on
    fsm.handle('press')
    assert fsm.context.is_on
    assert not fsm.context.error
    fsm.handle('press')
    assert fsm.context.is_on
    assert fsm.context.error
