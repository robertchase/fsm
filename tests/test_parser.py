import pytest
import fsm.parser as parser
import fsm.actions as actions


def test_basic():
    assert parser.Parser()


def test_too_few_tokens():
    with pytest.raises(parser.TooFewTokens):
        parser.Parser.parse([
            'FOO',
        ])


def test_unexpected_directive():
    with pytest.raises(parser.UnexpectedDirective):
        parser.Parser.parse([
            'FOO bar',
        ])


def test_extra_token():
    with pytest.raises(actions.ExtraToken):
        parser.Parser.parse([
            'STATE foo bar',
        ])
    with pytest.raises(actions.ExtraToken):
        parser.Parser.parse([
            'STATE foo',
            'ENTER foo bar',
        ])
    with pytest.raises(actions.ExtraToken):
        parser.Parser.parse([
            'STATE foo',
            'EXIT foo bar',
        ])


def test_duplicate_state_name():
    parser.Parser.parse([
        'STATE foo',
    ])
    with pytest.raises(actions.DuplicateName):
        parser.Parser.parse([
            'STATE foo',
            'STATE foo',
        ])


def test_duplicate_action_name():
    parser.Parser.parse([
        'STATE foo',
        'EVENT foo',
        'ACTION foo',
    ])
    with pytest.raises(actions.DuplicateName):
        parser.Parser.parse([
            'STATE foo',
            'EVENT foo',
            'ACTION foo',
            'ACTION foo',
        ])


def test_duplicate_enter_directive():
    parser.Parser.parse([
        'STATE foo',
        'ENTER bar',
    ])
    with pytest.raises(actions.DuplicateDirective):
        parser.Parser.parse([
            'STATE foo',
            'ENTER bar',
            'ENTER none'
        ])


def test_duplicate_exit_directive():
    parser.Parser.parse([
        'STATE foo',
        'EXIT bar',
    ])
    with pytest.raises(actions.DuplicateDirective):
        parser.Parser.parse([
            'STATE foo',
            'EXIT bar',
            'EXIT none'
        ])


def test_comment():
    p = parser.Parser().parse([
        'STATE one # two',
    ])
    assert p
    assert p.first_state == 'one'
