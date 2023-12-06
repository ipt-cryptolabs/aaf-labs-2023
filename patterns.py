from abc import ABC, abstractmethod
from typing import List
from re import fullmatch

SPECIAL_CHARS = ("(", ")", "<", ",")
INITIAL_KEYWORDS = ("create", "insert", "select")
AGGREGATION_FUNCTIONS = ("count", "max", "longest")
KEYWORDS = INITIAL_KEYWORDS + AGGREGATION_FUNCTIONS + ("into", "from", "where", "group_by", "indexed")


class Pattern(ABC):

    def __init__(self, name=None):
        self.name = name

    @abstractmethod
    def is_matching(self, token: str) -> bool:
        pass

    @abstractmethod
    def match(self, token: str) -> bool:
        pass

    @abstractmethod
    def is_optional(self) -> bool:
        pass

    @abstractmethod
    def can_go_to_next_pattern(self) -> bool:
        pass

    def can_go_to_next_token(self) -> bool:
        return True


class StringPattern(Pattern):

    def __init__(self, string_value: str, name=None):
        super().__init__(name)
        self.string_value = string_value

    def __repr__(self):
        return f"Necessary '{self.string_value}'"

    def is_matching(self, token: str) -> bool:
        return token.lower() == self.string_value

    def match(self, token: str) -> bool:
        return self.is_matching(token)

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return True


class OptionalStringPattern(StringPattern):

    def __repr__(self):
        return f"Optional '{self.string_value}'"

    def is_optional(self) -> bool:
        return True


class IdentifierPattern(Pattern):

    def is_matching(self, token: str) -> bool:
        if fullmatch("[a-zA-Z][a-zA-Z0-9_]*", token):
            print("Matched!")
            return True
        print("Unmatched!")
        return False

    def match(self, token) -> bool:
        return self.is_matching(token)

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return True


class LiteralPattern(Pattern):

    def is_matching(self, token) -> bool:
        return token[0] == token[-1] == "\""

    def match(self, token) -> bool:
        return self.is_matching(token)

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return True


class LiteralOrIdentifierPattern(Pattern):

    def is_matching(self, token: str) -> bool:
        if fullmatch("[a-zA-Z][a-zA-Z0-9_]*", token):
            return True
        return token[0] == token[-1] == "\""

    def match(self, token) -> bool:
        return self.is_matching(token)

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return True


class AggregationFunctionPattern(Pattern):

    def is_matching(self, token: str) -> bool:
        return token.lower() in AGGREGATION_FUNCTIONS

    def match(self, token) -> bool:
        return self.is_matching(token)

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return True


class RepeatedPattern(Pattern):

    def __init__(self, patterns: List[Pattern], repeat_from: int, name=None):
        super().__init__(name)
        self.patterns = patterns
        self.last_index = len(patterns)-1
        self.repeat_from = repeat_from
        self.index = 0
        self.finished = False

    def __repr__(self):
        return f"RepeatedPattern with {self.patterns[self.index]}"

    def is_matching(self, token: str) -> bool:
        return self.patterns[self.index].match(token)

    def match(self, token):
        print(f"Matching {token} to pattern {self.patterns[self.index]}")
        if self.is_matching(token):
            print(f"Matched! (index={self.index})")
            self.index = self.repeat_from if self.index == self.last_index else self.index + 1
            return True
        elif self.index == self.last_index:
            print("Kind of matched...")
            self.finished = True
            return True
        elif self.patterns[self.index].is_optional():
            print("Skipping optional...")
            self.index += 1
            return self.match(token)
        else:
            print("Not matched!")
            return False

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return self.finished

    def can_go_to_next_token(self) -> bool:
        return not self.finished


class OptionalRepeatedPattern(RepeatedPattern):

    def is_optional(self) -> bool:
        return True  # TODO might be a bug here


class OptionalNonRepeatedPattern(Pattern):

    def __init__(self, patterns: List[Pattern], name=None):
        super().__init__(name)
        self.patterns = patterns
        self.last_index = len(patterns) - 1
        self.index = 0
        self.finished = False

    def is_matching(self, token: str) -> bool:
        return self.patterns[self.index].match(token)

    def match(self, token: str) -> bool:  # TODO better not forget to test this
        if self.is_matching(token):
            print("Matched!")
            self.index = self.index + 1
            self.finished = self.index == self.last_index
            return True
        elif self.patterns[self.index].is_optional():
            print("Skipping optional...")
            self.index += 1
            return self.match(token)
        else:
            print("Not matched!")
            return False

    def is_optional(self) -> bool:
        return True  # TODO might be a bug here too

    def can_go_to_next_pattern(self) -> bool:
        return self.finished


PATTERNS = {"create": [IdentifierPattern(name="table_name"),
                       StringPattern("("),
                       RepeatedPattern([IdentifierPattern(),
                                        OptionalStringPattern("indexed"),
                                        StringPattern(",")], 0, name="columns"),
                       StringPattern(")")],
            "insert": [OptionalStringPattern("into"),
                       IdentifierPattern(name="table_name"),
                       StringPattern("("),
                       RepeatedPattern([LiteralPattern(),
                                        StringPattern(",")], 0, name="values"),
                       StringPattern(")")],
            "select": [OptionalRepeatedPattern([AggregationFunctionPattern(),
                                                StringPattern("("),
                                                IdentifierPattern(),
                                                StringPattern(")"),
                                                StringPattern(",")], 0, name="functions"),
                       StringPattern("from"),
                       IdentifierPattern(name="table_name"),
                       OptionalNonRepeatedPattern([StringPattern("where"),
                                                   IdentifierPattern(),
                                                   StringPattern("<"),
                                                   LiteralOrIdentifierPattern()], name="where"),
                       OptionalRepeatedPattern([StringPattern("group_by"),
                                                IdentifierPattern(),
                                                StringPattern(",")], 1, name="group_by")]}
