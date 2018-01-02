""" MIT License
https://github.com/robertchase/fsm/blob/master/LICENSE
"""
from __future__ import absolute_import
from ergaleia.load_from_path import load_lines_from_path
from ergaleia.un_comment import un_comment
from fsm.fsm_machine import create as create_machine
import fsm.FSM as FSM


class Parser(object):

    def __init__(self):
        self.error = None
        self.states = {}
        self.first_state = None
        self.state = None
        self.event = None
        self._actions = {}
        self.fsm = create_machine(
            action=self.act_action,
            enter=self.act_enter,
            event=self.act_event,
            exit=self.act_exit,
            state=self.act_state,
        )
        self.fsm.state = 'init'

    def __str__(self):
        states = self.states
        d = 'from fsm.FSM import STATE, EVENT, FSM\n'
        d += '\n'.join('# ' + a for a in sorted(self._actions))
        d += '\ndef create(**actions):\n'
        d += '\n'.join(self.define(s) for s in states.values())
        d += '\n' + '\n'.join(self.set_events(s) for s in states.values())
        d += '\n  return FSM([' + ','.join('S_' + s for s in states) + '])'
        return d

    @property
    def actions(self):
        return sorted(self._actions.keys())

    @property
    def events(self):
        events = []
        for state in self.states.values():
            for event in state['events'].values():
                events.append(event['name'])
        return list(set(events))

    @classmethod
    def parse(cls, data):
        data = load_lines_from_path(data, 'fsm')
        parser = cls()
        for num, line in enumerate(data, start=1):
            line = un_comment(line)
            if not line:
                continue
            line = line.split(' ', 1)
            if len(line) == 1:
                raise Exception('too few tokens, line=%d' % num)

            event, parser.line = line
            if not parser.fsm.handle(event.lower()):
                raise Exception(
                    "Unexpected directive '{}', line={}".format(event, num)
                )
            if parser.error:
                raise Exception('%s, line=%d' % (parser.error, num))
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

    def act_state(self):
        if len(self.line.split()) != 1:
            self.error = 'STATE name must be a single token'
            return 'error'
        name = self.line.strip()
        if name in self.states.keys():
            self.error = 'duplicate STATE name'
            return 'error'
        if self.first_state is None:
            self.first_state = name
        self.state = dict(name=name, enter=None, exit=None, events={})
        self.states[name] = self.state

    def act_enter(self):
        if len(self.line.split()) != 1:
            self.error = 'ENTER action must be a single token'
            return 'error'
        name = self.line.strip()
        if self.state['enter'] is not None:
            self.error = 'only one ENTER action allowed'
            return 'error'
        self.state['enter'] = name
        self._actions[name] = True

    def act_exit(self):
        if len(self.line.split()) != 1:
            self.error = 'EXIT action must be a single token'
            return 'error'
        name = self.line.strip()
        if self.state['exit'] is not None:
            self.error = 'only one EXIT action allowed'
            return 'error'
        self.state['exit'] = name
        self._actions[name] = True

    def act_event(self):
        if len(self.line.split()) == 2:
            name, next_state = self.line.strip().split()
        elif len(self.line.split()) != 1:
            self.error = 'EVENT can only have one or two tokens'
            return 'error'
        else:
            name = self.line.strip()
            next_state = None
        self.event = dict(name=name, actions=[], next=next_state)
        self.state['events'][name] = self.event

    def act_action(self):
        if len(self.line.split()) != 1:
            self.error = 'ACTION can only have one token'
            return 'error'
        name = self.line.strip()
        if name in self.event['actions']:
            self.error = 'duplicate ACTION name'
            return 'error'
        self.event['actions'].append(name)
        self._actions[name] = True


if __name__ == '__main__':
    import sys

    f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    fsm = Parser.parse(f.readlines())
    print(fsm)
