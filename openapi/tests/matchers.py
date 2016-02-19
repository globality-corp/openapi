"""
Custom hamcrest matchers.
"""
from hamcrest.core.base_matcher import BaseMatcher
from json import dumps, loads


class JSONMatcher(BaseMatcher):
    """
    Match JSON content.

    """

    def __init__(self, s):
        self.json = loads(s)

    def _matches(self, item):
        return loads(item) == self.json

    def describe_to(self, description):
        description.append_text("json ").append_text(dumps(self.json))


equal_to_json = JSONMatcher
