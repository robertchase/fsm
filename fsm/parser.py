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

        self.ctx = fsm_actions.Context()

        self.fsm = create_machine(
            action=partial(fsm_actions.act_action, self.ctx),
            context=partial(fsm_actions.act_context, self.ctx),
            enter=partial(fsm_actions.act_enter, self.ctx),
            event=partial(fsm_actions.act_event, self.ctx),
            exit=partial(fsm_actions.act_exit, self.ctx),
            handler=partial(fsm_actions.act_handler, self.ctx),
            state=partial(fsm_actions.act_state, self.ctx),
        )
        self.fsm.state = 'init'

    def __str__(self):
        states = self.states
        d = 'from fsm.FSM import STATE, EVENT, FSM\n'
        d += '\n'.join('# ' + a for a in self.actions)
        d += '\ndef create(**actions):\n'
        d += '\n'.join(self.define(s) for s in states.values())
        d += '\n' + '\n'.join(self.set_events(s) for s in states.values())
        d += '\n  return FSM([' + ','.join('S_' + s for s in states) + '])'
        return d

    @property
    def first_state(self):
        return self.ctx.first_state

    @property
    def actions(self):
        return self.ctx.actions

    @property
    def states(self):
        return self.ctx.states

    @property
    def events(self):
        return self.ctx.events

    @property
    def context(self):
        return self.ctx.context

    @property
    def handlers(self):
        return self.ctx.handlers

    @classmethod
    def parse(cls, data):
        parser = cls()
        ctx = parser.ctx
        for num, line in enumerate(
                    un_comment(load_lines_from_path(data, 'fsm')),
                    start=1
                ):
            if not line:
                continue
            line = line.split(' ', 1)
            if len(line) == 1:
                raise fsm_actions.TooFewTokens(line[0], num)

            event, ctx.line = line
            ctx.line_num = num

            if not parser.fsm.handle(event.lower()):
                raise UnexpectedDirective(event, num)
        return parser

    @classmethod
    def load(cls, path, *args, **kwargs):
        p = cls.parse(path)
        p.bind(*args, **kwargs)
        return p.build(**p.ctx.handlers)

    def bind(self, *args, **kwargs):
        if self.context:
            self.context = self.context(*args, **kwargs)
            for n, h in self.handlers.items():
                self.handlers[n] = partial(h, self.context)

    def build(self, **actions):
        states = {}
        for state in self.states.values():
            s = FSM.STATE(
                name=state.name,
                enter=actions[state.enter] if state.enter else None,
                exit=actions[state.exit] if state.exit else None,
            )
            states[s.name] = s
            for event in state.events.values():
                e = FSM.EVENT(
                    name=event.name,
                    actions=[actions[n] for n in event.actions],
                    next_state=event.next_state,
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
        s = "  S_{0}=STATE('{0}'".format(state.name)
        if state.enter:
            s += ",enter=actions['{}']".format(state.enter)
        if state.exit:
            s += ",exit=actions['{}']".format(state.exit)
        return s + ')'

    @staticmethod
    def set_events(state):
        s = "  S_{}.set_events([".format(state.name)
        for e in state.events.values():
            s += "EVENT('{}',[".format(e.name)
            s += ','.join("actions['{}']".format(a) for a in e.actions)
            s += ']'
            if e.next_state:
                s += ', S_{}'.format(e.next_state)
            s += "),"
        s += '])'
        return s


if __name__ == '__main__':
    import sys

    f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    parser = Parser.parse(f.readlines())
    print(parser)
