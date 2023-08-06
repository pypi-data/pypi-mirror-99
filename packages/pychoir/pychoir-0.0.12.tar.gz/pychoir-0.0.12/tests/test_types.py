from decimal import Decimal

from pychoir import ConvertsTo, IsInstance, OfType


def test_is_instance():
    assert OfType is IsInstance

    assert [1] == [IsInstance(int)]
    assert {'a': 'abc'} == {'a': IsInstance(str)}
    assert not ['abc'] == [IsInstance(int)]

    assert str([IsInstance(int)]) == '[IsInstance(int)]'


def test_converts_to():
    assert ['1'] == [ConvertsTo(int)]
    assert '1' == ConvertsTo(Decimal)
    assert 'asd' != ConvertsTo(int)
    assert [] != ConvertsTo(Decimal)

    assert str(ConvertsTo(int)) == 'ConvertsTo(int)'
    assert str(ConvertsTo(Decimal)) == 'ConvertsTo(Decimal)'
