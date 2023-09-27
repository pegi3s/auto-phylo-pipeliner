from typing import TypeVar, Generic, Optional, Tuple, Any, Callable, Union

from hamcrest import has_entries
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

T = TypeVar("T")
A = TypeVar("A")


class AssertionBuilder(Generic[A]):
    def __init__(self, expected_entity: A, actual_entity: A):
        self._expected_entity: A = expected_entity
        self._actual_entity: A = actual_entity

    def _get_field_values(self, field: str) -> Tuple[Any, Any]:
        return getattr(self._expected_entity, field), getattr(self._actual_entity, field)

    def and_is_true(self, evaluation: Callable[[A, A], bool],
                    message: Union[Callable[[bool], str], str]) -> "AssertionBuilder[A]":
        return self.is_true(evaluation, message)

    def is_true(self, evaluation: Callable[[A, A], bool],
                message: Union[Callable[[bool], str], str]) -> "AssertionBuilder[A]":
        if not evaluation(self._expected_entity, self._actual_entity):
            raise AssertionError(message)

        return self

    def and_has_same(self, field: str, matcher: Optional[Callable[[T], Matcher[Any]]] = None) -> "AssertionBuilder[A]":
        return self.has_same(field, matcher)

    def has_same(self, field: str, matcher: Optional[Callable[[T], Matcher[Any]]] = None) -> "AssertionBuilder[A]":
        match, description = self._compare_with_matcher(field, lambda e, a: e == a, matcher)

        if not match:
            expected_value, actual_value = self._get_field_values(field)
            if description is not None:
                raise AssertionError(
                    f"Field {field} should be {expected_value} but was {actual_value}"
                    f"The cause was: {description}"
                )
            else:
                raise AssertionError(f"Field {field} should be {expected_value} but was {actual_value}")
        else:
            return self

    def and_has_same_dict(self, field: str) -> "AssertionBuilder[A]":
        return self.has_same_dict(field)

    def has_same_dict(self, field: str) -> "AssertionBuilder[A]":
        expected_value, actual_value = self._get_field_values(field)

        if not has_entries(expected_value).matches(actual_value):
            raise AssertionError(f"Field {field} should be a dict containing {expected_value} but was {actual_value}")

        return self

    def and_has_same_list(self, field: str,
                          matcher: Optional[Callable[[T], Matcher[Any]]] = None) -> "AssertionBuilder[A]":
        return self.has_same_list(field, matcher)

    def has_same_list(self, field: str, matcher: Optional[Callable[[T], Matcher[Any]]] = None) -> "AssertionBuilder[A]":
        expected_value, actual_value = self._get_field_values(field)

        if len(expected_value) != len(actual_value):
            raise AssertionError(
                f"Field {field} should have {len(expected_value)} items but it has {len(actual_value)}")

        if matcher is None:
            for expected, actual in zip(expected_value, actual_value):
                if expected != actual:
                    raise AssertionError(
                        f"Field {field} should have the item {expected} but it has {actual}"
                    )
        else:
            for expected, actual in zip(expected_value, actual_value):
                description = Description()
                if not matcher(expected).matches(actual, description):
                    raise AssertionError(
                        f"Field {field} should have the item {expected} but it has {actual}. "
                        f"The cause was: {description}"
                    )

        return self

    def _compare_with_matcher(
        self,
        field: str,
        comparison: Callable[[T, T], bool],
        matcher: Optional[Callable[[T], Matcher[Any]]] = None
    ) -> Tuple[bool, Optional[Description]]:
        expected_value, actual_value = self._get_field_values(field)

        if matcher is None:
            return comparison(expected_value, actual_value), None
        else:
            description = Description()
            if matcher(expected_value).matches(actual_value, description):
                return True, None
            else:
                return False, description


class EntityMatcher(BaseMatcher[T], Generic[T]):
    def __init__(self, entity: T):
        super().__init__()
        self._entity: T = entity

        self._message: Optional[str] = None

    def _matches(self, actual_entity: T) -> bool:
        try:
            self._match_entity(actual_entity)

            return True
        except AssertionError as ae:
            self._message = str(ae)

            return False

    def _expect_that(self, actual_entity: T) -> "AssertionBuilder[T]":
        return AssertionBuilder(self._entity, actual_entity)

    def _match_entity(self, actual_entity: T) -> None:
        raise NotImplementedError("This method must be implemented")

    def describe_to(self, description: Description) -> None:
        description.append_text(self._message)
