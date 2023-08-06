import re
from typing import Match, List, Union, Iterable
from abc import ABC
from treepathmap.treepaths import (
    TREE_NODE_PATH_DELIMITER,
    TREE_PATH_METAATTRIBUTE_DELIMITER,
)


__all__ = [
    "UnixFilePatternParts",
    "UFPP",
    "RegularExpressionParts",
    "REP",
    "create_selection_pattern",
    "convert_to_where_searchable_parts",
    "turn_iterables_to_unixfilepatterns"
]


UFP2RE_WILDCARD_STAR = "*.?"
IGNORE_TREE_PATH_PARTS_IN_BETWEEN = "(.*{}{{}})".format(TREE_NODE_PATH_DELIMITER)
LAST_VALID_TREE_PATH_LEVEL = "(.*{}{{}}$)".format(TREE_NODE_PATH_DELIMITER)
END_POINT_SEARCH_PART_MUST_NOT_CONTINUE_AFTER_A_DELIMITER = "(?!.*{}).*".format(
    TREE_NODE_PATH_DELIMITER
)
META_ATTRIBUTE_PAIR_REGEX_WRAPPER = ".*{0}{{}}{0}.*".format(
    TREE_PATH_METAATTRIBUTE_DELIMITER
)


class QuestionmarkUnixFilePattern2RegexReplacer(object):
    """
    Replaces a question mark used in unix file patterns to a fitting regular
    expression.

    Examples:
        >>> from treepathmap.selections import QuestionmarkUnixFilePattern2RegexReplacer
        >>> QuestionmarkUnixFilePattern2RegexReplacer("?")
        '.'
        >>> QuestionmarkUnixFilePattern2RegexReplacer("???")
        '.{3}'
        >>> QuestionmarkUnixFilePattern2RegexReplacer("??o?")
        '.{2}o.'
        >>> QuestionmarkUnixFilePattern2RegexReplacer("??o??")
        '.{2}o.{2}'

    """

    target_char_is = "?"
    detector = re.compile("[?]+")

    def __new__(cls, expression_to_convert: str) -> str:
        if cls.target_char_is not in expression_to_convert:
            return expression_to_convert
        converted_expression = cls.detector.sub(
            cls.make_replacement, expression_to_convert
        )
        return converted_expression

    @staticmethod
    def make_replacement(questionmark_matchobject: Match) -> str:
        """
        Replaces a Unix file pattern '?' or a sequence of '?' with an
        equivalent regular expression pattern of '.'.

        Args:
            questionmark_matchobject(Match):
                Matching(s) of '?'

        Returns:
            str:
                Replaced Unix file pattern '?' with equivalent regular
                expression.
        """
        length = questionmark_matchobject.end(0) - questionmark_matchobject.start(0)
        if length == 1:
            return "."
        else:
            replacement = ".{{{}}}".format(length)
            return replacement


class StaticUnixFilePattern2RegexReplacer(object):
    """
        Defines a replacement of unix file patterns to regular expressions.

        Examples:
            >>> from treepathmap.selections import StaticUnixFilePattern2RegexReplacer
            >>> StarWildCard_Replacer = StaticUnixFilePattern2RegexReplacer(
            ...    regex_detection_pattern=r"\*",
            ...    replacement="*.?",
            ...    str_to_detect_in_expression="*"
            ... )
            ...
            >>> StarWildCard_Replacer("Any*in*between")
            'Any*.?in*.?between'

        """

    def __init__(
        self,
        regex_detection_pattern: str,
        replacement: str,
        str_to_detect_in_expression: str = None,
    ):
        self.detector = re.compile(regex_detection_pattern)
        self.replacement = replacement
        self.target_char_is = str_to_detect_in_expression

    def __call__(self, expression_to_convert: str):
        nothing_to_replace = (
            self.target_char_is is not None
            and self.target_char_is not in expression_to_convert
        )
        if nothing_to_replace:
            return expression_to_convert
        converted_expression = self.detector.sub(
            self.replacement, expression_to_convert
        )
        return converted_expression


StarWildCard_Replacer = StaticUnixFilePattern2RegexReplacer(
    regex_detection_pattern=r"\*", replacement="*.?", str_to_detect_in_expression="*"
)


UNIXFILEPATTERN_TO_REGEX_REPLACEMENTS = [
    QuestionmarkUnixFilePattern2RegexReplacer,
    StarWildCard_Replacer,
]


def convert_unixfilepattern_to_regex(expression_to_convert: str) -> str:
    """
    Converts an unix file pattern into a regular expression.

    Examples:
        >>> from treepathmap.selections import convert_unixfilepattern_to_regex
        >>> convert_unixfilepattern_to_regex("a n?m? with ????")
        'a n.m. with .{4}'
        >>> convert_unixfilepattern_to_regex("take a n*r [23456]")
        'take a n*.?r [23456]'

    Args:
        expression_to_convert(str):
            Unix file pattern to convert into a regular expression.

    Returns:
        str
            Regular expression pattern.
    """
    converted_expression = expression_to_convert
    for converter in UNIXFILEPATTERN_TO_REGEX_REPLACEMENTS:
        converted_expression = converter(converted_expression)
    return converted_expression


class TreePathSearchPatternParts(ABC):
    """
    Defines a set of tree path parts, which are combined to an `or` condition
    within this group within a query.
    """

    def to_re_pattern(self) -> str:
        """
        Converts all parts of this entity to regular expressions.

        Returns:
            str:
                Regular expressions of all parts.
        """
        pass


class UnixFilePatternParts(TreePathSearchPatternParts):
    """
    Defines parts unix file patterns for conversion into regular expression
    parts.

    Examples:
        >>> from treepathmap import UnixFilePatternParts
        >>> ufpp = UnixFilePatternParts("part1", "part*", "part??")
        >>> ufpp.to_re_pattern()
        '(part1|part*.?|part.{2})'
        >>> print(ufpp)
        UFPP(part1->part*->part??)
        >>> UnixFilePatternParts.convert_to_re_patterns("part1", "part*", "part??")
        ['part1', 'part*.?', 'part.{2}']

    """

    def __init__(self, *path_parts):
        self.path_parts = [str(part) for part in path_parts]

    def to_re_pattern(self) -> str:
        """
        Converts these UnixFilePatternParts into a regular expression, which
        will work as an or condition, if multiple parts are defined.

        Returns:
            str:
                regular expression
        """
        re_path_parts = UnixFilePatternParts.convert_to_re_patterns(*self.path_parts)
        or_conditioned = "|".join(re_path_parts)
        or_conditioned = "(" + or_conditioned + ")"
        return or_conditioned

    @staticmethod
    def convert_to_re_patterns(*unix_file_pattern) -> List[str]:
        """
        Converts strings being considered as a unix file patterns to regular
        expression patterns.

        Args:
            *unix_file_pattern:
                Search pattern(s) to be converted into regular expressions.

        Returns:
            List(str):
                Regular expression patterns.
        """
        regex_patterns = []
        for unit_file_pattern in unix_file_pattern:
            regex_pattern = convert_unixfilepattern_to_regex(unit_file_pattern)
            regex_patterns.append(regex_pattern)
        return regex_patterns

    def __repr__(self):
        joined_parts = "->".join(self.path_parts)
        return "{}({})".format(self.__class__.__name__, joined_parts)

    def __str__(self):
        joined_parts = "->".join(self.path_parts)
        return "UFPP({})".format(joined_parts)


UFPP = UnixFilePatternParts


class RegularExpressionParts(TreePathSearchPatternParts):
    def __init__(self, *path_parts):
        self.path_parts = path_parts

    def to_re_pattern(self) -> str:
        """
        Combines these RegularExpressionParts into a single regular
        expression, which will work as an or condition,
        if multiple parts are defined.

        Returns:
            str:
                regular expression
        """
        or_conditioned = "|".join(self.path_parts)
        or_conditioned = "(" + or_conditioned + ")"
        return or_conditioned

    def __str__(self):
        joined_parts = " -> ".join(self.path_parts)
        return "({})".format(joined_parts)


REP = RegularExpressionParts


def _convert_search_part_to_regex_pattern(
    search_part: Union[str, UnixFilePatternParts, RegularExpressionParts]
) -> str:
    """
    Converts a single search part to a regular expression search part. Strings
    will be considered as a unix file pattern. Regular expression parts need
    to be explicitly defined as 'RegularExpressionParts'.

    Args:
        search_part(Union[str, UnixFilePatternParts, RegularExpressionParts]):
            Tree path search part, which will be converted to a regular
            expression.

    Returns:
        str:
            regular expression
    """
    if isinstance(search_part, str):
        regex_pattern = convert_unixfilepattern_to_regex(search_part)
    else:
        regex_pattern = search_part.to_re_pattern()
    return regex_pattern


def _convert_all_search_parts_to_regex_patterns(
    *search_parts: Union[str, UnixFilePatternParts, RegularExpressionParts]
) -> List[str]:
    """
    Converts multiple search parts to regular expression search parts. Strings
    will be considered as a unix file pattern. Regular expression parts need
    to be explicitly defined as 'RegularExpressionParts'.

    Args:
        *search_part:
            Search parts of *str*, *UnixFilePatternParts* or
            *RegularExpressionParts*, which will be converted to a regular
            expressions.

    Returns:
        List[str]:
            regular expressions
    """
    regular_expression_search_parts = []

    for search_part in search_parts:
        search_part_pattern = _convert_search_part_to_regex_pattern(search_part)
        regular_expression_search_parts.append(search_part_pattern)

    return regular_expression_search_parts


def _make_search_parts_to_ignore_unknown_ones(
    regex_search_parts: List[str],
) -> List[str]:
    """
    Puts regular expression parts into a group

    Args:
        regex_search_parts(str):
            Regular expression search parts, which need to be enabled to
            ignore unknown tree path parts in between them.

    Returns:
        List[str]:
            Regular expression search parts (with ignorance), which will
            ignore unknown tree path parts in between them.
    """
    template = IGNORE_TREE_PATH_PARTS_IN_BETWEEN
    regex_search_parts_with_ignorance = []
    for regular_expression_search_part in regex_search_parts:
        pattern_with_ignorance = template.format(regular_expression_search_part)
        regex_search_parts_with_ignorance.append(pattern_with_ignorance)
    return regex_search_parts_with_ignorance


def _consider_star_wildcard(end_point_regex_search_part: str) -> str:
    """
    Takes account of a star wildcard within a search part, which should
    behave as the end point of the selection.

    Args:
        end_point_regex_search_part:
            Regular expression search part being an end point of search.

    Returns:
        str:
            Regular expression search part, which cannot continue with a
            tree path delimiter.
    """
    star_wildcard_endpoint = end_point_regex_search_part.replace(
        UFP2RE_WILDCARD_STAR, END_POINT_SEARCH_PART_MUST_NOT_CONTINUE_AFTER_A_DELIMITER
    )
    return star_wildcard_endpoint


def create_selection_pattern(*search_parts):
    """
    Creates a search pattern, which will select tree paths up to the last
    defined `search part`.

    Examples:
        >>> from treepathmap.selections import create_selection_pattern
        >>> create_selection_pattern("a_single_one")
        '(.*->a_single_one$)'
        >>> create_selection_pattern("first", "second")
        '(.*->first)(.*->second$)'
        >>> from treepathmap import UFPP
        >>> create_selection_pattern("f?rst", UFPP("s*cond", "th?rd"), "f??rth")
        '(.*->f.rst)(.*->(s*.?cond|th.rd))(.*->f.{2}rth$)'
        >>> from treepathmap import REP
        >>> create_selection_pattern("f?rst", REP("s*cond", "th?rd"), "f??rth")
        '(.*->f.rst)(.*->(s*cond|th?rd))(.*->f.{2}rth$)'

    Args:
        *search_parts:
            Search parts being str,

    Returns:

    """
    regex_search_parts = _convert_all_search_parts_to_regex_patterns(*search_parts)
    final_search_parts = _make_search_parts_to_ignore_unknown_ones(regex_search_parts)

    last_regex_search_part = regex_search_parts[-1]
    end_point_search_part = LAST_VALID_TREE_PATH_LEVEL.format(last_regex_search_part)
    end_point_search_part = _consider_star_wildcard(end_point_search_part)
    final_search_parts[-1] = end_point_search_part

    # build search pattern
    search_pattern = "".join(final_search_parts)

    return search_pattern


QueryPart = Union[str, UnixFilePatternParts, RegularExpressionParts]
QueryParts = Union[QueryPart, List[QueryPart]]


def convert_to_where_searchable_parts(*search_parts: QueryParts) -> List[str]:
    """
    Creates a search pattern, which will select tree paths up to the last
    defined `search part`.

    Examples:
        >>> from treepathmap.selections import convert_to_where_searchable_parts
        >>> convert_to_where_searchable_parts("a_single_one")
        ['.*/a_single_one/.*']
        >>> convert_to_where_searchable_parts("first", "second")
        ['.*/first/.*', '.*/second/.*']
        >>> from treepathmap import UFPP
        >>> convert_to_where_searchable_parts("f?rst", UFPP("s*cond", "th?rd"), "f??rth")
        ['.*/f.rst/.*', '.*/(s*.?cond|th.rd)/.*', '.*/f.{2}rth/.*']
        >>> from treepathmap import REP
        >>> convert_to_where_searchable_parts("f?rst", REP("s*cond", "th?rd"), "f??rth")
        ['.*/f.rst/.*', '.*/(s*cond|th?rd)/.*', '.*/f.{2}rth/.*']

    Args:
        *search_parts:
            Search parts being str,

    Returns:
        List[str]:
            Search pattern for looking at _meta_attributes.
    """
    regex_search_parts = _convert_all_search_parts_to_regex_patterns(*search_parts)
    where_searchable_parts = []
    for search_part in regex_search_parts:
        where_searchable = META_ATTRIBUTE_PAIR_REGEX_WRAPPER.format(search_part)
        where_searchable_parts.append(where_searchable)
    return where_searchable_parts


class SelectionRegexPathQuery(object):
    """
    Examples:
        >>> from treepathmap import UFPP, REP
        >>> from treepathmap.selections import SelectionRegexPathQuery
        >>> SelectionRegexPathQuery("part1", "part2")
        SelectionRegexPathQuery((.*->part1)(.*->part2$))
        >>> SelectionRegexPathQuery("part1", UFPP("part2", "part3"), "part4")
        SelectionRegexPathQuery((.*->part1)(.*->(part2|part3))(.*->part4$))
        >>> SelectionRegexPathQuery("part1", REP("?i:ignore_case"), "part4")
        SelectionRegexPathQuery((.*->part1)(.*->(?i:ignore_case))(.*->part4$))

    """

    def __init__(self, *path_parts: QueryParts):
        self.path_parts = path_parts
        self.search_pattern = create_selection_pattern(*path_parts)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.search_pattern)


def turn_iterables_to_unixfilepatterns(
    search_parts: Iterable[Union[int, str]],
) -> List[Union[str, UnixFilePatternParts, RegularExpressionParts]]:
    """
    Examples:
        >>> from treepathmap.selections import turn_iterables_to_unixfilepatterns
        >>> turn_iterables_to_unixfilepatterns([])
        []
        >>> turn_iterables_to_unixfilepatterns([1])
        ['1']
        >>> turn_iterables_to_unixfilepatterns(["1"])
        ['1']
        >>> turn_iterables_to_unixfilepatterns([1, 2])
        ['1', '2']
        >>> turn_iterables_to_unixfilepatterns([[1, 2]])
        [UnixFilePatternParts(1->2)]

    Args:
        search_parts:

    Returns:

    """
    appropriate_search_parts = []
    for search_part in search_parts:
        if isinstance(search_part, (list, tuple)):
            clean_part = UnixFilePatternParts(*search_part)
        else:
            clean_part = str(search_part)
        appropriate_search_parts.append(clean_part)
    return appropriate_search_parts