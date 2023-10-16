from typing import Iterable, List, Optional

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description

from auto_phylo.pipeliner.io.ParseError import ParseError


class ParseErrorLinesMatcher(BaseMatcher[ParseError]):
    def __init__(self, lines: Optional[Iterable[int]] = None):
        super().__init__()
        self._expected_lines: Optional[List[int]] = None if lines is None else sorted(lines)

    def _matches(self, actual_entity: ParseError) -> bool:
        actual_lines = None if actual_entity.line_errors is None else sorted(actual_entity.line_errors.keys())

        return self._expected_lines == actual_lines

    def describe_to(self, description: Description) -> None:
        description.append_text(f"errors in lines {self._expected_lines}")


def does_not_have_any_line_error() -> "ParseErrorLinesMatcher":
    return ParseErrorLinesMatcher()


def has_errors_in_lines(lines: Iterable[int]) -> "ParseErrorLinesMatcher":
    return ParseErrorLinesMatcher(lines)
