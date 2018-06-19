from functools import partial

from ergaleia.import_by_path import import_by_path


class TooFewTokens(Exception):
    def __init__(self, line):
        super(TooFewTokens, self).__init__(
            'too few tokens, line={}'.format(line)
        )


class ExtraToken(Exception):
    def __init__(self, type, count=None, line=0):
        if count is None:
            count, token = 'one', 'token'
        else:
            token = 'tokens'
        super(ExtraToken, self).__init__(
            '{} must have {} {}, line={}'.format(type, count, token, line)
        )


class DuplicateName(Exception):
    def __init__(self, type, line):
        super(DuplicateName, self).__init__(
            'duplicate {} name, line={}'.format(type, line)
        )


class DuplicateDirective(Exception):
    def __init__(self, directive, line):
        super(DuplicateDirective, self).__init__(
            "duplicate directive '{}', line={}".format(directive, line)
        )


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
            for event in state['events'].values():
                events.append(event['name'])
        return list(set(events))


def act_state(context):
    if len(context.line.split()) != 1:
        raise ExtraToken('STATE', line=context.line_num)
    name = context.line.strip()
    if name in context.states.keys():
        raise DuplicateName('STATE', context.line_num)
    if context.first_state is None:
        context.first_state = name
    context.state = dict(name=name, enter=None, exit=None, events={})
    context.states[name] = context.state


def act_enter(context):
    if len(context.line.split()) != 1:
        raise ExtraToken('ENTER', line=context.line_num)
    name = context.line.strip()
    if context.state['enter'] is not None:
        raise DuplicateDirective('ENTER', context.line_num)
    context.state['enter'] = name
    context.add_action(name)


def act_exit(context):
    if len(context.line.split()) != 1:
        raise ExtraToken('EXIT', line=context.line_num)
    name = context.line.strip()
    if context.state['exit'] is not None:
        raise DuplicateDirective('EXIT', context.line_num)
    context.state['exit'] = name
    context.add_action(name)


def act_event(context):
    if len(context.line.split()) == 2:
        name, next_state = context.line.strip().split()
    elif len(context.line.split()) != 1:
        raise ExtraToken('EVENT', 'one or two', context.line_num)
    else:
        name = context.line.strip()
        next_state = None
    context.event = dict(name=name, actions=[], next=next_state)
    context.state['events'][name] = context.event


def act_action(context):
    if len(context.line.split()) != 1:
        raise ExtraToken('ACTION', line=context.line_num)
    name = context.line.strip()
    if name in context.event['actions']:
        raise DuplicateName('ACTION', context.line_num)
    context.event['actions'].append(name)
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
    if context.context:
        handler = partial(handler, context.context)
    context.handlers[name] = handler