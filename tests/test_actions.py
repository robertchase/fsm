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
