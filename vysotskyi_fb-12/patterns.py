from abc import ABC, abstractmethod
from typing import List
from re import fullmatch

SPECIAL_CHARS = ("(", ")", "<", ",")
INITIAL_KEYWORDS = ("create", "insert", "select")
AGGREGATION_FUNCTIONS = ("count", "max", "longest")
KEYWORDS = INITIAL_KEYWORDS + AGGREGATION_FUNCTIONS + ("into", "from", "where", "group_by")  # , "indexed")


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

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def should_be_saved(self) -> bool:
        pass


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

    def should_be_saved(self) -> bool:
        return False


class OptionalStringPattern(StringPattern):

    def __repr__(self):
        return f"Optional '{self.string_value}'"

    def is_optional(self) -> bool:
        return True


class IdentifierPattern(Pattern):

    def is_matching(self, token: str) -> bool:
        if fullmatch("[a-zA-Z][a-zA-Z0-9_]*", token):
            return token not in KEYWORDS
        return False

    def match(self, token) -> bool:
        return self.is_matching(token)

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return True

    def __repr__(self):
        return "Identifier (keywords are not valid Identifiers)"

    def should_be_saved(self) -> bool:
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

    def __repr__(self):
        return "Literal"

    def should_be_saved(self) -> bool:
        return True


class LiteralOrIdentifierPattern(Pattern):

    def is_matching(self, token: str) -> bool:
        if fullmatch("[a-zA-Z][a-zA-Z0-9_]*", token):
            return token not in KEYWORDS
        return token[0] == token[-1] == "\""

    def match(self, token) -> bool:
        return self.is_matching(token)

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return True

    def __repr__(self):
        return "Literal or Identifier (keywords are not valid Identifiers)"

    def should_be_saved(self) -> bool:
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

    def __repr__(self):
        return "Aggregation function"

    def should_be_saved(self) -> bool:
        return True


class RepeatedPattern(Pattern):

    def __init__(self, patterns: List[Pattern], repeat_from: int, name=None):
        super().__init__(name)
        self.patterns = patterns.copy()
        self.last_index = len(patterns)-1
        self.repeat_from = repeat_from
        self.index = 0
        self.finished = False

    def __repr__(self):
        return f"{self.patterns[self.index]}"

    def is_matching(self, token: str) -> bool:
        return self.patterns[self.index].match(token)

    def match(self, token):
        if self.is_matching(token):
            self.index = self.repeat_from if self.index == self.last_index else self.index + 1
            return True
        elif self.index == self.last_index:
            self.finished = True
            return True
        elif self.patterns[self.index].is_optional():
            self.index += 1
            return self.match(token)
        else:
            return False

    def is_optional(self) -> bool:
        return False

    def can_go_to_next_pattern(self) -> bool:
        return self.finished

    def can_go_to_next_token(self) -> bool:
        return not self.finished

    def should_be_saved(self) -> bool:
        return self.patterns[self.index].should_be_saved()


class OptionalRepeatedPattern(RepeatedPattern):

    def is_optional(self) -> bool:
        return self.index in (0, len(self.patterns) - 1)


class OptionalNonRepeatedPattern(Pattern):

    def __init__(self, patterns: List[Pattern], name=None):
        super().__init__(name)
        self.patterns = patterns.copy()
        self.last_index = len(patterns)
        self.index = 0
        self.finished = False

    def is_matching(self, token: str) -> bool:
        return self.patterns[self.index].match(token)

    def match(self, token: str) -> bool:
        if self.is_matching(token):
            self.index = self.index + 1
            self.finished = self.index == self.last_index
            return True
        elif self.patterns[self.index].is_optional():
            self.index += 1
            return self.match(token)
        else:
            return False

    def is_optional(self) -> bool:
        return self.index in (0, len(self.patterns) - 1)

    def can_go_to_next_pattern(self) -> bool:
        return self.finished

    def __repr__(self):
        return f"{self.patterns[self.index]}"

    def should_be_saved(self) -> bool:
        return self.patterns[self.index].should_be_saved()


def pattern_create():
    return [IdentifierPattern(name="table_name"),
            StringPattern("("),
            RepeatedPattern([IdentifierPattern(),
                            # OptionalStringPattern("indexed"),
                            StringPattern(",")], 0, name="columns"),
            StringPattern(")")]


def pattern_insert():
    return [OptionalStringPattern("into"),
            IdentifierPattern(name="table_name"),
            StringPattern("("),
            RepeatedPattern([LiteralPattern(),
                            StringPattern(",")], 0, name="values"),
            StringPattern(")")]


def pattern_select():
    return [OptionalRepeatedPattern([AggregationFunctionPattern(),
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
                                    StringPattern(",")], 1, name="group_by")]


def get_pattern(key):
    if key == "create":
        return pattern_create()
    elif key == "insert":
        return pattern_insert()
    elif key == "select":
        return pattern_select()
