import sys
from abc import ABC, abstractmethod
from contextlib import contextmanager
from enum import Enum
from typing import Any, Callable, Iterator, List, Optional, Tuple, Type, TypeVar, Union

from pychoir.utils import sequence_or_its_only_member

MatchedType = TypeVar('MatchedType', bound=Any)

if sys.version_info >= (3, 8):
    from typing import Protocol

    class Matchable(Protocol):
        """Type for a value that can be matched against using the :code:`==` operator (has the :code:`__eq__()` method).
        In the pychoir API, you can typically pass `Matcher` s and/or normal values where `Matchable` s are expected.
        """
        def __eq__(self, other: MatchedType) -> bool:
            ...  # pragma: no cover
else:
    Matchable = Any


if sys.version_info >= (3, 8):
    from typing import final
else:
    CallableT = TypeVar('CallableT', bound=Callable)

    def final(x: CallableT) -> CallableT:
        return x


T = TypeVar('T')


class _MatcherStatus(str, Enum):
    NOT_RUN = 'NOT RUN'
    PASSED = 'PASSED'
    FAILED = 'FAILED'


class _MatcherState:
    def __init__(self, status: _MatcherStatus = _MatcherStatus.NOT_RUN):
        self.__status: _MatcherStatus = status
        self.__failed_values: List[Any] = []

    def update(self, passed: bool, value: Any) -> None:
        if passed:
            self.__add_success()
        else:
            self.__add_failure(value)

    def reset_failures(self) -> None:
        if self.__status == _MatcherStatus.FAILED:
            self.__status = _MatcherStatus.NOT_RUN
            self.__failed_values = []

    @property
    def status(self) -> _MatcherStatus:
        return self.__status

    @property
    def failed_values(self) -> Tuple[Any, ...]:
        return tuple(self.__failed_values)

    @property
    def was_already_run(self) -> bool:
        return self.status != _MatcherStatus.NOT_RUN

    def __add_failure(self, value: Any) -> None:
        self.__status = _MatcherStatus.FAILED
        self.__failed_values.append(value)

    def __add_success(self) -> None:
        if not self.was_already_run:
            self.__status = _MatcherStatus.PASSED


class _MatcherContext:
    def __init__(self, mismatch_expected: bool, nested_call: bool) -> None:
        self.__mismatch_expected = mismatch_expected
        self.__nested_call = nested_call

    @property
    def mismatch_expected(self) -> bool:
        return self.__mismatch_expected

    @property
    def nested_call(self) -> bool:
        return self.__nested_call


class Matcher(ABC):
    """The baseclass for all Matchers."""
    def __init__(self, override_name: Optional[str] = None) -> None:
        super().__init__()
        self.__name = override_name if override_name is not None else self.__class__.__name__
        self.__state = _MatcherState()
        self.__context: Optional[_MatcherContext] = None

    def as_(self, type_: Type[T]) -> T:
        """To make matchers pass type checking."""
        return self  # type: ignore

    @final
    def nested_match(
        self,
        matcher: Union['Matcher', Matchable],
        other: MatchedType,
        expect_mismatch: bool = False
    ) -> bool:
        """For evaluating Matchables (or calling Matchers) from inside a Matcher.

        Takes care of passing all necessary context and updating state when matching.

        :param matcher: The value or Matcher to compare against.
        :param other: The value being compared.
        :param expect_mismatch: Set to True when expecting a mismatch (for example in :class:`Not`).
        """
        if self.__context is not None and self.__context.mismatch_expected:
            expect_mismatch = not expect_mismatch

        if isinstance(matcher, Matcher):
            return matcher.matches(other, _MatcherContext(mismatch_expected=expect_mismatch, nested_call=True))
        else:
            return matcher == other

    @final
    def nested_reset(
        self,
        matcher: Union['Matcher', Matchable],
    ) -> None:
        """For resetting failure state of child matchers in case of passing due to other Matchers.

        For example in :class:`Or`, it is enough that one child Matcher passes.
        The matchers tried up to that point should not report failure.
        After a match, :class:`Or` should call `self.nested_reset(matcher)` for all its Matchers.

        :param matcher: The value or Matcher to reset (nothing will be done for non-Matchers).
        """
        if isinstance(matcher, Matcher):
            return matcher.__state.reset_failures()

    @final
    @property
    def expected_result(self) -> bool:
        if self.__context is None:
            raise RuntimeError('expected_result is only available while in match context')
        return not self.__context.mismatch_expected

    @abstractmethod
    def _matches(self, other: MatchedType) -> bool:
        """Returns True when Matcher matches, False otherwise.

        :param other: The value being compared.

        **To be implemented by all Matchers.**
        """
        ...  # pragma: no cover

    @abstractmethod
    def _description(self) -> str:
        """Returns a textual representation of the Matcher's parameters.

        For example in :code:`"EqualTo('foo')"` the :code:`'foo'` is returned by :code:`_description()`.

        **To be implemented by all Matchers.**
        """
        ...  # pragma: no cover

    @final
    def matches(self, other: MatchedType, context: _MatcherContext) -> bool:
        with self.__set_context(context):
            passed = self._matches(other)

        reported_passed = passed if not context.mismatch_expected else not passed
        self.__state.update(reported_passed, other)

        return passed

    @final
    def __eq__(self, other: MatchedType) -> bool:
        return self.matches(other, _MatcherContext(mismatch_expected=False, nested_call=False))

    @final
    def __ne__(self, other: MatchedType) -> bool:
        return not self.matches(other, _MatcherContext(mismatch_expected=True, nested_call=False))

    @final
    def __str__(self) -> str:
        return self.__describe()

    @final
    def __repr__(self) -> str:
        return self.__describe()

    @final
    def __describe(self) -> str:
        failed_value = sequence_or_its_only_member(self.__state.failed_values)
        status_str = f'[FAILED for {failed_value!r}]' if self.__state.status == _MatcherStatus.FAILED else ''
        return f'{self.__name}({self._description()}){status_str}'

    @final
    @contextmanager
    def __set_context(self, context: _MatcherContext) -> Iterator[None]:
        self.__context = context
        yield
        self.__context = None


class MatchWrapper:
    def __init__(self, value: MatchedType, matcher: Matcher, did_match: bool):
        self.value = value
        self.matcher = matcher
        self.did_match = did_match

    def __bool__(self) -> bool:
        return self.did_match

    def __str__(self) -> str:
        return f'that({self.value!r}).matches({self.matcher})'

    def __repr__(self) -> str:
        return str(self)


class MatcherWrapper:
    def __init__(self, value: MatchedType):
        self.value = value

    def matches(self, matcher: Matcher) -> MatchWrapper:
        """
        :param matcher: The Matcher to compare `that(value)` with
        :return: a truthy value in case `that(value)` passes the given `matcher`
        """
        context = _MatcherContext(mismatch_expected=False, nested_call=False)
        did_match = matcher.matches(self.value, context)
        return MatchWrapper(self.value, matcher, did_match)


def that(value: MatchedType) -> MatcherWrapper:
    """
    A helper for syntactically sugar coating matches instead of using `==`.

    :param value: The value to pass into the Matcher in `MatcherWrapper.matches()`
    :return: A :class:`MatcherWrapper`

    Usage:
      >>> from pychoir import that, GreaterThan
      >>> assert that(3).matches(GreaterThan(2))
      ...
      >>> assert that(1).matches(GreaterThan(2))
      Traceback (most recent call last):
      ...
      AssertionError
    """
    return MatcherWrapper(value)


class Transformer(ABC):
    @abstractmethod
    def __call__(self, matcher: Matchable) -> Matcher:
        ...
