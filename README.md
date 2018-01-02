# FSM

### Finite State Machine for Python

The `fsm` project allows a state-event machine to be built and executed
in python code.

The `fsm` is defined in a mini-language (DSL) which is compiled to python code,
allowing it to respond to `events` and call `action` routines in accordance with
the state machine definition.

### An example

Here is a trivial state machine for a push-button light switch.

```
STATE off
  EVENT press on
    ACTION turn_on
STATE on
  EVENT press off
    ACTION turn_off
```

The machine starts in the state `off`. When the `press` event arrives, the action
`turn_on` is executed, and the machine transisions to the state `on`.
When the `press` event arrives in the state `on`, the action `turn_off` is
executed, and the machine transistions back to the state `off`.

This example demonstrates the key ideas of a finite state machine:

* `events` arrive while the machine is in a `state`
* `events` can trigger an `action` or series of `actions`
* `events` can trigger a transition to a different `state`

Let's add some more logic to this machine:

```
STATE off
  EVENT press on
    ACTION turn_on
STATE on
  ENTER test
  EVENT on
  EVENT off off
  EVENT press off
    ACTION turn_off
```

It might be the case that the button is faulty, or the light is missing or broken.
A new `action` has been created called *test*, which can verify that the light is on.
It *emits* an `event` of `on` or `off`, based upon what it discovers.

An `enter` `action` has been added to the state `on`.
The `enter` action is triggered when the `on` `state` is entered.
This `action` tests if the light is on.
Nothing happens if the *test* `action` emits the `event` `on`; if the
event `off` is emitted, the machine transitions back to `state` `off`.

The same logic can be defined in this way:

```
STATE off
  EVENT press
    ACTION turn_on
    ACTION test
  EVENT on on
  EVENT off
STATE on
  EVENT press off
    ACTION turn_off
```

The *test* `action` is executed as part of the `press` event in state `off`, and
a transition to state `on` only happens if the *test* `action` returns an `on` event.

A key takeaway from comparing these two state machines is that the *test* `action`
works in either state. Action routines are meant to be very small pieces of
code which operate without regard to state.

The `if/elif/else` logic which would normally accompany these state management
problems is abstracted into the `fsm` definition, and the coding is simplified
into a collection of focused action routines.

### So, how does this work with python?

##### Parsing

If we have an fsm description file named `switch.fsm` in a module
named `my_switch`. The unix path to this file is, starting with the top level
directory of the module, `my_switch/switch.fsm`. The following code will parse this file:
```
from fsm.parser import Parser as parser
description = parser.parse('my_switch.switch.fsm')
```

Using dot-notation to specify the location within the module allows the fsm description
file to be located anywhere in `PYTHONPATH`.

The `parse` function will also accept an os-specific file path, or a list of strings,
where each string acts as a line from a file.
```
description = parser.parse([
    'STATE off',
    '  EVENT press on',
    '    ACTION turn_on',
    'STATE on',
    '  EVENT press off',
    '    ACTION turn_off',
])
```
It is best practice to keep the `fsm` description in a separate file within
the python directory structure, accessed with dot-notation.
Tests, or other special cases, may find the
alternative methods helpful.

##### Actions

Once an `fsm` file has been parsed, `action` routines must be written for each
`action`. The actions are obvious by inspection, but can be easily gotten
from the parsed description:
```
>>> description.actions
['turn_off', 'turn_on']
```

Here are two trivial implementations:
```
def turn_off():
    print('the light is off')

def turn_on():
    print('the light is on')
```

##### Initalize the machine

Combine the description and the actions to create a new machine:

```
fsm = description.build(
    turn_off=turn_off,
    turn_on=turn_on,
)
```

##### Run the machine

The machine accepts events with the `handle` method. If `handle` is able to
process the `event` in the current state, it returns `True`.

Let's try it out:
```
>>> fsm.handle('press')
the light is on
True
>>> fsm.handle('press')
the light is off
True
>>> fsm.handle('press')
the light is on
True
```
Notice that the `event` is simply a string.

If we pass an unrecognized event:
```
>>> fsm.handle('huh')
False
```

### More fun

More examples and reference documenation can be found in the `/doc` directory of the repo.
