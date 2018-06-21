import pytest

import fsm.actions as actions


@pytest.fixture
def context():
    c = actions.Context()
    c.line_num = 10
    return c


def test_state(context):
    assert len(context.states) == 0
    context.line = 'one'
    actions.act_state(context)
    assert len(context.states) == 1
    assert context.states['one']


def test_first_state(context):
    assert context.first_state is None
    context.line = 'one'
    actions.act_state(context)
    assert context.first_state == 'one'
    context.line = 'two'
    actions.act_state(context)
    assert context.first_state == 'one'


def test_state_extra_token(context):
    context.line = 'one two'
    with pytest.raises(actions.ExtraToken):
        actions.act_state(context)


def test_state_duplicate(context):
    context.line = 'one'
    actions.act_state(context)
    with pytest.raises(actions.DuplicateName):
        actions.act_state(context)


@pytest.fixture
def context_state(context):
    context.line = 'one'
    actions.act_state(context)
    return context


def test_enter(context_state):
    context_state.line = 'two'
    actions.act_enter(context_state)


def test_enter_extra_token(context_state):
    context_state.line = 'two three'
    with pytest.raises(actions.ExtraToken):
        actions.act_enter(context_state)


def test_enter_duplicate_directive(context_state):
    context_state.line = 'two'
    actions.act_enter(context_state)
    with pytest.raises(actions.DuplicateDirective):
        actions.act_enter(context_state)


def test_exit(context_state):
    context_state.line = 'two'
    actions.act_exit(context_state)


def test_exit_extra_token(context_state):
    context_state.line = 'two three'
    with pytest.raises(actions.ExtraToken):
        actions.act_exit(context_state)


def test_exit_duplicate_directive(context_state):
    context_state.line = 'two'
    actions.act_exit(context_state)
    with pytest.raises(actions.DuplicateDirective):
        actions.act_exit(context_state)


def test_event(context_state):
    context_state.line = 'two'
    actions.act_event(context_state)
    context_state.line = 'three four'
    actions.act_event(context_state)


def test_event_extra_token(context_state):
    context_state.line = 'two three four'
    with pytest.raises(actions.ExtraToken):
        actions.act_event(context_state)


@pytest.fixture
def context_event(context_state):
    context_state.line = 'one'
    actions.act_event(context_state)
    return context_state


def test_action(context_event):
    context_event.line = 'one'
    actions.act_action(context_event)


def test_action_extra_token(context_event):
    context_event.line = 'one two'
    with pytest.raises(actions.ExtraToken):
        actions.act_action(context_event)


def test_action_duplicate_name(context_event):
    context_event.line = 'one'
    actions.act_action(context_event)
    with pytest.raises(actions.DuplicateName):
        actions.act_action(context_event)
        actions.act_action(context_event)


def test_context(context):
    assert context.context is None
    context.line = 'fsm.actions.act_context'
    actions.act_context(context)
    assert context.context


def test_context_extra_token(context):
    context.line = 'one two'
    with pytest.raises(actions.ExtraToken):
        actions.act_context(context)


def test_context_duplicate_name(context):
    context.line = 'fsm.actions.act_context'
    actions.act_context(context)
    with pytest.raises(actions.DuplicateName):
        actions.act_context(context)


def test_handler(context):
    assert len(context.handlers) == 0
    context.line = 'one fsm.actions.act_context'
    actions.act_handler(context)
    assert len(context.handlers) == 1


def test_handler_too_few_tokens(context):
    context.line = 'one'
    with pytest.raises(actions.TooFewTokens):
        actions.act_handler(context)


def test_handler_extra_token(context):
    context.line = 'one two three'
    with pytest.raises(actions.ExtraToken):
        actions.act_handler(context)


def test_handler_duplicate_name(context):
    context.line = 'one fsm.actions.act_context'
    actions.act_handler(context)
    with pytest.raises(actions.DuplicateName):
        actions.act_handler(context)
