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

Leading white space is ignored, although it can help distinguish between
different parts of the file.

## Directives

### STATE

```
STATE state_name
```

The `state` directive defines the start of a new `state`. All subsequent
directives will apply to this `state` until a new
`state`, `context` or `handler`
directive is encountered.
A `state`'s name must be unique within the `fsm`.

### EVENT

```
EVENT event_name <new_state>
```

The `event` directive describes what happens when an `event` arrives
while the `fsm` is in the current `state`.
Any subsequent `action` directives will apply to this `event` until a non-`action`
directive is encountered.

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
This feature allows a single external event to trigger an arbitrarily long
sequence of `state`/`event` processes.

When an `event` causes an `fsm` `state` transition,
then *return value handling* is different:

##### state-transition return value handling

If an `event` transitions the `fsm` to a new `state`,
then any `event` returned from the last `action`
will be handled in the new `state`.
The last `action` is the last of:

- the last `action` defined for the `event` that caused the transition
- the `exit` `action` of the `state` being transitioned from
- the `enter` `action` of the `state` being transitioned to

The only `event` returned from an `action` that matters, is the `event`
returned from the *last* `action`.
Any other returned `event` is ignored.

##### action routine context

If a set of `action` routines needs to operate against a shared context,
then those routines can be specified as methods on a context object.
The `fsm` does not need to be aware of this.
Alternatively, the action routines can share a context as defined in
the `context` directive below.

### CONTEXT

```
CONTEXT path
```

The `context` directive defines a shared object to be passed to each
`action` routine.

The `path` is a dot-delimited path to a callable which is
invoked with the `args` and `kwargs` of the parser's `load`
method, returning an object.

The `context` directive only works with `action` routines defined
with the `handler` directive, and loaded with the `load` method.

### HANDLER

```
HANDLER name path
```

The `handler` directive defines a callable to be invoked for
an `action` defined in the finite state machine.

### EXCEPTION

```
EXCEPTION path
```

The `exception` directive defines a handler to be invoked
if an `action routine` raises an `Exception`.
The handler is provided with the `Exception` object.
If `CONTEXT` is defined,
the handler is provided with the `context` followed by the `Exception`.

The handler can return an `event` name, which will
be handled in the current `state`.

If not defined, an `Exception` will not be handled by the `FSM`.

### DEFAULT

```
DEFAULT event_name <new_state>
```

The `default` directive defines an `event` that is global
to the `FSM`. If an `event` arrives in a `state` for which the
`event` is not defined, then the `default` event, if specified, will
be used. A `default` event is processed in the current `state`.

Any subsequent `action` directives will apply to this `event` until a
non-`action`
directive is encountered.

If a `new_state` argument is specified,
the `fsm` will transition to that `state` after processing any
`action` directives associated with the `event`.
