from typing import Iterable, List, Optional

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description

from auto_phylo.gui.io.ParseError import ParseError


class ParseErrorGeneralErrorsMatcher(BaseMatcher[ParseError]):
    def __init__(self, general_errors: Optional[Iterable[str]] = None):
        super().__init__()
        self._expected_general_errors: List[str] = None if general_errors is None else sorted(general_errors)

    def _matches(self, actual_entity: ParseError) -> bool:
        actual_general_errors = None if actual_entity.general_errors is None else sorted(actual_entity.general_errors)
        
        return self._expected_general_errors == actual_general_errors

    def describe_to(self, description: Description) -> None:
        description.append_text(f"errors in lines {self._expected_general_errors}")


def does_not_have_any_general_error() -> "ParseErrorGeneralErrorsMatcher":
    return ParseErrorGeneralErrorsMatcher()


def has_general_errors(general_error: Iterable[str]) -> "ParseErrorGeneralErrorsMatcher":
    return ParseErrorGeneralErrorsMatcher(general_error)
