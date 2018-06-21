""" MIT License
https://github.com/robertchase/fsm/blob/master/LICENSE
"""
from __future__ import absolute_import
from functools import partial

from ergaleia.load_from_path import load_lines_from_path
from ergaleia.un_comment import un_comment

import fsm.actions as fsm_actions
from fsm.fsm_machine import create as create_machine
import fsm.FSM as FSM


class UnexpectedDirective(Exception):
    def __init__(self, directive, line):
        super(UnexpectedDirective, self).__init__(
            "unexpected directive '{}', line={}".format(directive, line)
        )


class Parser(object):

    def __init__(self):

        self.context = ctx = fsm_actions.Context()

        self.fsm = create_machine(
            action=partial(fsm_actions.act_action, ctx),
            context=partial(fsm_actions.act_context, ctx),
            enter=partial(fsm_actions.act_enter, ctx),
            event=partial(fsm_actions.act_event, ctx),
            exit=partial(fsm_actions.act_exit, ctx),
            handler=partial(fsm_actions.act_handler, ctx),
            state=partial(fsm_actions.act_state, ctx),
        )
        self.fsm.state = 'init'

    def __str__(self):
        context = self.context
        states = context.states
        d = 'from fsm.FSM import STATE, EVENT, FSM\n'
        d += '\n'.join('# ' + a for a in context.actions)
        d += '\ndef create(**actions):\n'
        d += '\n'.join(self.define(s) for s in states.values())
        d += '\n' + '\n'.join(self.set_events(s) for s in states.values())
        d += '\n  return FSM([' + ','.join('S_' + s for s in states) + '])'
        return d

    @property
    def first_state(self):
        return self.context.first_state

    @property
    def actions(self):
        return self.context.actions

    @property
    def events(self):
        return self.context.events

    @classmethod
    def parse(cls, data):
        parser = cls()
        context = parser.context
        for num, line in enumerate(
                    un_comment(load_lines_from_path(data, 'fsm')),
                    start=1
                ):
            if not line:
                continue
            line = line.split(' ', 1)
            if len(line) == 1:
                raise fsm_actions.TooFewTokens(line[0], num)

            event, context.line = line
            context.line_num = num

            if not parser.fsm.handle(event.lower()):
                raise UnexpectedDirective(event, num)
        return parser

    def build(self, **actions):
        states = {}
        for state in self.states.values():
            s = FSM.STATE(
                name=state['name'],
                enter=actions[state['enter']] if state['enter'] else None,
                exit=actions[state['exit']] if state['exit'] else None,
            )
            states[s.name] = s
            for event in state['events'].values():
                e = FSM.EVENT(
                    name=event['name'],
                    actions=[actions[n] for n in event['actions']],
                    next_state=event['next'],
                )
                s.events[e.name] = e
        for state in states.values():
            for event in state.events.values():
                if event.next_state:
                    event.next_state = states[event.next_state]
        fsm = FSM.FSM(states.values())
        fsm.state = self.first_state
        return fsm

    @staticmethod
    def define(state):
        s = "  S_%s=STATE('%s'" % (state['name'], state['name'])
        if state['enter']:
            s += ",enter=actions['%s']" % state['enter']
        if state['exit']:
            s += ",exit=actions['%s']" % state['exit']
        return s + ')'

    @staticmethod
    def set_events(state):
        s = "  S_%s.set_events([" % state['name']
        for e in state['events'].values():
            s += "EVENT('%s',[" % e['name']
            s += ','.join("actions['%s']" % a for a in e['actions'])
            s += ']'
            if e['next']:
                s += ', S_%s' % e['next']
            s += "),"
        s += '])'
        return s


if __name__ == '__main__':
    import sys

    f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    fsm = Parser.parse(f.readlines())
    print(fsm)
