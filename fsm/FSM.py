""" MIT License
https://github.com/robertchase/fsm/blob/master/LICENSE
"""


class STATE (object):

    def __init__(self, name, enter=None, exit=None):
        self.name = name
        self.events = {}
        self.enter = enter
        self.exit = exit

    def set_events(self, events):
        for event in events:
            self.events[event.name] = event


class EVENT (object):

    def __init__(self, name, actions, next_state=None):
        self.name = name
        self.actions = actions
        self.next_state = next_state


class FSM (object):

    def __init__(self, states):
        self.states = {}
        for state in states:
            self.states[state.name] = state
        self._state = None
        self.on_state_change = None
        self.trace = None
        self.undefined = None

    @property
    def state(self):
        return self._state.name

    @state.setter
    def state(self, state):
        self._state = self.states[state]

    def _handle(self, event):
        next_event = None

        for action in event.actions:
            next_event = action()

        if event.next_state:
            if self._state.exit:
                next_event = self._state.exit()

            if self.on_state_change:
                self.on_state_change(event.next_state.name, self._state.name)
            self._state = event.next_state

            if self._state.enter:
                next_event = self._state.enter()

        return next_event

    def handle(self, event):
        is_internal = False

        while event:
            is_default = False

            # --- locate event handler
            if event in self._state.events:
                state_event = self._state.events[event]

            # --- or default event handler
            elif 'default' in self._state.events:
                is_default = True
                state_event = self._state.events['default']

            # --- or oops
            else:
                state_event = None

            # --- trace
            if self.trace:
                self.trace(self._state.name, event, is_default, is_internal)

            # --- no event handler
            if not state_event:
                if self.undefined:
                    self.undefined(self._state.name, event, False, is_internal)
                return False  # event not handled!

            # --- handle, if non-null event is returned, keep going
            event = self._handle(state_event)
            is_internal = True  # every event after the first event is internal

        return True  # OK
