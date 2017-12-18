# FSM File
## A Reference Guide

An `fsm` file describes a finite state machine
as an object in one of a set of `states`,
each of which reacts to `events` by
executing `actions` and transitioning to other `states`.
Yeah.

## Structure of an `fsm` file

An `fsm` file is a set of single-line directives that each specify some aspect of a
finite state machine.

A directive starts with a directive-type token followed by some arguments. For example:

```
STATE init
```

This record's directive-type is *STATE*, and the argument value *init* is specified.
The directive-type is case insensitive, although, upper case helps legibility.
The argument values *are* case sensitive.

Leading white space is ignored, although it can help distingish between
different parts of the file.

## Directives

### STATE

```
STATE state_name
```

The `state` directive defines the start of a new `state`. All subsequent
directives will apply to this `state` until a new `state` directive is encountered.
A `state`'s name must be unique within the `fsm`.

### EVENT

```
EVENT event_name <new_state>
```

The `event` directive describes what happens when an `event` arrives
while the `fsm` is in the current `state`.
Any subsequent `action` directives will apply to this `event` until a new `state`,
`event`, `enter` or `exit` directive is encountered.

If a `new_state` argument is specified,
the `fsm` will transition to that `state` after processing any
`action` directives associated with the `event`.

### ACTION

```
ACTION action_name
```

The `action` directive defines the name of an `action` routine to be executed.

##### the action routine

An `action` routine is a *callable* that is executed without any arguments from the
`fsm`. An `action` routine may return a single string result which must match
an `event` name in the `fsm`.

##### return value handling

If an `action` routine returns an `event` name **and** the `action` directive
is the last directive defined for the currently processing `event`, then the
returned `event` name is immediately handled by the `fsm`.
This feature allows a single external event to trigger an aritrarily long
sequence of `state`/`event` processes.

##### state-transition return value handling

If an `event` transitions to a new state, then the returned `event` name
from the last `action` routine will be handled in the new `state`.

##### action routine context

If a set of `action` routines needs to operate against a shared context,
then those routines can be specified as methods on a context object.
The `fsm` does not need to be aware of this.
