"""

The *tree item paths* states the position of a item within a tree similar to file
systems. Within a tree the **real path** is its the true location. By using the *path
parts* of a *real path* as indexes like ``tree[part_1] .. [part_n]`` the correspondent
item is returned. Other tree paths than the *real path* are freely definable and have
the purpose to construct different views.

.. warning::
   Either an *empty string* and *None* do reset a *tree node path*, if the are used
   solely in :func:`treepathmap.TreeNodePath.join`. This behavior is wanted. Also
   an *empty string* or *None* should not be used as a collection key. Use a
   placeholder instead.

"""
import re
from collections.abc import Sequence
from itertools import zip_longest
from typing import (
    Union,
    List,
    Tuple,
    Iterable,
    Iterator,
    Hashable,
    Optional,
)


__all__ = [
    "TREE_NODE_PATH_DELIMITER",
    "TreePathPart",
    "TreePathParts",
    "TreeNodePath",
    "TREE_PATH_METAATTRIBUTE_DELIMITER",
    "TreeNodePaths",
    "RootNodePath",
    "convert_metaattributes_to_pathlike",
    "convert_pathlike_metaattributes",
    "split_tree_path",
]

from pandas import Series

TreePathPart = Optional[Union[Hashable, "TreeNodePath"]]
"""
Any *tree path part* can be used within a Sequence or Mapping for indexing,
therefore it must be an *Hashable*.
"""

TreePathParts = Union[TreePathPart, List[TreePathPart]]
"""
A path is constructed by one or many *tree path parts*. The *real path*
corresponds to the nested level of the tree.
"""

TREE_NODE_PATH_DELIMITER = "->"
"""
Tree node paths are not file system paths. To clearly distinguish these from file 
system paths a different delimiter is chosen to separate the different path parts of 
a *tree node path*.
"""

REAL_PATH_INDEX = 0
"""
The first path of a *tree node* must the the **real path** of that node.
"""


_detect_multiple_delimiter = re.compile("({})+".format(TREE_NODE_PATH_DELIMITER))


def _normalize_path_of_tree(*parts_to_normalize: TreePathParts) -> str:
    # Suppressed for doctesting.
    # noinspection PyProtectedMember
    """
    Normalized a path (str) or parts of a path (List[str]) to a defined
    representation.

    Examples:
        >>> from treepathmap.treepaths import _normalize_path_of_tree
        >>> _normalize_path_of_tree("a", "path", "like", "this")
        '->a->path->like->this'
        >>> _normalize_path_of_tree("single_part")
        '->single_part'
        >>> _normalize_path_of_tree("->->items->with->", "redundant->->", "delimiters")
        '->items->with->redundant->delimiters'
        >>> _normalize_path_of_tree()
        ''
        >>> _normalize_path_of_tree("")
        ''
        >>> _normalize_path_of_tree("", "")
        ''
        >>> _normalize_path_of_tree([])
        ''
        >>> _normalize_path_of_tree("->")
        '->'
        >>> _normalize_path_of_tree("->path->->with->->->redundant->->delimiters->->")
        '->path->with->redundant->delimiters'
        >>> _normalize_path_of_tree(None)
        ''
        >>> _normalize_path_of_tree(None, "dropping", "0.level")
        '->dropping->0.level'
        >>> _normalize_path_of_tree("dropping", None, "middle", "level")
        '->dropping->middle->level'

    Args:
        *parts_to_normalize(TreePathParts):
            A single tree path part or multiple tree path parts.

    Returns:
        str:
            Normalized path '->like->this->example'.
    """

    if not parts_to_normalize:
        return ""
    convert_path = [
        str(part)
        for part in parts_to_normalize
        if isinstance(part, _valid_path_part_types) and part != ""
    ]
    joined_path = TREE_NODE_PATH_DELIMITER.join(convert_path)

    normalized_path = _detect_multiple_delimiter.sub(
        TREE_NODE_PATH_DELIMITER, joined_path
    )
    if not normalized_path:
        return ""

    delimiter_length = len(TREE_NODE_PATH_DELIMITER)
    last_chars = -delimiter_length
    first_chars = delimiter_length

    path_is_root = normalized_path == TREE_NODE_PATH_DELIMITER
    if path_is_root:
        return normalized_path

    path_ends_with_delimiter = normalized_path[last_chars:] == TREE_NODE_PATH_DELIMITER
    if path_ends_with_delimiter:
        normalized_path = normalized_path[:last_chars]

    path_starts_with_delimiter = (
        normalized_path[:first_chars] == TREE_NODE_PATH_DELIMITER
    )
    if not path_starts_with_delimiter:
        normalized_path = TREE_NODE_PATH_DELIMITER + normalized_path

    return normalized_path


def split_tree_path(tree_path: str) -> Tuple[str, str]:
    """
    Examples:
        >>> from treepathmap.treepaths import split_tree_path
        >>> split_tree_path("->a->path->with->a->attribute_name")
        ('->a->path->with->a', 'attribute_name')
        >>> split_tree_path("->a_root_path")
        ('->', 'a_root_path')
        >>> split_tree_path("")
        ('', '')
        >>> split_tree_path("->")
        ('->', '')

    Raises:
        TypeError:
            If None is given.

    Args:
        tree_path:

    Returns:
        Tuple[str, str]:
            Last item of the path.
    """
    if tree_path is None:
        raise TypeError("TypeError: expected str, not NoneType")
    if not tree_path:
        return "", ""
    parent_segment, tree_node_key = tree_path.rsplit(TREE_NODE_PATH_DELIMITER, 1)
    if not parent_segment:
        parent_segment = TREE_NODE_PATH_DELIMITER
    return parent_segment, tree_node_key


class TreeNodePath(object):
    def __init__(self, *tree_node_path_parts: TreePathParts):
        """
        A *tree node path* is at best a *List* of *Hashables*. The *TreeNodePath*
        class is a helper class to clearly distinguish this kind of path within
        the code. It also provides a convinient function to join additional parts
        to an existing *tree node path*. Except a **real path** other paths can
        be empty.

        Notes:
            Neither a validity of the path is checked nor the last part not being
            a pure int or hashable object for the targeted container.

            To preserve the ability to get the original containers items the last
            part of a path should always be the pure key or index object.

        Args:
            *tree_node_path_parts(*treePathParts):
                Parts this treepath consists of.

        Examples:
            >>> from treepathmap import TreeNodePath, TREE_NODE_PATH_DELIMITER

        By default a *tree node path* is an empty string.

            >>> TreeNodePath()
            TreeNodePath('')
            >>> print(TreeNodePath(""))
            <BLANKLINE>
            >>> print(TreeNodePath(None))
            <BLANKLINE>
            >>> print(TreeNodePath("", ""))
            <BLANKLINE>

        Behaves like a string for just `in` and `rsplit`. `split` does not
        behave list the `str.split`.

            >>> a_path = TreeNodePath("a", "path")
            >>> TREE_NODE_PATH_DELIMITER in a_path
            True
            >>> "a" in a_path
            True
            >>> a_path.rsplit("->", 1)
            ['->a', 'path']
            >>> a_path.rsplit("p")
            ['->a->', 'ath']

        A root path is a sole *TREE_NODE_PATH_DELIMITER*.

            >>> print(TreeNodePath(TREE_NODE_PATH_DELIMITER))
            ->

        As priorly demonstrated, turning a *TreeNodePath* into a string leads to a
        pure string representation of a *tree node path*.

            >>> print(TreeNodePath("a", "path"))
            ->a->path
            >>> print(TreeNodePath("->path", "parts->", "with->->to", "much", "delimiters"))
            ->path->parts->with->to->much->delimiters
            >>> print(TreeNodePath(TreeNodePath("a"), TreeNodePath("double", "entry")))
            ->a->double->entry
            >>> a_path = TreeNodePath("", "a->path")
            >>> print(a_path)
            ->a->path
            >>> a_path.container_key
            'path'

        """
        self._container_key = self._get_container_key(tree_node_path_parts)
        self._normalized_path = _normalize_path_of_tree(*tree_node_path_parts)

    def __iter__(self):
        parent_path, key = split_tree_path(self._normalized_path)
        yield parent_path
        yield self._container_key
        return None

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self._normalized_path)

    def __contains__(self, item_to_search) -> bool:
        return item_to_search in self._normalized_path

    def rsplit(self, sep: str = " ", maxsplit: int = -1):
        return self._normalized_path.rsplit(sep=sep, maxsplit=maxsplit)

    def __str__(self):
        return self._normalized_path

    @staticmethod
    def _get_container_key(tree_node_path_parts: TreePathParts) -> Optional[Hashable]:
        """
        Retrieves the container key of the last *tree node path part*.

        Examples:
            >>> from treepathmap.treepaths import TreeNodePath
            >>> TreeNodePath._get_container_key([""])
            ''
            >>> TreeNodePath._get_container_key(["", ""])
            ''
            >>> TreeNodePath._get_container_key(["", "a->path"])
            'path'
            >>> TreeNodePath._get_container_key(["", "a->path", 1])
            1

        Args:
            tree_node_path_parts:

        Returns:

        """
        assert isinstance(
            tree_node_path_parts, (list, tuple)
        ), "`tree_node_path_parts` must be a list or tuple."
        try:
            last_item_part = tree_node_path_parts[-1]
            if isinstance(last_item_part, TreeNodePath):
                container_key = last_item_part.container_key
            else:
                container_key = last_item_part
            if last_item_part == TREE_NODE_PATH_DELIMITER:
                return None
            elif last_item_part is None:
                return None
            elif (
                isinstance(last_item_part, str)
                and TREE_NODE_PATH_DELIMITER in last_item_part
            ):
                return split_tree_path(last_item_part)[1]
            else:
                return container_key
        except IndexError:
            return None

    @property
    def container_key(self) -> Hashable:
        """
        Index or key of the origin collection. Within a *real path* this key
        resembles the *Hashable* to obtain the corresponding item of a
        collection (Sequence or Mapping). It is assumed to be the last
        *tree node path part*.

        Returns:
            Hashable:
                Index or key by which an item is obtained of a collection.

        Examples:
            >>> print(TreeNodePath().container_key)
            None
            >>> TreeNodePath("").container_key
            ''
            >>> print(TreeNodePath(None).container_key)
            None
            >>> print(TreeNodePath("->").container_key)
            None
            >>> TreeNodePath("a_single_key").container_key
            'a_single_key'
            >>> TreeNodePath(TreeNodePath("a_single_key")).container_key
            'a_single_key'
            >>> TreeNodePath("a", "path").container_key
            'path'
            >>> TreeNodePath("->path", "with", "a", 1).container_key
            1
            >>> TreeNodePath(TreeNodePath("a"), TreeNodePath("double", 2)).container_key
            2

        """
        return self._container_key

    def join(self, *additional_path_parts: TreePathParts) -> "TreeNodePath":
        """
        Joins additional path parts to this *tree node path* using the
        *TREE_NODE_PATH_DELIMITER*.

        Examples:
            >>> from treepathmap import TreeNodePath, TREE_NODE_PATH_DELIMITER
            >>> root_node_path = TreeNodePath(TREE_NODE_PATH_DELIMITER)
            >>> child_of_root_path = root_node_path.join("parent")
            >>> child_of_root_path
            TreeNodePath('->parent')
            >>> child_of_root_path.join("a_child")
            TreeNodePath('->parent->a_child')
            >>> child_of_root_path.join(TreeNodePath("another_child"))
            TreeNodePath('->parent->another_child')
            >>> child_of_root_path.join(*["a", "listed", "child"])
            TreeNodePath('->parent->a->listed->child')
            >>> blank_tree_node_path = TreeNodePath("")
            >>> blank_tree_node_path
            TreeNodePath('')
            >>> blank_tree_node_path.join("")
            TreeNodePath('')
            >>> a_path = blank_tree_node_path.join("a->path")
            >>> a_path
            TreeNodePath('->a->path')

        .. warning::
            Either the *empty string* or *None* will lead to an empty
            *tree node path*. These should not be used as keys for collections
            within treepathmap. Use placeholders instead.

            >>> a_path.join("")
            TreeNodePath('')
            >>> a_path.join("", "")
            TreeNodePath('')
            >>> a_path.join(None)
            TreeNodePath('')
            >>> a_path.join(0)
            TreeNodePath('->a->path->0')

        Args:
            *additional_path_parts:

        Returns:
            TreeNodePath
        """
        for path_part in additional_path_parts:
            if path_part is not None and path_part != "":
                return TreeNodePath(self._normalized_path, *additional_path_parts)
        return TreeNodePath("")

    def split(self) -> Tuple["TreeNodePath", Hashable]:
        """
        Splits a *TreeNodePath* into its parent path and container key (like
        os.path.split).

        Notes:
            Hashables others than strings should be put into a TreeNodePath
            unconverted to preserve their attributes, since the representation
            of a *TreeNodePath* is a pure string.

        Examples:
            >>> from treepathmap import TreeNodePath
            >>> a_path_with_a_number = TreeNodePath("a_path_with_a", 1)
            >>> print(a_path_with_a_number)
            ->a_path_with_a->1
            >>> list(a_path_with_a_number)
            ['->a_path_with_a', 1]
            >>> parent_path, container_key = a_path_with_a_number.split()
            >>> parent_path
            TreeNodePath('->a_path_with_a')
            >>> container_key
            1
            >>> total_root, container_key_of_parent = parent_path.split()
            >>> total_root
            TreeNodePath('->')
            >>> container_key_of_parent
            'a_path_with_a'
            >>> total_root.split()
            (TreeNodePath('->'), '')

        Returns:
            Tuple[TreeNodePath, Hashable]
        """
        parent_segment = split_tree_path(self._normalized_path)[0]
        parent_root_path, container_key_of_parent = split_tree_path(parent_segment)
        return (
            TreeNodePath(parent_root_path, container_key_of_parent),
            self.container_key,
        )


class RootNodePath(TreeNodePath):
    """
    The *RootNodePath* is a helper class to represent the root of a tree.

    Examples:
        >>> from treepathmap import RootNodePath
        >>> RootNodePath()
        TreeNodePath('->')

    """

    def __new__(cls):
        return TreeNodePath(TREE_NODE_PATH_DELIMITER)


_valid_path_part_types = (str, int, float, TreeNodePath)


def _normalize_tree_paths(tree_paths: List[TreePathParts]) -> List[TreePathParts]:
    # Suppressed for doctesting.
    # noinspection PyProtectedMember
    """

    Examples:
        >>> tree_path_samples = [
        ...     ["a", "path", "like", "this"],
        ...     ["single_part"],
        ...     ["->->items", "with->", "unnecessary->->", "delimiters"],
        ...     [],
        ...     ["->a->->path->->->with->->->unnecessary->->delimiters->->"]
        ... ]
        ...
        >>> from treepathmap.treepaths import _normalize_tree_paths
        >>> normalized_tree_paths = _normalize_tree_paths(tree_path_samples)
        >>> for tree_path in normalized_tree_paths:
        ...     print("'{}'".format(tree_path))
        ...
        '->a->path->like->this'
        '->single_part'
        '->items->with->unnecessary->delimiters'
        ''
        '->a->path->with->unnecessary->delimiters'

    Args:
        tree_paths(List[TreePathParts]):
            blah blah

    Returns:
        List[TreePathParts]
    """
    normalized_tree_paths = []
    for tree_path_parts in tree_paths:
        normalized_tree_path = _normalize_path_of_tree(*tree_path_parts)
        normalized_tree_paths.append(normalized_tree_path)
    return normalized_tree_paths


TREE_PATH_METAATTRIBUTE_DELIMITER = "/"
"""
Seperates the meta attribute parts.
"""


def _sort_metaattributes(meta_attributes: dict) -> List[Tuple[str, str]]:
    """
    Examples:
        >>> from treepathmap.treepaths import _sort_metaattributes
        >>> _sort_metaattributes({"Zebra": "monochrome", "Ape": "black", "Lion": "orange"})
        [('Ape', 'black'), ('Lion', 'orange'), ('Zebra', 'monochrome')]

    Args:
        meta_attributes:

    Returns:

    """
    sorted_meta_attribute_pairs = sorted(
        meta_attributes.items(),
        key=lambda key_value_pair: (key_value_pair[0], key_value_pair[1]),
    )
    return sorted_meta_attribute_pairs


NOT_A_NUMBER_OR_NONE_REPRESENTATIONS = ["nan"]


def convert_metaattributes_to_pathlike(meta_attributes: Union[dict, Series]) -> str:
    """
    Examples:
        >>> from treepathmap.treepaths import convert_metaattributes_to_pathlike
        >>> convert_metaattributes_to_pathlike(
        ...     {"key2": 2, "key1": 1}
        ... )
        ...
        '//key1/1//key2/2//'
        >>> from pandas import Series
        >>> import numpy as np
        >>> sample_series = Series(["a", "b", np.nan], index=["key1", "key2", "key3"])
        >>> convert_metaattributes_to_pathlike(sample_series)
        '//key1/a//key2/b//key3///'

    Args:
        meta_attributes:

    Returns:

    """
    converted_attribute_pairs = []
    doubled_delimiter = TREE_PATH_METAATTRIBUTE_DELIMITER * 2
    for attribute_name, attribute_value in _sort_metaattributes(meta_attributes):
        value_representation = str(attribute_value)
        if value_representation not in NOT_A_NUMBER_OR_NONE_REPRESENTATIONS:
            formatted_pair = "{}{}{}".format(
                attribute_name, TREE_PATH_METAATTRIBUTE_DELIMITER, attribute_value
            )
        else:
            formatted_pair = "{}{}".format(
                attribute_name, TREE_PATH_METAATTRIBUTE_DELIMITER
            )
        converted_attribute_pairs.append(formatted_pair)
    combined_metaattributes = doubled_delimiter.join(converted_attribute_pairs)
    meta_attributes_alike_treepath = doubled_delimiter + combined_metaattributes
    meta_attributes_alike_treepath += doubled_delimiter
    return meta_attributes_alike_treepath


def _group_metaattributes(metaattribute_parts: Iterable) -> Iterator:
    # Suppressed for doctesting.
    # noinspection PyProtectedMember
    """
    Taken from https://docs.python.org/3.8/library/itertools.html#recipes at
    grouper.
    Collects potential_tree into fixed-length chunks or blocks.

    Examples:
        >>> from treepathmap.treepaths import _group_metaattributes
        >>> list(
        ...     _group_metaattributes(
        ...         ['a', 'b', 'c', 'd']
        ...     )
        ... )
        ...
        [('a', 'b'), ('c', 'd')]

    Args:
        metaattribute_parts(Iterable):
            An iterable, which will be grouped into groups of *group_size*.
    Returns:
        Iterator
    """
    # Group size of meta attributes is 2
    key_value_pairs = [iter(metaattribute_parts)] * 2
    # uneven occurrences are filled with empty strings
    return zip_longest(*key_value_pairs, fillvalue="")


def convert_pathlike_metaattributes(pathlike_metaattribute: str,) -> dict:
    """
    Converts a pathlike *meta attribute* from this path map to a
    sequence of attribute_name and value tuples.

    Examples:
        >>> from treepathmap.treepaths import convert_pathlike_metaattributes
        >>> convert_pathlike_metaattributes(
        ...    "/key1/value1/key2/value2/"
        ... )
        ...
        {'key1': 'value1', 'key2': 'value2'}

    Args:
        pathlike_metaattribute(str):
            A string like a tree path with an addition of a closing
            delimiter.

    Returns:
        dict
    """
    all_without_first_and_last = slice(1, -1, 1)
    splitted_parts = pathlike_metaattribute.split(TREE_PATH_METAATTRIBUTE_DELIMITER)
    metaattribute_parts = splitted_parts[all_without_first_and_last]
    metaattributes = dict(_group_metaattributes(metaattribute_parts))
    return metaattributes


class TreeNodePaths(Sequence):
    def __init__(
        self,
        tree_paths: List[Union[TreeNodePath, List[Hashable]]] = "",
        meta_attributes: dict = None,
    ):
        """
        Defines a path within a nested potential_tree structure of `sequence` and
        `mapping`. Within a *tree path map* a tree node can have multiple paths.
        Also meta attributes can be associated with these paths for a more
        refined selection of tree nodes.

        Notes:
            The first path must be the **real path** of the tree node.

        Args:
            tree_paths (List[TreeNodePath]):
                The real path within the potential_tree structure.

            meta_attributes (dict):
                Additional attributes of this tree node, which should
                refer to this path.

        Examples:
            >>> from treepathmap import TreeNodePaths, RootNodePath
            >>> print(TreeNodePaths([RootNodePath()]))
            TreePath:
                path-0: ->
                metadata: {}
            >>> parent_tree_single_path = TreeNodePaths(
            ...     [TreeNodePath("parent")], {"meta_1": "1"}
            ... )
            ...
            >>> parent_tree_single_path.real_key
            'parent'
            >>> print(parent_tree_single_path)
            TreePath:
                path-0: ->parent
                metadata: {'meta_1': '1'}
            >>> child_tree_single_path = parent_tree_single_path.join(
            ...     [["child"]],
            ...     {"meta_2": "2"}
            ... )
            ...
            >>> child_tree_single_path.real_key
            'child'
            >>> print(child_tree_single_path)
            TreePath:
                path-0: ->parent->child
                metadata: {'meta_1': '1', 'meta_2': '2'}
            >>> child_with_number = parent_tree_single_path.join([[1]])
            >>> child_with_number.real_key
            1
            >>> print(child_tree_single_path)
            TreePath:
                path-0: ->parent->child
                metadata: {'meta_1': '1', 'meta_2': '2'}
            >>> parent_tree_multi_path = TreeNodePaths(
            ...     [["parent"], ["stepparent"]],
            ...     {"meta_1": "1"}
            ... )
            ...
            >>> print(parent_tree_multi_path)
            TreePath:
                path-0: ->parent
                path-1: ->stepparent
                metadata: {'meta_1': '1'}
            >>> child_tree_multi_path = parent_tree_multi_path.join(
            ...     [["1st child"], ["2nd child"]],
            ...     {"meta_2": "2"}
            ... )
            ...
            >>> print(child_tree_multi_path)
            TreePath:
                path-0: ->parent->1st child
                path-1: ->stepparent->2nd child
                metadata: {'meta_1': '1', 'meta_2': '2'}

        .. warning:

            *Tree node path parts* should always be defined as parts or at least
            a seperated **container key** from the **parent path**. A 'a->path' as
            the last element of a path part will lead to a wrong depiction.

            >>> root_node_paths = TreeNodePaths([RootNodePath()])
            >>> a_first_path = root_node_paths.join([["a->path"], ["x"]])
            >>> print(a_first_path)
            TreePath:
                path-0: ->a->path
                path-1: ->x
                metadata: {}
            >>> print(a_first_path.join([["part"], [""]]))
            TreePath:
                path-0: ->a->path->part
                path-1: NO PATH
                metadata: {}

        """
        assert meta_attributes is None or isinstance(
            meta_attributes, dict
        ), "The meta attributes needs to be a dict, got '{}' instead.".format(
            type(meta_attributes).__name__
        )
        self.tree_paths = []
        for path in tree_paths:
            new_tree_path = TreeNodePath(*path)
            self.tree_paths.append(new_tree_path)
        if meta_attributes is not None:
            self._meta_attributes = meta_attributes
        else:
            self._meta_attributes = {}

    def __len__(self):
        return len(self.tree_paths)

    def __getitem__(self, index) -> Union[str, List[str]]:
        return self.tree_paths[index]

    @property
    def meta_attributes(self) -> dict:
        """
        Meta attributes this the tree node is associated with.

        Returns:
            dict
        """
        return self._meta_attributes

    @property
    def real_key(self) -> Hashable:
        """
        The **real key** is the *Hashable* to obtain the corresponding item
        from a collection (Sequence or Mapping).

        Returns:
            Hashable
        """
        return self.tree_paths[0].container_key

    @property
    def path_count(self) -> int:
        """
        Count of (multiple) paths defined for this item.

        Returns:
            int
        """
        return len(self.tree_paths)

    def join(
        self,
        tree_sub_paths: List[TreePathParts] = "",
        meta_attributes: dict = None,
        reset: Optional[List[int]] = None,
    ) -> "TreeNodePaths":
        """
        Joins the tree node sub paths to this item returning a new child.
        Count of sub paths must be equal to the count of this item.

        Args:
            tree_sub_paths (List[TreePathParts]):
                Sub paths for this tree node path.

            meta_attributes (dict):
                Associations of this path part.

        Returns:
            TreeNodePaths:
                Path within augmented tree.
        """
        count_of_given_paths_to_join = len(tree_sub_paths)
        self._extend_tree_path_count(count_of_given_paths_to_join)

        new_children_paths = []
        maximum_index_of_given_tree_paths_to_join = count_of_given_paths_to_join - 1
        for index, current_parent_path in enumerate(self.tree_paths):
            if index > maximum_index_of_given_tree_paths_to_join:
                break
            sub_path_parts = tree_sub_paths[index]
            new_childs_path = current_parent_path.join(*sub_path_parts)
            new_children_paths.append(new_childs_path)

        meta_attributes_of_child = self._meta_attributes.copy()
        if isinstance(meta_attributes, dict):
            meta_attributes_of_child.update(meta_attributes)

        new_sub_path = TreeNodePaths(
            tree_paths=new_children_paths, meta_attributes=meta_attributes_of_child
        )
        return new_sub_path

    def __str__(self):
        strings_of_paths = []
        for index, path in enumerate(self.tree_paths):
            converted_path = str(path)
            if converted_path == "":
                strings_of_paths.append("path-{}: NO PATH".format(index))
            else:
                strings_of_paths.append("path-{}: {}".format(index, converted_path))
        output_of_paths = "\n    ".join(strings_of_paths)
        output = "TreePath:\n    {}\n    metadata: {}".format(
            output_of_paths, self._meta_attributes
        )
        return output

    def add_meta_attributes(self, additional_meta_attributes: dict):
        """
        Adds additional meta attributes to this instance.

        Examples:
            >>> from treepathmap import TreeNodePaths, RootNodePath
            >>> sample_paths = TreeNodePaths([RootNodePath()], {"1st": "item"})
            >>> print(sample_paths)
            TreePath:
                path-0: ->
                metadata: {'1st': 'item'}
            >>> sample_paths.add_meta_attributes({"1st": "overridden", "new": "one"})
            >>> print(sample_paths)
            TreePath:
                path-0: ->
                metadata: {'1st': 'overridden', 'new': 'one'}

        Note:
            Be alarmed as existing keys are overridden. This behavior is
            intended as it resembles the idea of inheritance from root to
            leaf, while giving the leaf the chance for a local definition.

        Args:
            additional_meta_attributes(dict):
                These additional meta attributes update the existing
                definition.

        """
        self._meta_attributes.update(additional_meta_attributes)

    def _extend_tree_path_count(self, requested_count: int):
        additional_required_count_of_paths = requested_count - self.path_count
        self._add_required_blank_tree_paths(additional_required_count_of_paths)

    def _add_required_blank_tree_paths(self, additional_required_count_of_paths: int):
        paths_need_to_be_added = additional_required_count_of_paths > 0
        if paths_need_to_be_added:
            empty_tree_node_path = TreeNodePath(None)
            additional_paths = [
                empty_tree_node_path for i in range(additional_required_count_of_paths)
            ]
            self.tree_paths.extend(additional_paths)

    def set_tree_path(self, index_of_paths: int, *tree_node_path_parts: TreePathParts):
        """
        Adds additional meta attributes to this instance.

        Examples:
            >>> from treepathmap import TreeNodePaths, TreeNodePath
            >>> sample_paths = TreeNodePaths([TreeNodePath("1st", 1)])
            >>> print(sample_paths)
            TreePath:
                path-0: ->1st->1
                metadata: {}

        'Holes' are filled with blank paths.

            >>> sample_paths.set_tree_path(2, "3rd", "path", "is", "hot.")
            >>> print(sample_paths)
            TreePath:
                path-0: ->1st->1
                path-1: NO PATH
                path-2: ->3rd->path->is->hot.
                metadata: {}
            >>> sample_paths.set_tree_path(1, "2nd", "one")
            >>> print(sample_paths)
            TreePath:
                path-0: ->1st->1
                path-1: ->2nd->one
                path-2: ->3rd->path->is->hot.
                metadata: {}

        Raises:
            ValueError:
                The **real path** cannot be changed after the first definition.
                Therefore the index *REAL_PATH_INDEX* is prohibited.

        Args:
            additional_meta_attributes(dict):
                These additional meta attributes update the existing
                definition.

        """
        position_of_real_paths = 0
        prohibited_change_is_requested = index_of_paths == position_of_real_paths
        if prohibited_change_is_requested:
            raise ValueError("Changing the real path is prohibited.")
        new_tree_path = TreeNodePath(*tree_node_path_parts)

        required_count_by_index = index_of_paths + 1
        self._extend_tree_path_count(required_count_by_index)

        self.tree_paths[index_of_paths] = new_tree_path