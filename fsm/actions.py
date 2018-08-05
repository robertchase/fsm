""" MIT License
https://github.com/robertchase/fsm/blob/master/LICENSE
"""
# pylint: disable=too-many-instance-attributes
from ergaleia.import_by_path import import_by_path


class TooFewTokens(Exception):
    def __init__(self, directive, line):
        super(TooFewTokens, self).__init__(
            '{} has too few tokens, line={}'.format(directive, line)
        )


class ExtraToken(Exception):
    def __init__(self, directive, count=None, line=0):
        if count is None:
            count, token = 'one', 'token'
        else:
            token = 'tokens'
        super(ExtraToken, self).__init__(
            '{} must have {} {}, line={}'.format(directive, count, token, line)
        )


class DuplicateName(Exception):
    def __init__(self, directive, line):
        super(DuplicateName, self).__init__(
            'duplicate {} name, line={}'.format(directive, line)
        )


class DuplicateDirective(Exception):
    def __init__(self, directive, line):
        super(DuplicateDirective, self).__init__(
            "duplicate directive '{}', line={}".format(directive, line)
        )


class State(object):

    def __init__(self, name):
        self.name = name
        self.enter = None
        self.exit = None
        self.events = {}


class Event(object):

    def __init__(self, name, next_state):
        self.name = name
        self.next_state = next_state
        self.actions = []


class Context(object):

    def __init__(self):
        self.states = {}
        self.first_state = None
        self.state = None
        self.event = None
        self.actions = []
        self.context = None
        self.handlers = {}

        self.line = None
        self.line_num = None

    def add_action(self, action):
        if action not in self.actions:
            self.actions.append(action)
            self.actions = sorted(self.actions)

    @property
    def events(self):
        events = []
        for state in self.states.values():
            for event in state.events.values():
                events.append(event.name)
        return list(set(events))


def act_state(context):
    args = context.line.split()
    if len(args) != 1:
        raise ExtraToken('STATE', line=context.line_num)
    name = args[0].strip()
    if name in context.states.keys():
        raise DuplicateName('STATE', context.line_num)
    if context.first_state is None:
        context.first_state = name
    context.state = State(name)
    context.states[name] = context.state


def act_enter(context):
    args = context.line.split()
    if len(args) != 1:
        raise ExtraToken('ENTER', line=context.line_num)
    name = args[0].strip()
    if context.state.enter is not None:
        raise DuplicateDirective('ENTER', context.line_num)
    context.state.enter = name
    context.add_action(name)


def act_exit(context):
    args = context.line.split()
    if len(args) != 1:
        raise ExtraToken('EXIT', line=context.line_num)
    name = args[0].strip()
    if context.state.exit is not None:
        raise DuplicateDirective('EXIT', context.line_num)
    context.state.exit = name
    context.add_action(name)


def act_event(context):
    args = context.line.split()
    if len(args) == 2:
        name, next_state = args
    elif len(args) != 1:
        raise ExtraToken('EVENT', 'one or two', context.line_num)
    else:
        name = args[0].strip()
        next_state = None
    context.event = Event(name, next_state)
    context.state.events[name] = context.event


def act_action(context):
    args = context.line.split()
    if len(args) != 1:
        raise ExtraToken('ACTION', line=context.line_num)
    name = args[0].strip()
    if name in context.event.actions:
        raise DuplicateName('ACTION', context.line_num)
    context.event.actions.append(name)
    context.add_action(name)


def act_context(context):
    if len(context.line.split()) != 1:
        raise ExtraToken('CONTEXT', line=context.line_num)
    if context.context:
        raise DuplicateName('CONTEXT', context.line_num)
    context.context = import_by_path(context.line)


def act_handler(context):
    args = context.line.split()
    if len(args) == 1:
        raise TooFewTokens('HANDLER', line=context.line_num)
    if len(args) > 2:
        raise ExtraToken('HANDLER', line=context.line_num)
    name, path = args
    name = name.strip()
    if name in context.handlers:
        raise DuplicateName('HANDLER', context.line_num)
    handler = import_by_path(path)
    context.handlers[name] = handler
