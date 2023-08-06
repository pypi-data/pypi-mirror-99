import warnings
from abc import abstractmethod, ABC
from typing import (
    Union,
    Iterable,
    Any,
    List,
    Generator,
    Optional,
    Dict,
    Tuple,
    Callable,
    Mapping,
    Hashable,
    overload,
    Sequence,
)

import pandas
from pandas import DataFrame, Series, Index
from treepathmap.selectables import (
    SelectablePaths,
    REAL_PATH_INDEX,
    IrregularTags,
    WhereSelectable,
    RelatedGroupTags,
)

from treepathmap import (
    TreeNodeItem,
    ATreeNodeItem,
    TreeNodeItems,
)
from treepathmap.selections import create_selection_pattern
from treepathmap.treepaths import (
    TreeNodePaths,
    TreeNodePath,
    TREE_PATH_METAATTRIBUTE_DELIMITER,
    TREE_NODE_PATH_DELIMITER,
    RootNodePath,
)
import treenodedefinition
from treenodedefinition import DetectATreeLeaf


__all__ = [
    "PathMap",
    "wh_is",
    "map_tree",
    "map_tree_items",
    "iter_tree_items",
    "PathMapTable",
]


class MimicsSequence(ABC):
    @abstractmethod
    def __len__(self):
        pass

    def __getitem__(
        self, key: Union[int, str, slice]
    ) -> Union[ATreeNodeItem, Iterable[ATreeNodeItem]]:
        """
        Retrieves an item at the given *real_path* or the x-th integer
        *position* within its PathMap. If a *slice* is given all corresponding
        item are returned.

        Args:
            key(Union[int, str, slice]):
                Either a *real_path*, an integer *position* or a slice.

        Returns:
            Union[TreeNodeItem, Iterable[PathMapItem]]:
                An item for a *real_path* or integer *position* or a list
                of items for a *slice*.
        """
        if isinstance(key, int):
            return self.by_position(key)
        if isinstance(key, str):
            return self.by_real_path(key)
        if isinstance(key, slice):
            return self.by_slice(key)
        raise IndexError(
            "Neither a real_path, a integer position or a slice were given."
        )

    @abstractmethod
    def by_real_path(self, real_path: str) -> Any:
        """
        Retrieves an item at the given *real_path*.

        Args:
            real_path(str):
                Real path of the tree item, for which a PathMapItem is
                returned.

        Returns:
            Any
        """
        pass

    @abstractmethod
    def by_position(self, position: int) -> Any:
        """
        Retrieves an item for the integer *position* within this
        path map.

        Args:
            position(int):
                Integer position within the path map.

        Returns:
            Any
        """
        pass

    @abstractmethod
    def by_slice(self, positions: slice) -> List[Any]:
        """
        Retrieves a set of items at the positions, which are defined
        by a slice.

        Args:
            positions(slice):
                Slice for which items should be returned.

        Returns:
            List[Any]
        """
        pass


class TreeNodeItemSequenceMimic(MimicsSequence):
    def __init__(self, parent_pathmap: "PathMap"):
        self._parent = parent_pathmap

    def __len__(self):
        return len(self._parent)

    def __iter__(self) -> Generator[TreeNodeItem, None, None]:
        for real_path in self._parent.real_paths:
            path_map_item = self._parent.get_path_map_item_by_real_path(real_path)
            yield path_map_item

    def __getitem__(
        self, key: Union[int, str, slice]
    ) -> Union[ATreeNodeItem, Iterable[ATreeNodeItem]]:
        """
        Retrieves a PathMapItem at the given *real_path* or the x-th integer
        *position* within its PathMap. If a *slice* is given all corresponding
        PathMapItem are returned.

        Args:
            key(Union[int, str, slice]):
                Either a *real_path*, an integer *position* or a slice.

        Returns:
            Union[TreeNodeItem, Iterable[PathMapItem]]:
                A PathMapItem for a *real_path* or integer *position* or a list
                of tree items for a *slice*.
        """
        return super().__getitem__(key)

    def by_real_path(self, real_path: str) -> TreeNodeItem:
        """
        Retrieves a *PathMapItem* at the given *real_path*.

        Args:
            real_path(str):
                Real path of the tree item, for which a PathMapItem is
                returned.

        Returns:
            PathMapItem
        """
        requested_path_map_item = self._parent.get_path_map_item_by_real_path(real_path)
        return requested_path_map_item

    def by_position(self, position: int) -> TreeNodeItem:
        """
        Retrieves a *PathMapItem* for the integer *position* within this
        path map.

        Args:
            position(int):
                Integer position within the path map.

        Returns:
            PathMapItem
        """
        real_path = self._parent.real_paths[position]
        return self.by_real_path(real_path)

    def by_slice(self, positions: slice) -> List[TreeNodeItem]:
        """
        Retrieves a set of *PathMapItem* at the positions, which are defined
        by a slice.

        Args:
            positions(slice):
                Slice for which *PathMapItems* should be returned.

        Returns:
            List[PathMapItems]
        """
        requested_pathmapitems = []
        requested_real_paths = self._parent.real_paths[positions]
        for real_path in requested_real_paths:
            pathmapitem = self.by_real_path(real_path)
            requested_pathmapitems.append(pathmapitem)
        return requested_pathmapitems


class TreeNodeSequenceMimic(MimicsSequence):
    """
    Examples:
        >>> from treepathmap import TreeNodePaths, TreeNodeItem, TreeNodeItems, map_tree
        >>> sample_tree = {"a": {"b": {"c": "leaf"}}}
        >>> sample_items = TreeNodeItems(
        ...     TreeNodeItem(TreeNodePaths([["a"], ["x"]], {"k1": 1}), sample_tree),
        ...     TreeNodeItem(TreeNodePaths([["a", "b"], [""]], {"k1": 2}), sample_tree["a"]),
        ...     TreeNodeItem(TreeNodePaths([["a", "b", "c"], ["z"]], {"k1": 3}), sample_tree["a"]["b"])
        ... )
        ...
        >>> sample_map = PathMap(PathMapTable(sample_items))
        >>> sample_map.tree_items[0]
        {'b': {'c': 'leaf'}}
        >>> sample_map.tree_items[1]
        {'c': 'leaf'}
        >>> sample_map.tree_items[2]
        'leaf'
        >>> sample_map.tree_items["->a"]
        {'b': {'c': 'leaf'}}
        >>> sample_map.tree_items["->a->b"]
        {'c': 'leaf'}
        >>> sample_map.tree_items["->a->b->c"]
        'leaf'
        >>> sample_map.tree_items[::2]
        [{'b': {'c': 'leaf'}}, 'leaf']

        >>> sample_tree = {"a": {"b": {"c": "leaf"}}}
        >>> sample_map = map_tree(sample_tree)
        >>> sample_map.tree_items[2] = "changed value"
        >>> sample_tree
        {'a': {'b': {'c': 'changed value'}}}
        >>> sample_map.tree_items[2] = {"more": "items"}
        >>> sample_tree
        {'a': {'b': {'c': {'more': 'items'}}}}
        >>> sample_map.real_paths
        Index(['->a', '->a->b', '->a->b->c', '->a->b->c->more'], dtype='object')
        >>> sample_map.tree_items[3]
        'items'
        >>> sample_map.tree_items[1] = {"overriding": "removes items"}
        >>> sample_tree
        {'a': {'b': {'overriding': 'removes items'}}}
        >>> sample_map
        ->a
        ->a->b
        ->a->b->overriding
        >>> sample_map.tree_items[3]
        Traceback (most recent call last):
        IndexError: Index 3 out of range of 3 TreeNodeItems
        >>> sample_map.tree_items[::2] = "First occurrence is overridden."
        >>> sample_tree
        {'a': 'First occurrence is overridden.'}
        >>> sample_map
        ->a

    """

    def __init__(self, parent_pathmap: "PathMap"):
        self._parent = parent_pathmap

    def __len__(self):
        return len(self._parent)

    def __iter__(self):
        for real_path in self._parent.real_paths:
            treeitem = self.by_real_path(real_path)
            yield treeitem

    @overload
    def __getitem__(self, key: str) -> ATreeNodeItem:
        pass

    @overload
    def __getitem__(self, index: int) -> ATreeNodeItem:
        pass

    @overload
    def __getitem__(self, index_slice: slice) -> Iterable[ATreeNodeItem]:
        pass

    def __getitem__(
        self, key: Union[int, str, slice]
    ) -> Union[ATreeNodeItem, Iterable[ATreeNodeItem]]:
        """
        Retrieves a tree item at the given *real_path* or the x-th integer
        *position* within its PathMap. If a *slice* is given all corresponding
        tree items are returned.

        Args:
            key(Union[int, str, slice]):
                Either a *real_path*, an integer *position* or a slice.

        Returns:
            Union[APathMapTreeItem, Iterable[APathMapTreeItem]]:
                A tree item for a *real_path* or integer *position* or a list
                of tree items for a *slice*.
        """
        if key is None:
            return self._parent.tree_data
        if isinstance(key, int):
            return self.by_position(key)
        if isinstance(key, str):
            return self.by_real_path(key)
        if isinstance(key, slice):
            return self.by_slice(key)
        raise IndexError(
            "Neither a real_path, a integer position or a slice were given."
        )

    def by_real_path(self, real_path: str) -> ATreeNodeItem:
        """
        Retrives a tree item by its *real_path*.

        Args:
            real_path(str):
                The requested tree item's real path.

        Returns:
            AnTreeItem:
                Tree item at the provided *real_path*.
        """
        requested_path_map_item = self._parent.get_path_map_item_by_real_path(real_path)
        parent_of_tree_item = requested_path_map_item.parent_tree_node
        return parent_of_tree_item[requested_path_map_item.real_key]

    def by_position(self, position: int) -> Optional[ATreeNodeItem]:
        """
        Retrives the treeitem by an integer index, based on the tree items
        row within the TreeMap.

        Args:
            position(int):
                Row's index within the PathMap

        Returns:
            AnTreeItem:
                Tree item at the position.
        """
        assert isinstance(position, int), "position has to be an integer"
        assert position >= 0, "position needs to be a positive integer or zero."
        if self._parent.is_empty():
            return None
        try:
            real_path = self._parent.real_paths[position]
        except IndexError:
            raise IndexError(
                "Index {} out of range of {} {}".format(
                    position, len(self), TreeNodeItems.__name__
                )
            )
        requested_path_map_item = self._parent.get_path_map_item_by_real_path(real_path)
        parent_of_treeitem = requested_path_map_item.parent_tree_node
        return parent_of_treeitem[requested_path_map_item.real_key]

    def by_slice(self, positions: slice) -> Iterable[ATreeNodeItem]:
        """
        Retrives the treeitem by an integer index, based on the tree items
        row within the TreeMap.

        Args:
            positions(slice):
                Row's index within the PathMap

        Returns:
            AnTreeItem:
                Tree item at the position.
        """
        if self._parent.is_empty():
            return []
        requested_real_paths = self._parent.real_paths[positions]
        requested_tree_items = []
        for real_path in requested_real_paths:
            # noinspection PyTypeChecker
            tree_item = self.by_real_path(real_path)
            requested_tree_items.append(tree_item)
        return requested_tree_items

    def __setitem__(self, key: Union[str, int, slice], value: Any):
        if isinstance(key, int):
            return self.set_value_of_tree_item_by_position(key, value)
        if isinstance(key, str):
            return self.set_value_of_tree_item_by_real_path(key, value)
        if isinstance(key, slice):
            return self.set_value_of_tree_items(key, value)
        raise IndexError(
            "Neither a real_path, a integer position or a slice were given."
        )

    def set_value_of_tree_item_by_real_path(self, real_path: str, value: Any):
        assert isinstance(real_path, str), "real_path needs to be a string."
        path_map_item = self._parent.tree_node_items.by_real_path(real_path)
        path_map_item.prime_value = self._parent.map_additional_tree_items(
            value, path_map_item
        )

    def set_value_of_tree_item_by_position(self, position: int, value: Any):
        assert isinstance(position, int), "position needs to be an integer."
        assert position >= 0, "position needs to be a positive integer or zero."
        path_map_item = self._parent.tree_node_items.by_position(position)
        path_map_item.prime_value = self._parent.map_additional_tree_items(
            value, path_map_item
        )

    def set_value_of_tree_items(self, positions: slice, value: Any):
        assert isinstance(positions, slice), "position needs to be a slice."
        selected_path_map_items = self._parent.tree_node_items.by_slice(positions)
        for path_map_item in selected_path_map_items:
            was_removed = not self._parent.real_path_exists(path_map_item.real_path)
            if was_removed:
                continue
            path_map_item.prime_value = self._parent.map_additional_tree_items(
                value, path_map_item
            )


DEFAULT_METAATTRIBUTES_COLUMN_NAME = "meta_attributes"


def _do_nothing(passed_this_through: Any) -> Any:
    """
    Does nothing with an argument.

    Args:
        passed_this_through:
            The input to be passed through.

    Returns:
        Any:
            The unchanged input.
    """
    return passed_this_through


def map_tree_items(
    potential_tree: Union[Sequence, Mapping],
    parent_path_map_item: Optional[TreeNodeItem] = None,
    item_is_a_leaf: Optional[DetectATreeLeaf] = None,
    modify_default_path_map_item: Optional[
        Callable[[TreeNodeItem], TreeNodeItem]
    ] = None,
) -> TreeNodeItems:
    """

    Examples:
        >>> from treepathmap.maps import map_tree_items
        >>> sample_tree = {"1st": [["a set", "of"], ["items"]]}
        >>> mapped_path_map_items = map_tree_items(sample_tree)
        >>> for real_path, item in mapped_path_map_items.items():
        ...     print(item)
        TreeNodeItem(->1st: in a dict)
        TreeNodeItem(->1st->0: in a list)
        TreeNodeItem(->1st->1: in a list)
        >>> mapped_path_map_items.real_paths
        ['->1st', '->1st->0', '->1st->1']
        >>> def add_path_and_meta_attributes(a_path_map_item):
        ...     a_path_map_item.add_meta_attributes({"some": "metadata"})
        ...     # don't give this additional path example to much credit.
        ...     a_nonsense_path = 0
        ...     the_value_of_this_item = a_path_map_item.prime_value
        ...     for char in str(the_value_of_this_item):
        ...         a_nonsense_path += ord(char)
        ...     # the additional path is set to location 1, first place after
        ...     # the real path generated by the default mapping method.
        ...     a_path_map_item.set_tree_path(1, a_nonsense_path)
        ...     return a_path_map_item
        ...
        >>> extended_path_map_items = map_tree_items(
        ...     sample_tree,
        ...     modify_default_path_map_item=add_path_and_meta_attributes
        ... )
        ...
        >>> extended_path_map_items.print_full_items()
        TreePath:
            path-0: ->1st
            path-1: ->2158
            metadata: {'some': 'metadata'}
            parent container type: dict
        TreePath:
            path-0: ->1st->0
            path-1: ->1090
            metadata: {'some': 'metadata'}
            parent container type: list
        TreePath:
            path-0: ->1st->1
            path-1: ->808
            metadata: {'some': 'metadata'}
            parent container type: list

    Args:
        potential_tree:
            The potential nested tree to be mapped.

        parent_path_map_item(Optional[TreeNodeItem]):
            The path map item of the parent container, the *potential tree* is
            located in. The default option *None* means the *potential tree*
            is the root container.

        item_is_a_leaf(Optional[DetectATreeLeaf]):
            The custom Callable *item_is_a_leaf* defines if an item is a leaf
            or a node. By default treenodedefinition.this_item_is_a_leaf is
            used.

        modify_default_path_map_item(Optional[Callable[[TreeNodeItem], TreeNodeItem]]):
            Defines a Callable, which enables an additional declaration of
            tree paths and meta potential_tree of the default real path TreeNodeItem
            directly after its creation.

    Raises:
        TypeError:
            if *tree_item_to_map* is not a Sequence or Mapping.

    Returns:
        TreeNodeItems
    """
    if item_is_a_leaf is None:
        item_is_a_leaf = treenodedefinition.this_item_is_a_leaf

    this_is_not_a_tree = item_is_a_leaf(potential_tree)
    if this_is_not_a_tree:
        raise TypeError(
            "Expected a Sequence or Mapping, got '{}' instead.".format(
                type(potential_tree)
            )
        )

    parent_path_map_item_is_assumed_to_be_the_root = parent_path_map_item is None
    if parent_path_map_item_is_assumed_to_be_the_root:
        parent_path_map_item = TreeNodeItem(TreeNodePaths([RootNodePath()]))

    if modify_default_path_map_item is None:
        modify_default_path_map_item = _do_nothing
    elif not isinstance(modify_default_path_map_item, Callable):
        raise TypeError("`modify_default_path_map_item` needs to be a Callable.")

    mapped_tree_items = _map_tree(
        tree_item_to_map=potential_tree,
        parent_path_map_item=parent_path_map_item,
        this_is_a_leaf=item_is_a_leaf,
        modify_default_path_map_item=modify_default_path_map_item,
    )
    return mapped_tree_items


def map_tree(
    potential_tree: Union[Sequence, Mapping],
    parent_path_map_item: Optional[TreeNodeItem] = None,
    item_is_a_leaf: Optional[DetectATreeLeaf] = None,
    modify_default_path_map_item: Optional[
        Callable[[TreeNodeItem], TreeNodeItem]
    ] = None,
) -> "PathMap":
    """
    Maps a nested collection to a PathMap.

    Args:
        potential_tree:
            The potential nested tree to be mapped.

        parent_path_map_item(Optional[TreeNodeItem]):
            The path map item of the parent container, the *potential tree* is
            located in. The default option *None* means the *potential tree*
            is the root container.

        item_is_a_leaf(Optional[DetectATreeLeaf]):
            The custom Callable *item_is_a_leaf* defines if an item is a leaf
            or a node. By default treenodedefinition.this_item_is_a_leaf is
            used.

        modify_default_path_map_item(Optional[Callable[[TreeNodeItem], TreeNodeItem]]):
            Defines a Callable, which enables an additional declaration of
            tree paths and meta potential_tree of the default real path TreeNodeItem
            directly after its creation.

    Raises:
        TypeError:
            if *tree_item_to_map* is not a Sequence or Mapping.

    Returns:
        PathMap

    Examples:
        >>> from treepathmap.maps import map_tree
        >>> sample_tree = {"1st": [["a set", "of"], ["items"]]}
        >>> sample_map = map_tree(sample_tree)
        >>> print(sample_map)
                 meta_attributes
        ->1st               ////
        ->1st->0            ////
        ->1st->1            ////
        >>> def add_path_and_meta_attributes(a_path_map_item):
        ...     a_path_map_item.add_meta_attributes({"some": "metadata"})
        ...     # don't give this additional path example to much credit.
        ...     a_nonsense_path = 0
        ...     the_value_of_this_item = a_path_map_item.prime_value
        ...     for char in str(the_value_of_this_item):
        ...         a_nonsense_path += ord(char)
        ...     # the additional path is set to location 1, first place after
        ...     # the real path generated by the default mapping method.
        ...     a_path_map_item.set_tree_path(1, a_nonsense_path)
        ...     return a_path_map_item
        ...
        >>> extended_path_map_items = map_tree_items(
        ...     sample_tree,
        ...     modify_default_path_map_item=add_path_and_meta_attributes
        ... )
        ...
        >>> extended_path_map_items.print_full_items()
        TreePath:
            path-0: ->1st
            path-1: ->2158
            metadata: {'some': 'metadata'}
            parent container type: dict
        TreePath:
            path-0: ->1st->0
            path-1: ->1090
            metadata: {'some': 'metadata'}
            parent container type: list
        TreePath:
            path-0: ->1st->1
            path-1: ->808
            metadata: {'some': 'metadata'}
            parent container type: list

    """
    mapped_tree_items = map_tree_items(
        potential_tree=potential_tree,
        parent_path_map_item=parent_path_map_item,
        item_is_a_leaf=item_is_a_leaf,
        modify_default_path_map_item=modify_default_path_map_item,
    )
    path_map_table = PathMapTable(tree_node_items=mapped_tree_items)
    path_map = PathMap(path_map_table=path_map_table)
    return path_map


def iter_tree_items(
    potential_tree: Union[Sequence, Mapping],
) -> Generator[Tuple[Hashable, Any], None, None]:
    """
    Iterates through the potential tree of Sequences or Mappings
    returning the integer index or key with the corresponding value.

    Examples:
        >>> from treepathmap.maps import iter_tree_items
        >>> list(iter_tree_items({"1st": "item", "2nd": "one"}))
        [('1st', 'item'), ('2nd', 'one')]
        >>> list(iter_tree_items([["a", "item"], ["another"]]))
        [(0, ['a', 'item']), (1, ['another'])]

    Args:
        potential_tree(Union[Sequence, Mapping]):
            A potentially nested tree.

    Returns:
        Generator[Tuple[Hashable, Any], None, None]:
            Yields items of Sequences or Mappings as (index, value) or
            (key, value) pairs.
    """
    if isinstance(potential_tree, Sequence):
        for index, item in enumerate(potential_tree):
            yield index, item
    elif isinstance(potential_tree, Mapping):
        for key, item in potential_tree.items():
            yield key, item


def _map_tree(
    tree_item_to_map: Union[Sequence, Mapping],
    parent_path_map_item: TreeNodeItem,
    this_is_a_leaf: DetectATreeLeaf,
    modify_default_path_map_item: Callable[[TreeNodeItem], TreeNodeItem],
) -> TreeNodeItems:
    """
    Worker function of map_tree after argument check and setting of defaults.
    """
    mapped_tree_items = TreeNodeItems()
    for real_key_of_child, child_tree_item in iter_tree_items(tree_item_to_map):
        childs_path_map_item = parent_path_map_item.join(
            [[real_key_of_child]], ref_parent_container=tree_item_to_map
        )
        modified_childs_path_map_item = modify_default_path_map_item(
            childs_path_map_item
        )
        mapped_tree_items.add(modified_childs_path_map_item)
        the_child_is_a_leaf = this_is_a_leaf(child_tree_item)
        if the_child_is_a_leaf:
            continue
        sub_path_map_items = _map_tree(
            child_tree_item,
            parent_path_map_item=modified_childs_path_map_item,
            this_is_a_leaf=this_is_a_leaf,
            modify_default_path_map_item=modify_default_path_map_item,
        )
        mapped_tree_items.add_many(sub_path_map_items)
    return mapped_tree_items


def wh_is(attribute_name: str, value: Union[int, str]) -> str:
    """
    Makes a 'where is' search pattern. Using this method ensures the
    correct key-value delimiter within the search pattern.

    Args:
        attribute_name(str):
            The attribute of which the value is choosen.

        value(Union[int, str]):
            The value of the attribute to choose.

    Returns:
        str

    Examples:
        >>> from treepathmap import wh_is
        >>> wh_is("a", "b")
        'a/b'

    """
    return "{}{}{}".format(attribute_name, TREE_PATH_METAATTRIBUTE_DELIMITER, value)


DETAILED_REPRESENTATION_LINE_INDENT = "    "


def _make_additional_path_representation(
    additional_paths: List[Union[str, TreeNodePath]],
    names_of_additional_paths: List[str],
    line_indent: str,
) -> str:
    """
    Make representation of additional paths of a path map item. Non existing
    paths are not shown.

    Examples:
        >>> from treepathmap import TreeNodePath
        >>> from treepathmap.maps import _make_additional_path_representation as test_func
        >>> print(test_func([], [], "    "))
        <BLANKLINE>
        >>> print(test_func([TreeNodePath("first", "path")], ["1st"], "    "))
            1st: ->first->path
        <BLANKLINE>
        >>> print(
        ...     test_func(
        ...         [TreeNodePath("first", "path"), TreeNodePath("second", "path")],
        ...         ["1st", "2nd"],
        ...         "    "
        ...     )
        ... )
            1st: ->first->path
            2nd: ->second->path
        <BLANKLINE>
        >>> print(
        ...     test_func([
        ...         TreeNodePath("first", "path"),
        ...         TreeNodePath(),
        ...         TreeNodePath("third", "path")
        ...         ],
        ...         ["1st", "2nd", "3rd"],
        ...     "    "
        ...     )
        ... )
            1st: ->first->path
            3rd: ->third->path
        <BLANKLINE>

    Args:
        additional_paths(List[Union[str, TreeNodePath]]):
            Additional paths of the path map item, without the real path.

        names_of_additional_paths(List[str]):
            The names these paths should get.

        line_indent:
            Line indent of each additional path line.

    Returns:
        str
    """
    no_paths_then_no_output = len(additional_paths) == 0
    if no_paths_then_no_output:
        return ""

    strings_of_paths = []
    not_enough_names_for_additional_paths = len(additional_paths) > len(
        names_of_additional_paths
    )
    if not_enough_names_for_additional_paths:
        raise ValueError(
            "Given `additional_path_names` are less then the given path map item "
            "requests."
        )

    for index, path in enumerate(additional_paths):
        converted_path = str(path)

        current_path_is_empty_therefore_discard_it = not converted_path
        if current_path_is_empty_therefore_discard_it:
            continue

        path_name = names_of_additional_paths[index]
        strings_of_paths.append(
            "{}{}: {}".format(line_indent, path_name, converted_path)
        )

    no_paths_left_then_put_empty_string_out = not strings_of_paths
    if no_paths_left_then_put_empty_string_out:
        return ""

    output_of_paths = "\n".join(strings_of_paths)
    return output_of_paths + "\n"


def _make_meta_attribute_representation(meta_attributes: dict, line_indent: str) -> str:
    """
    Examples:
        >>> from treepathmap.maps import _make_meta_attribute_representation as test_func
        >>> test_func({}, "    ")
        ''
        >>> print(test_func({}, "    "))
        <BLANKLINE>
        >>> print(test_func({"meta": "attribute"}, "    "))
            meta attributes: {'meta': 'attribute'}
        <BLANKLINE>

    Args:
        meta_attributes:
        line_indent:

    Returns:

    """
    empty_metaattributes_then_discard = not meta_attributes
    if empty_metaattributes_then_discard:
        return ""
    return "{}meta attributes: {}\n".format(line_indent, meta_attributes)


def _make_detailed_representation(
    tree_node_items: Union[TreeNodeItems, List[TreeNodeItem]],
    additional_path_names: List[str],
) -> str:
    """
    Examples:
        >>> from treepathmap.maps import map_tree_items
        >>> from treepathmap.maps import _make_detailed_representation
        >>> mapped_items = map_tree_items({"a": 1, "b": 2, "c": 3})
        >>> print(_make_detailed_representation(mapped_items, []))
        ->a
        ->b
        ->c
        >>> mapped_items["->a"].add_meta_attributes({"this": "one"})
        >>> print(_make_detailed_representation(mapped_items, []))
        ->a
            meta attributes: {'this': 'one'}
        ->b
        ->c
        >>> mapped_items["->b"].set_tree_path(1, "an", "additional", "path")
        >>> print(_make_detailed_representation(mapped_items, ["additional_path_1"]))
        ->a
            meta attributes: {'this': 'one'}
        ->b
            additional_path_1: ->an->additional->path
        ->c

    Args:
        tree_node_items:
        additional_path_names:

    Returns:
        str
    """
    assert isinstance(
        tree_node_items, Mapping
    ), "tree_node_items must be a Mapping like Dict[RealPath, TreeNodeItem]."
    item_representations = []
    item_printer = _make_detailed_tree_node_item_representation
    for real_path, path_map_item in tree_node_items.items():
        item_representation = item_printer(path_map_item, additional_path_names)
        item_representations.append(item_representation)
    return "\n".join(item_representations)


def _pop_indexes_of_non_equal_items(
    path_map_table, real_paths_to_check, target_value
) -> pandas.Index:
    indexes_to_drop = []
    for real_path in real_paths_to_check:
        path_map_item = path_map_table.get_path_map_item_by_real_path(real_path)
        if path_map_item.prime_value == target_value:
            continue
        indexes_to_drop.append(real_path)
    return real_paths_to_check.drop(indexes_to_drop)


def _make_detailed_tree_node_item_representation(
    item: TreeNodeItem, additional_path_names: List[str]
) -> str:
    """
    Generates a detailed string representation of a path map item.

    Examples:
        >>> from treepathmap import TreeNodeItem, TreeNodePaths
        >>> from treepathmap.maps import _make_detailed_tree_node_item_representation
        >>> sample_item = TreeNodeItem(
        ...     TreeNodePaths([
        ...         ["real", "path", "parts"],
        ...         ["can", "be", "anything"]],
        ...         {"meta": "attributes", "for": "specific", "selection": "purpose"},
        ...     ),
        ...     ref_parent_container={"parts": {"the": "tree node of this item"}}
        ... )
        ...
        >>> additional_sample_path_names = ["additional_path_1"]
        >>> print(_make_detailed_tree_node_item_representation(
        ...     sample_item, additional_sample_path_names)
        ... )
        ->real->path->parts
            additional_path_1: ->can->be->anything
            meta attributes: {'meta': 'attributes', 'for': 'specific', 'selection': 'purpose'}
        >>> sample_item = TreeNodeItem(
        ...     TreeNodePaths([["real", "path", "parts"]],
        ...     ),
        ...     ref_parent_container={"parts": {"the": "tree node of this item"}}
        ... )
        ...
        >>> print(_make_detailed_tree_node_item_representation(
        ...     sample_item, additional_sample_path_names)
        ... )
        ->real->path->parts

    Args:
        item(TreeNodeItem):
            The path map item of which a detailed string representation is
            generated.

        additional_path_names(Optional[List[str]]):
            The names of the paths.

    Returns:
        str:
            Detailed representation of this path item.
    """
    real_path = item.tree_node_paths[0]
    line_indent = DETAILED_REPRESENTATION_LINE_INDENT
    real_path_representation = str(real_path) + "\n"
    additional_paths = item.tree_node_paths[1:]
    additional_path_representation = _make_additional_path_representation(
        additional_paths, additional_path_names, line_indent
    )
    meta_attribute_representation = _make_meta_attribute_representation(
        item.meta_attributes, line_indent
    )
    output = (
        real_path_representation
        + additional_path_representation
        + meta_attribute_representation
    )
    removed_last_trailing_newline = output[:-1]
    return removed_last_trailing_newline


class APathMapFrame(object):
    def __new__(cls, *args, **kwargs):
        if isinstance(cls, APathMapFrame):
            raise NotImplementedError("APathMapFrame cannot be instanced directly.")
        return object.__new__(cls)

    def __init__(self):
        self._selectable_paths: SelectablePaths = None

    def __getitem__(self, columns):
        return self._selectable_paths[columns]

    @property
    def index(self) -> pandas.Index:
        return self._selectable_paths.index

    @property
    def loc(self):
        return self._selectable_paths.loc

    @property
    def columns(self):
        return self._selectable_paths.columns

    @property
    def empty(self):
        return self._selectable_paths.empty

    # @staticmethod
    # def get_path_columns(path_map_table: "PathMapTable") -> List[str]:
    #     """
    #     >>> from pandas import DataFrame
    #     >>> from treepathmap.maps import (
    #     ...     DEFAULT_METAATTRIBUTES_COLUMN_NAME as TESTVAR,
    #     ...     PathMapTable
    #     ... )
    #     >>> test_table = DataFrame(columns=["real_path", "add-1", TESTVAR])
    #     >>> PathMapTable.get_path_columns(test_table)
    #     ['real_path', 'add-1', 'meta_attributes']
    #
    #     Args:
    #         path_map_table:
    #
    #     Returns:
    #
    #     """
    #     warnings.warn(
    #         "Due to restructuring its recommend "
    #         "to grab directly from path_map_table.columns",
    #         DeprecationWarning,
    #     )
    #     return path_map_table.columns.to_list()

    def copy_dataframe(self) -> DataFrame:
        return self._selectable_paths.copy_dataframe()


def _extract_meta_attributes_from_tree_node_items(
    tree_node_items: TreeNodeItems,
) -> Dict[str, Union[int, str]]:
    """
    Examples:
        >>> sample_container = {"a": {"b": "a value"}}
        >>> sample_items = TreeNodeItems(
        ...     TreeNodeItem(TreeNodePaths([["->a"]], {"k1": 1}), sample_container),
        ...     TreeNodeItem(TreeNodePaths([["->a->b"]], {"k1": 2}), sample_container),
        ... )
        >>> from treepathmap.maps import _extract_meta_attributes_from_tree_node_items
        >>> _extract_meta_attributes_from_tree_node_items(sample_items)
        {'->a': {'k1': 1}, '->a->b': {'k1': 2}}

    Args:
        tree_node_items:

    Returns:

    """
    return {
        real_path: item.meta_attributes for real_path, item in tree_node_items.items()
    }


class TagGroups(object):
    """
    Examples:
        >>> from treepathmap.maps import TagGroups
        >>> from treepathmap.selectables import RelatedGroupTags
        >>> from pandas import DataFrame
        >>> sample_tags = DataFrame(
        ...     data=list(range(1, 6)),
        ...     columns=["foo"],
        ...     index=["->a", "->b", "->c", "->d", "->e"]
        ... )
        >>> sample_tags = RelatedGroupTags(tags=sample_tags)
        >>> sample_tags
             foo      where
        ->a    1  //foo/1//
        ->b    2  //foo/2//
        ->c    3  //foo/3//
        ->d    4  //foo/4//
        ->e    5  //foo/5//
        >>> groups = TagGroups()
        >>> groups["sample"] = sample_tags
        >>> sample_group = groups["sample"]
        >>> sample_group.where("foo/1", pre_selection_indexes=["->b", "->c", "->d"])
        Index([], dtype='object')
        >>> sample_group.where("foo/3")
        Index(['->c'], dtype='object')

    """

    def __init__(self):
        self._tag_groups: Dict[str, WhereSelectable] = {}
        self._current_selection: pandas.Index = []
        self._current_group_name: str = ""
        self.items = self._tag_groups.items

    def __getitem__(self, group_name: str):
        if group_name not in self._tag_groups:
            self._tag_groups[group_name] = RelatedGroupTags(name=group_name)
        return self._tag_groups[group_name]

    def __setitem__(self, group_name: str, tag_group: WhereSelectable):
        if not isinstance(tag_group, WhereSelectable):
            raise TypeError(
                "Only Instaces of {} are permitted. "
                "Got {} instead.".format(WhereSelectable.__name__, type(tag_group))
            )
        self._tag_groups[group_name] = tag_group

    def __len__(self):
        return len(self._tag_groups)

    def __iter__(self):
        return iter(self._tag_groups)

    def add_tag_group(self, tag_group_name: str, tag_group: WhereSelectable):
        self._tag_groups[tag_group_name] = tag_group

    # def set_selected_group(self, selected_tag_group_name: str):
    #     warnings.warn("This method will be removed.", DeprecationWarning)
    #     self._current_group_name = selected_tag_group_name

    def get_subsections(self, indexes):
        subsections = []
        for group_name, tags in self._tag_groups.items():
            subsection = tags.get_series(target_indexes=indexes).copy()
            subsections.append(subsection)
        return subsections

    @property
    def where(self) -> WhereSelectable:
        return self._tag_groups[self._current_group_name]


class PathMapTable(APathMapFrame):
    """
    This class represents the table of the real and additional tree paths of
    a mapped tree. It also carries the necessary meta data to handle
    additional tasks of the table.

    Examples:
        >>> from treepathmap.maps import map_tree_items, PathMapTable
        >>> mapped_items = map_tree_items({"a": "item", "another": "item"})
        >>> mapped_items
        TreeNodeItems(->a, ->another)
        >>> sample_tree_data = PathMapTable(tree_node_items=mapped_items)
        >>> sample_tree_data
        ->a
        ->another
        >>> sample_tree_data.real_paths
        Index(['->a', '->another'], dtype='object')
        >>> sample_tree_data.get_position_of_real_path("->another")
        1

        The selection of paths is composed from SelectablePaths.

        >>> sample_tree_data.select("real_path", ["*"])
        Index(['->a', '->another'], dtype='object')
        >>> sample_tree_data.select("real_path", ["g"])
        Index([], dtype='object')
        >>> sample_tree_data.select("real_path", ["a"])
        Index(['->a'], dtype='object')

    """

    def __init__(self, tree_node_items: TreeNodeItems):
        super().__init__()
        self._tree_node_items = tree_node_items
        self._selectable_paths = SelectablePaths(
            tree_path_table=tree_node_items.to_dataframe()
        )
        meta_attribute_map = _extract_meta_attributes_from_tree_node_items(
            tree_node_items=tree_node_items
        )
        self._tags = TagGroups()
        self._tags.add_tag_group(
            tag_group_name=DEFAULT_METAATTRIBUTES_COLUMN_NAME,
            tag_group=IrregularTags(
                name=DEFAULT_METAATTRIBUTES_COLUMN_NAME, meta_items=meta_attribute_map
            ),
        )

    def __repr__(self):
        return self.make_detailed_representation_of_pathmaptable(self)

    @property
    def meta_attributes(self):
        return self._tags[DEFAULT_METAATTRIBUTES_COLUMN_NAME]

    @property
    def tags(self):
        return self._tags

    def select(
        self,
        selection_path_name: str,
        search_parts: List[str],
        pre_selection_indexes: Optional[pandas.Index] = None,
    ) -> pandas.Index:
        """
        Selects tree items on base of the supplied *search_parts*, which are
        parts of the *augmented_paths* within the tree. All parts are
        considered with an *and* condition in between them. Multiple parts
        within a part are considered with an *or* condition in between.

        Examples:
            select("this", "and_that", ["this", "or_this", "or_that"])

        Args:
            selection_path_name(str):
                The name of the paths from which the selection should be done.

            search_parts(List[str]):
                Tree path parts which are parts of the requested tree items
                paths.

            pre_selection_indexes(Optional[pandas.Index]):
                Selection is done from this collection of indexes only.

        Returns:
            PathMapSelection:
                Selection of augmented tree items.
        """
        return self._selectable_paths.select(
            selection_path_name=selection_path_name,
            search_parts=search_parts,
            pre_selection_indexes=pre_selection_indexes,
        )

    def where(
        self,
        selection_path_name: str,
        where_search_parts: List[str],
        pre_selection_indexes: Optional[pandas.Index] = None,
    ) -> pandas.Index:
        """
        Selects tree items on base of the supplied *search_parts*, which are
        parts of the tree items *meta_attributes*. All parts are
        considered with an *and* condition in between them. Multiple parts
        within a part are considered with an *or* condition in between.

        Args:
            *search_parts:
                Tree path parts which are parts of the requested tree items
                paths.

            pre_selection_indexes(Optional[pandas.Index]):
                Selection is done from this collection of indexes only.

        Returns:
            PathMapSelection:
                Selection of augmented tree items.
        """
        even_number_of_arguments = len(where_search_parts) % 2 == 0
        if not even_number_of_arguments:
            raise ValueError("PathMap where_search_parts must come in groups of 2.")

        initial_search_part, target_value = where_search_parts[:2]
        requested_indexes = self._selectable_paths.select(
            selection_path_name=selection_path_name,
            search_parts=[initial_search_part],
            pre_selection_indexes=pre_selection_indexes,
        )
        if requested_indexes.empty:
            return requested_indexes

        requested_indexes = _pop_indexes_of_non_equal_items(
            path_map_table=self,
            real_paths_to_check=requested_indexes,
            target_value=target_value,
        )
        if requested_indexes.empty:
            return requested_indexes

        for path_part, target_value in where_search_parts[2::2]:
            requested_indexes = self._selectable_paths.select(
                initial_search_part, pre_selection_indexes=pre_selection_indexes
            )
            if requested_indexes.empty:
                return requested_indexes
            requested_indexes = _pop_indexes_of_non_equal_items(
                path_map_table=self,
                real_paths_to_check=requested_indexes,
                target_value=target_value,
            )
            if requested_indexes.empty:
                return requested_indexes

        return requested_indexes

    @property
    def real_paths(self) -> pandas.Index:
        """
        The *real paths* locate the tree nodes position within the native
        data structure. Its parts can be used to access the tree node
        like `tree[part_1][..][part_n]`

        Returns:
            pandas.index
        """
        return self._selectable_paths.index

    def get_path_map_item_by_real_path(self, real_path: str) -> TreeNodeItem:
        """
        Retrieves the tree node item of a requested real path.

        Args:
            real_path(str):
                real path of the requested tree item.

        Returns:
            TreeNodeItem
        """
        try:
            requested_path_map_item = self._tree_node_items[real_path]
            return requested_path_map_item
        except KeyError:
            raise KeyError(
                "real_path '{}' doesn't exists in this pathmap.".format(real_path)
            )

    def get_position_of_real_path(self, real_path: str) -> int:
        assert isinstance(real_path, str), "real_path is not a str."
        return self.index.get_loc(real_path)

    @staticmethod
    def get_sub_paths_of_real_path(
        path_table: DataFrame, root_real_path: str
    ) -> List[str]:
        """
        Examples:
            >>> from treepathmap.maps import map_tree_items
            >>> sample_tree = {"a": {"b": {"c": 1, "d": 2}}}
            >>> sample_table = map_tree_items(sample_tree).to_dataframe()
            >>> sample_table[["real_path"]]
                       real_path
            ->a              ->a
            ->a->b        ->a->b
            ->a->b->c  ->a->b->c
            ->a->b->d  ->a->b->d
            >>> PathMapTable.get_sub_paths_of_real_path(sample_table, "->a->b")
            ['->a->b->c', '->a->b->d']

        Args:
            path_table:
                DataFrame containing the *path table* of *path map items*.

            root_real_path:
                Root real path of which all children path should be listed.

        Returns:
            List[str]
        """
        search_pattern = r"^{}{}.*".format(root_real_path, TREE_NODE_PATH_DELIMITER)
        mask = path_table.index.str.match(search_pattern)
        return path_table.index[mask].to_list()

    @staticmethod
    def get_path_indexes(path_map_table: DataFrame, path_column_name: str) -> Index:
        """
        Generates the path indexes
        Associated with initialisation to the tree path table.

        Examples:
            >>> from pandas import DataFrame
            >>> sample_data = [["a", "b"], ["c", ""], ["e", "f"]]
            >>> sample_table = DataFrame(
            ...     sample_data, index=["a", "c", "e"], columns=["real_path", "another"]
            ... )
            >>> from treepathmap import PathMapTable
            >>> PathMapTable.get_path_indexes(sample_table, "another")
            Index(['a', 'e'], dtype='object')

        Args:
            path_map_table(DataFrame):
                Table of real and additional paths.

            path_column_name(str):
                Name of the map's paths.

        Returns:
            Index
        """
        current_paths = path_map_table[path_column_name]
        defined_path_indexes = current_paths != ""
        indexes_of_current_paths = current_paths[defined_path_indexes].index
        return indexes_of_current_paths

    def _drop_path_map_items(self, real_paths_to_drop: List[str]):
        """
        Drops all path map items from the map of these.

        Args:
            real_paths_to_drop: List[str]:
                Real paths of the items, which are dropped.
        """
        self._tree_node_items.drop_items(real_paths=real_paths_to_drop)

    def drop_all_sub_entities_of_real_path(self, real_path_to_drop: str):
        found_real_paths = self.get_sub_paths_of_real_path(
            path_table=self._selectable_paths, root_real_path=real_path_to_drop
        )
        self.drop_all_entities_by_real_paths(real_paths_to_drop=found_real_paths)

    def drop_all_entities_by_real_paths(self, real_paths_to_drop: List[str]):
        """
        Drops path map items and all other related entities within this
        instance.

        Args:
            real_paths_to_drop(List[str]):
                The real paths for which all entities should be dropped.

        """
        self._selectable_paths.drop(real_paths_to_drop, inplace=True)
        self._drop_path_map_items(real_paths_to_drop)

    def insert_additional_tree_items(
        self,
        tree_node_items_to_insert: TreeNodeItems,
        parent_tree_node_item: TreeNodeItem,
    ) -> List[str]:
        """
        Notes:
            This function doesn't check whether the insertion of the mapped
            items is valid or not. It drops all sub paths of the parent path
            map item and insert the new items.

        Args:
            tree_node_items_to_insert:
            parent_tree_node_item:

        Returns:
            List[str]:
                Real paths (indexes) of the inserted items.
        """
        if parent_tree_node_item is None:
            raise ValueError(
                "Path map items cannot be inserted at root level. Use `update` instead."
            )
        if parent_tree_node_item is None:
            raise ValueError(
                "Actions at root level are not supported. "
                "You must provide a valid parent path map item."
            )
        target_path = parent_tree_node_item.real_path
        self.drop_all_sub_entities_of_real_path(real_path_to_drop=target_path)
        insertion_index = self.get_position_of_real_path(real_path=target_path) + 1
        table_of_tree_node_items_to_insert = tree_node_items_to_insert.to_dataframe()
        self._selectable_paths.insert_tree_path_table_section_at(
            table_section_to_insert=table_of_tree_node_items_to_insert,
            insertion_position=insertion_index,
        )

        # add the path map item - instances to the map (dict)
        inserted_real_paths = self._tree_node_items.add_many(tree_node_items_to_insert)
        meta_tags: IrregularTags = self._tags[DEFAULT_METAATTRIBUTES_COLUMN_NAME]
        meta_items = {
            real_path: item.meta_attributes
            for real_path, item in tree_node_items_to_insert.items()
        }
        meta_tags.add_meta_items(meta_items)
        return pandas.Index(inserted_real_paths)

    @staticmethod
    def make_detailed_representation_of_pathmaptable(
        path_map_table: "PathMapTable", selected_indexes: Optional[Index] = None
    ):
        all_path_names = path_map_table.columns
        path_names_without_real_path = all_path_names[1:]
        items_to_put = {}
        if selected_indexes is None:
            selected_indexes = path_map_table.index
        if selected_indexes.empty:
            return "<empty map>"
        for real_path in selected_indexes:
            path_map_item = path_map_table.get_path_map_item_by_real_path(real_path)
            items_to_put[real_path] = path_map_item
        return _make_detailed_representation(items_to_put, path_names_without_real_path)


class PathMapTableBaggage(PathMapTable):
    def __init__(
        self,
        tree_node_items: TreeNodeItems = None,
        selected_map_paths_name_or_index: Union[str, int] = 0,
    ):
        super().__init__(tree_node_items=tree_node_items)
        self.path_column_names = APathMapFrame.get_path_columns(path_map_table=self)
        self._path_indexes: Dict[str, pandas.Index] = {}
        self._analyse_tree_path_table()
        self._current_path_name = self._get_map_paths_name(
            selected_map_paths_name_or_index
        )
        self._root = None

        an_item_in_root = self.find_path_map_item_of_root(tree_node_items)
        if an_item_in_root is not None:
            self._root = an_item_in_root.parent_container

    def get_indexes(self) -> Index:
        warnings.warn("This method should be removed.", DeprecationWarning)
        return Index(list(self.map_of_path_map_items))

    def get_root_path_map_item(self):
        warnings.warn("This method should be removed.", DeprecationWarning)
        additional_path_count = len(self.path_column_names) - 1
        root_path = [RootNodePath()]
        if additional_path_count > 0:
            tree_paths = root_path + [""] * additional_path_count
        else:
            tree_paths = root_path
        return TreeNodeItem(
            tree_node_paths=TreeNodePaths(tree_paths), ref_parent_container=self._root
        )

    @staticmethod
    def find_path_map_item_of_root(
        mapped_path_map_items: Dict[str, TreeNodeItem]
    ) -> TreeNodeItem:
        warnings.warn("This method should be removed.", DeprecationWarning)
        for real_path, a_path_map_item in mapped_path_map_items.items():
            is_a_path_in_root = real_path.count(TREE_NODE_PATH_DELIMITER) == 1
            if is_a_path_in_root:
                return a_path_map_item
        return None

    @staticmethod
    def create_path_indexes(
        path_table: DataFrame, path_column_names: List[str]
    ) -> dict:
        warnings.warn("This method should be removed.", DeprecationWarning)
        return {
            column_name: PathMapTable.get_path_indexes(path_table, column_name)
            for column_name in path_column_names
        }

    @property
    def current_path_name(self) -> str:
        """
        Name of the current used paths. By default the *real path* is used.

        Returns:
            str
        """
        warnings.warn("This method should be removed.", DeprecationWarning)
        return self._current_path_name

    @property
    def path_indexes(self) -> dict:
        """

        Returns:

        """
        warnings.warn("This method should be removed.", DeprecationWarning)
        return self._path_indexes

    def _analyse_tree_path_table(self):
        warnings.warn("This method should be removed.", DeprecationWarning)
        assert isinstance(
            self.path_table, DataFrame
        ), "self.path_map_table should be a DataFrame"
        self._path_indexes = self.create_path_indexes(
            self.path_table, self.path_column_names
        )

    def _update_after_change(self):
        warnings.warn("This method should be removed.", DeprecationWarning)
        self._path_indexes = self._create_path_indexes()

    def _create_path_indexes(self) -> dict:
        warnings.warn("This method should be removed.", DeprecationWarning)
        return PathMapTable.create_path_indexes(self.path_table, self.path_column_names)

    def _get_map_paths_name(self, map_paths_name_or_index: Union[str, int]):
        warnings.warn("This method should be removed.", DeprecationWarning)
        assert isinstance(
            map_paths_name_or_index, (str, int)
        ), "The selection needs to be an int or str."
        if isinstance(map_paths_name_or_index, int):
            return self.path_column_names[map_paths_name_or_index]
        assert (
            map_paths_name_or_index in self.path_column_names
        ), "The name of the map's paths does not exists."
        return map_paths_name_or_index


class APathMappingBehavior(ABC):
    """
    Defines the mapping behavior of a *path map*.
    """

    @abstractmethod
    def item_is_a_leaf(self, potential_tree: Any) -> bool:
        pass

    @abstractmethod
    def modify_default_path_map_item(
        self, default_path_map_item: TreeNodeItem
    ) -> TreeNodeItem:
        pass

    @abstractmethod
    def map_tree_items(
        self,
        potential_tree: Union[Sequence, Mapping],
        parent_path_map_item: Optional[TreeNodeItem] = None,
    ) -> TreeNodeItems:
        pass


class DefaultPathMappingBehavior(APathMappingBehavior):
    def item_is_a_leaf(self, potential_tree: Any) -> bool:
        return treenodedefinition.this_item_is_a_leaf(potential_tree)

    def modify_default_path_map_item(
        self, default_path_map_item: TreeNodeItem
    ) -> TreeNodeItem:
        return default_path_map_item

    def map_tree_items(
        self,
        potential_tree: Union[Sequence, Mapping],
        parent_path_map_item: Optional[TreeNodeItem] = None,
    ) -> TreeNodeItems:
        return map_tree_items(
            potential_tree=potential_tree,
            parent_path_map_item=parent_path_map_item,
            item_is_a_leaf=self.item_is_a_leaf,
            modify_default_path_map_item=self.modify_default_path_map_item,
        )


class _PathMapTagWrapper(object):
    def __init__(self, parent: "PathMap", tags: WhereSelectable):
        self._parent = parent
        self._tags = tags

    def where(self, *search_parts) -> "PathMap":
        selected_indexes = self._tags.where(
            *search_parts, pre_selection_indexes=self._parent.selected_indexes
        )
        return self._parent.from_selection(selected_real_paths=selected_indexes)

    def tag(self, values_to_tag: Dict[str, Union[int, str]]):
        self._tags.tag(
            indexes=self._parent.selected_indexes,
            values_to_tag=values_to_tag,
        )

    def __repr__(self):
        return repr(self._tags)


class _PathMapTagGroups(object):
    def __init__(self, parent: "PathMap"):
        self._parent = parent

    def __getitem__(self, group_key: str) -> TagGroups:
        return _PathMapTagWrapper(
            self._parent, self._parent.path_map_table.tags[group_key]
        )


class PathMap(object):
    """
    A map of a nested collection.
    """

    def __init__(
        self,
        path_map_table: Optional[PathMapTable] = None,
        selected_real_paths: Optional[pandas.Index] = None,
        selection_path_name: Optional[str] = None,
        path_mapping_behavior: Optional[APathMappingBehavior] = None,
    ):
        # noinspection PyUnresolvedReferences
        """
        A map of a nested collection.

        Args:
            path_map_table(Optional[PathMapTable]):
                The table of all real paths and *path map items*, which is the
                basis of each *path map*.

            selected_real_paths(Optional[pandas.Index]):
                The selected real paths (indexes) of this instance.

            selection_path_name(Optional[str]):
                The name of the paths (real or additional paths) this path map
                points to.

            path_mapping_behavior(Optional[APathMappingBehavior]):
                The mapping behavior of this path map, by which new items
                are mapped.

        Examples:

            In this example the map is build from scratch instead using
            :func:`treepathmap.map_tree`, which is the recommend way.

            >>> from treepathmap import (
            ...     TreeNodePaths,
            ...     TreeNodeItem,
            ...     TreeNodeItems,
            ...     PathMapTable
            ... )

        The nested sample collection is kept simple.

            >>> sample_tree = {"a": {"b": {"d": "leaf-1"}, "c": {"e": "leaf-2"}}}

        The *tree node paths* are pointing at items of the collection.
        *Meta attributes* are inherited, what is taken into account here.

            >>> tree_node_paths = [
            ...     TreeNodePaths([["a"], ["x"]], {"k1": 1}),
            ...     TreeNodePaths([["a", "b"], [""]], {"k1": 2, "k2": "n"}),
            ...     TreeNodePaths([["a", "b", "d"], ["y"]], {"k1": 2, "k2": "m"}),
            ...     TreeNodePaths([["a", "c"], [""]], {"k1": 3, "k2": "n"}),
            ...     TreeNodePaths([["a", "c", "e"], ["y"]], {"k1": 3, "k2": "m"})
            ... ]

        The prior block is identical to the following one, which shows the
        joining method of TreeNodePaths.

            >>> a_root_path = TreeNodePaths([RootNodePath()])
            >>> path_1 = a_root_path.join([["a"], ["x"]], {"k1": 1})
            >>> path_11 = path_1.join([["b"], [""]], {"k1": 2, "k2": "n"})
            >>> path_111 = path_11.join([["d"], ["y"]], {"k2": "m"})
            >>> path_21 = path_1.join([["c"], [""]], {"k1": 3, "k2": "n"})
            >>> path_211 = path_21.join([["e"], ["y"]], {"k2": "m"})
            >>> tree_node_paths = [path_1, path_11, path_111, path_21, path_211]

        The *tree node items* resembles the core of the *PathMapTable*, which is
        the basis of the final *PathMap*. Using :func:`treepathmap.map_tree` is
        the recommended way to get a *PathMap*.

            >>> sample_node_items = TreeNodeItems(
            ...     TreeNodeItem(tree_node_paths[0], sample_tree),
            ...     TreeNodeItem(tree_node_paths[1], sample_tree["a"]),
            ...     TreeNodeItem(tree_node_paths[2], sample_tree["a"]["b"]),
            ...     TreeNodeItem(tree_node_paths[3], sample_tree["a"]),
            ...     TreeNodeItem(tree_node_paths[4], sample_tree["a"]["c"]),
            ... )
            ...
            >>> sample_table = PathMapTable(tree_node_items=sample_node_items)
            >>> sample_map = PathMap(sample_table)
            >>> print(sample_map)
                      additional_path_1 meta_attributes
            ->a                     ->x        //k1/1//
            ->a->b                       //k1/2//k2/n//
            ->a->b->d               ->y  //k1/2//k2/m//
            ->a->c                       //k1/3//k2/n//
            ->a->c->e               ->y  //k1/3//k2/m//

        The choosen path column defines the active tree nodes. The default
        column are the *real paths*. In this example the *additional paths*
        has one blank path, which is removed from the view.

            >>> sample_map = PathMap(sample_table)
            >>> sample_map.real_paths
            Index(['->a', '->a->b', '->a->b->d', '->a->c', '->a->c->e'], dtype='object')
            >>> other_view = sample_map[1]
            >>> other_view.real_paths
            Index(['->a', '->a->b->d', '->a->c->e'], dtype='object')

        The choosen paths define the selection and iteration behavior of
        the *path map*. In the following case the paths '->a->b' and '->a->c'
        are omitted, due to a *blank* path in the *additional paths*.

            >>> rows = {
            ...     real_path: row.to_list()
            ...     for real_path, row in other_view.iter_rows()
            ... }
            ...
            >>> from dicthandling import print_tree
            >>> print_tree(rows)
            ->a: ['->a', '->x']
            ->a->b->d: ['->a->b->d', '->y']
            ->a->c->e: ['->a->c->e', '->y']
            >>> selected_map = other_view.select("y")
            >>> print(selected_map)
                      additional_path_1 meta_attributes
            ->a->b->d               ->y  //k1/2//k2/m//
            ->a->c->e               ->y  //k1/3//k2/m//

        Since the *additional paths* are active only '->a->c->e' should be
        selected using the where statement, although '->a->c' also is tagged
        with {k1: 3}.

            >>> reduced_map = selected_map.meta.where(wh_is("k1", "3"))
            >>> print(reduced_map)
                      additional_path_1 meta_attributes
            ->a->c->e               ->y  //k1/3//k2/m//
            >>> reduced_map.select("->a->b->d")
            <empty map>
            >>> reduced_map.real_path_exists("->not->existing")
            False
            >>> reduced_map.real_path_exists("->a->b")
            False
            >>> reduced_map.real_path_exists("->a->c->e")
            True

            >>> for item in reduced_map.tree_node_items:
            ...     print(item)
            TreeNodeItem(->a->c->e: in a dict)

            >>> list(reduced_map.tree_items)
            ['leaf-2']

        The reduced map is switched back to the real paths. Selections from the
        reduced map should not exceed the current selection.

            >>> reduced_map = reduced_map["real_path"]
            >>> reduced_map.selected_indexes
            Index(['->a->c->e'], dtype='object')
            >>> reduced_map.select("a", "*")
            ->a->c->e
                additional_path_1: ->y
                meta attributes: {'k1': 3, 'k2': 'm'}

        By default the first tag group are the meta_attributes, which are an instance
        of :class:`treepathmap.IrregularTags`. The **tags** attribute of the *path map*
        gives access to all *tag groups*. In this example all items with the
        *meta attributes* *k2* being *m* are selected. The new tag group *'ids'*
        is assigned, which can be selected by this tags from the whole map afterwards.


            >>> items_with_k2_is_m = sample_map.tags["meta_attributes"].where("k2/m")
            >>> items_with_k2_is_m.tags["ids"].tag({"category": "foo", "name": "bar"})
            >>> items_with_k2_is_m.tags["ids"]
                      category name                         ids
            ->a->b->d      foo  bar  //category/foo//name/bar//
            ->a->c->e      foo  bar  //category/foo//name/bar//
            >>> sample_map.tags["ids"].where("category/foo")
            ->a->b->d
                additional_path_1: ->y
                meta attributes: {'k1': 2, 'k2': 'm'}
            ->a->c->e
                additional_path_1: ->y
                meta attributes: {'k1': 3, 'k2': 'm'}

        """
        self.path_map_table = path_map_table
        self._tree_node_items = TreeNodeItemSequenceMimic(self)
        self._tree_items = TreeNodeSequenceMimic(self)
        self.path_column_names = path_map_table.columns.to_list()
        self._current_path_name = self.get_path_name(
            path_map_table, selection_path_name
        )
        self._tags = _PathMapTagGroups(parent=self)
        self._mapping_behavior = None
        self.set_path_mapping_behavior(mapping_behavior=path_mapping_behavior)
        if selected_real_paths is None:
            self._selected_indexes = self.path_map_table.index.copy()
        else:
            assert isinstance(
                selected_real_paths, Index
            ), "selected_real_paths must be an pandas.Index"
            self._selected_indexes = selected_real_paths

    def __getitem__(self, index_or_name: Union[int, str]) -> "PathMap":
        if isinstance(index_or_name, int):
            selected_path_name = self.path_map_table.columns[index_or_name]
        elif isinstance(index_or_name, str):
            if index_or_name not in self.path_map_table.columns:
                raise IndexError(
                    "The path column name '' does not exist in this PathMap."
                    "".format(index_or_name)
                )
            selected_path_name = index_or_name
        else:
            raise TypeError(
                "Only integers or string are permitted for selecting the path columns."
            )
        return self.from_selection(
            selected_real_paths=self.get_indexes_for_path_name(selected_path_name),
            selection_path_name=selected_path_name,
        )

        self.choose_path_column(index)
        return self

    def __bool__(self):
        return self.is_empty()

    def __len__(self):
        return len(self._selected_indexes)

    def __repr__(self):
        return PathMapTable.make_detailed_representation_of_pathmaptable(
            self.path_map_table, self._selected_indexes
        )

    def __str__(self):
        return str(self.to_dataframe())

    @property
    def empty(self) -> bool:
        return self._selected_indexes.empty

    @property
    def meta(self):
        return self._tags[DEFAULT_METAATTRIBUTES_COLUMN_NAME]

    @property
    def tags(self):
        return self._tags

    @property
    def real_paths(self) -> Index:
        return self._selected_indexes

    @property
    def selection_path_name(self) -> str:
        """
        States the current name of the paths from which the item selection
        via *select* is performed.

        Returns:
            str
        """
        return self._current_path_name

    @property
    def tree_node_items(self):
        return self._tree_node_items

    @property
    def tree_items(self):
        return self._tree_items

    def from_selection(
        self,
        selected_real_paths: Optional[pandas.Index] = None,
        selection_path_name: Optional[str] = None,
    ):
        if selected_real_paths is None:
            selected_real_paths = self._selected_indexes
        if selection_path_name is None:
            selection_path_name = self.selection_path_name
        return PathMap(
            path_map_table=self.path_map_table,
            selected_real_paths=selected_real_paths,
            selection_path_name=selection_path_name,
            path_mapping_behavior=self._mapping_behavior,
        )

    def real_path_exists(self, real_path: str) -> bool:
        assert isinstance(real_path, str), "real_path is not a string."
        return real_path in self._selected_indexes

    def get_indexes_for_path_name(self, path_name):
        all_indexes = self.path_map_table.get_path_indexes(
            path_map_table=self.path_map_table, path_column_name=path_name
        )
        indexes_within_requested_paths = self._selected_indexes.isin(all_indexes)
        return self._selected_indexes[indexes_within_requested_paths]

    def choose_path_column(self, path_column_index: int):
        warnings.warn("This method will be removed.", DeprecationWarning)
        self._current_path_name = self.path_column_names[path_column_index]
        all_indexes = self.path_map_table.get_path_indexes(
            path_map_table=self.path_map_table, path_column_name=self._current_path_name
        )
        indexes_within_requested_paths = self._selected_indexes.isin(all_indexes)
        self._selected_indexes = self._selected_indexes[indexes_within_requested_paths]

    def get_indexes(self) -> Index:
        warnings.warn(
            "This method will be removed in the next release.", DeprecationWarning
        )
        return self.get_indexes()

    @property
    def selected_indexes(self) -> Index:
        return self._selected_indexes

    def select(self, *search_parts) -> "PathMap":
        """
        Selects tree items on base of the supplied w*search_parts*, which are
        parts of the *augmented_paths* within the tree. All parts are
        considered with an *and* condition in between them. Multiple parts
        within a part are considered with an *or* condition in between.

        Examples:
            select("this", "and_that", ["this", "or_this", "or_that"])

        Args:
            *search_parts:
                Tree path parts which are parts of the requested tree items
                paths.

        Returns:
            PathMapSelection:
                Selection of augmented tree items.
        """
        selected_indexes = self.path_map_table.select(
            selection_path_name=self.selection_path_name,
            search_parts=search_parts,
            pre_selection_indexes=self._selected_indexes,
        )
        return self.from_selection(selected_real_paths=selected_indexes)

    def where(self, *where_search_parts) -> "PathMap":
        """

        Args:
            *search_parts:
                Tree path parts which are parts of the requested tree items
                paths.

        Returns:
            PathMapSelection:
                Selection of augmented tree items.
        """
        selected_indexes = self.path_map_table.where(
            selection_path_name=self.selection_path_name,
            where_search_parts=where_search_parts,
            pre_selection_indexes=self._selected_indexes,
        )
        return self.from_selection(selected_real_paths=selected_indexes)

    def _insert_new_tree_path_data(
        self, target_real_path: str, path_map_table: DataFrame, path_map_meta_objects
    ):
        raise NotImplementedError("add the stuff to the active table.")

    def get_path_map_item_by_real_path(self, real_path: str) -> TreeNodeItem:
        """
        Retrieves the tree node item of a requested real path.

        Args:
            real_path(str):
                real path of the requested tree item.

        Returns:
            TreeNodeItem
        """
        if real_path not in self._selected_indexes:
            raise KeyError("real_path '{}' is not within this map.".format(real_path))
        return self.path_map_table.get_path_map_item_by_real_path(real_path=real_path)

    def get_sub_paths_of_real_path(self, parent_real_path: str) -> List[str]:
        selection_query = create_selection_pattern(parent_real_path, "*")
        selection_to_delete = self._get_selected_indexes(
            selection_query, self.selection_path_name
        )
        return selection_to_delete.index.to_list()

    def _delete_sub_path_of_real_path(self, parent_real_path: str):
        real_paths_to_remove = self._get_sub_paths_of_real_path(parent_real_path)
        self.drop_all_entities_by_real_paths(real_paths_to_remove)

    def map_additional_tree_items(
        self,
        potential_tree: Any,
        parent_tree_node_item: TreeNodeItem,
    ) -> Any:
        """
        Maps additional path map items from a *potential tree*.

        Examples:
            >>> from treepathmap import map_tree
            >>> sample_tree = {"an":{"old": "item"}}
            >>> sample_map = map_tree(sample_tree)
            >>> print(sample_map)
                      meta_attributes
            ->an                 ////
            ->an->old            ////
            >>> sample_map.tree_items["->an"] = {"new": "item", "with": "another"}
            >>> print(sample_map)
                       meta_attributes
            ->an                  ////
            ->an->new             ////
            ->an->with            ////

        Args:
            potential_tree:
            parent_tree_node_item:

        Returns:

        """
        assert isinstance(
            parent_tree_node_item, TreeNodeItem
        ), "parent_tree_node_item must be a {}. Got '{}' instead." "".format(
            TreeNodeItem.__name__, type(parent_tree_node_item)
        )
        if parent_tree_node_item is None:
            raise ValueError(
                "Actions at root level are not supported. "
                "You must provide a valid parent path map item."
            )

        no_container_to_map = self._mapping_behavior.item_is_a_leaf(potential_tree)
        if no_container_to_map:
            self.path_map_table.drop_all_sub_entities_of_real_path(
                parent_tree_node_item.real_path
            )
            self.update_selected_indexes()
            return potential_tree

        # map the container
        fresh_path_map_items = self._mapping_behavior.map_tree_items(
            potential_tree, parent_tree_node_item
        )
        inserted_indexes = self.path_map_table.insert_additional_tree_items(
            tree_node_items_to_insert=fresh_path_map_items,
            parent_tree_node_item=parent_tree_node_item,
        )

        self._selected_indexes = self._selected_indexes.append(inserted_indexes)
        self.update_selected_indexes()
        # return the item, so they can be used further.
        return potential_tree

    def update_selected_indexes(self):
        """
        Updates the selected indexes e.g. real paths regarding the actual
        existing indexes of the *tree path table*.
        """
        indexes_to_check = self._selected_indexes
        remaining_mask = self.path_map_table.real_paths.isin(indexes_to_check)
        self._selected_indexes = self.path_map_table.real_paths[remaining_mask]

    def iter_rows(self) -> Generator[Tuple[str, Series], None, None]:
        for real_path in self._selected_indexes:
            # Within in this class the index of sub table is a str
            # noinspection PyTypeChecker
            treeitem_metadata = self.path_map_table.loc[real_path]
            yield real_path, treeitem_metadata

    def is_empty(self):
        return self.path_map_table.empty

    def sort(self, sorting_method: Optional[Callable[[TreeNodeItem], int]] = None):
        """
        Sorts the items within this map by their augmented path.

        Args:
            sorting_method(Callable[[TreeNodeItem], int], optional):
                Custom method to tag TreeNodeItems of this selection with a
                ascending integer number.
        """
        if sorting_method is None:
            self._default_sort()
        else:
            self._custom_sort(sorting_method)

    def _default_sort(self):
        """
        By default the items are sorted by their augmented path.
        """
        self.path_table = self.path_map_table.sort_values(by=[self.selection_path_name])

    def _custom_sort(self, sorting_method: Optional[Callable[[TreeNodeItem], int]]):
        """
        Sorts the items using a custom user method by the TreeNodeItems.

        Args:
            sorting_method(Callable[[TreeNodeItem], int]):
                Custom method to tag TreeNodeItems of this selection with a
                ascending integer number.
        """
        tagged_real_paths = []
        for path_map_item in self.tree_node_items:
            order_number = sorting_method(path_map_item)
            tagged_real_paths.append([path_map_item.real_path, order_number])
        ordered_real_paths_and_numbers = sorted(tagged_real_paths, key=lambda x: x[1])
        custom_ordered_real_paths = [item[0] for item in ordered_real_paths_and_numbers]
        self.path_map_table = self.path_map_table.loc[custom_ordered_real_paths]

    def _path_name_exist(self, path_name: str) -> bool:
        return path_name in self.path_map_table.columns

    def drop_sub_path_map_items(self, parent_real_path: str):
        """
        Drops all sub path map items and their paths of a certain tree node,
        if these exist.

        Args:
            parent_real_path(str):
                Real path from which all sub paths should be dropped.
        """
        dropping_unix_pattern = "{}{}*".format(
            parent_real_path, TREE_NODE_PATH_DELIMITER
        )
        dropping_query = create_selection_pattern(dropping_unix_pattern)
        real_path_column_name = self.path_column_names[REAL_PATH_INDEX]
        selection_to_drop = self._get_selected_indexes(
            dropping_query, real_path_column_name
        )
        real_paths_to_drop = selection_to_drop.index.to_list()
        self.drop_all_entities_by_real_paths(real_paths_to_drop)

    def to_list(self):
        selected_values = []
        for tree_item in self.tree_items:
            selected_values.append(tree_item)
        return selected_values

    @staticmethod
    def get_path_name(path_map_table: PathMapTable, selection_path_name: str):
        if selection_path_name is None:
            return path_map_table.columns[0]
        if selection_path_name not in path_map_table.columns:
            column_representation = "', '".join(path_map_table.columns)
            raise KeyError(
                "Selection paths '{}' is not in "
                "'{}'".format(selection_path_name, column_representation)
            )
        else:
            return selection_path_name

    def set_path_mapping_behavior(self, mapping_behavior: APathMappingBehavior):
        if mapping_behavior is None:
            self._mapping_behavior = DefaultPathMappingBehavior()
        else:
            self._mapping_behavior = mapping_behavior

    def to_dataframe(self):
        base_path_table = self.path_map_table.loc[self._selected_indexes].copy()
        subsections = self.path_map_table.tags.get_subsections(self._selected_indexes)
        output_frame = pandas.concat([base_path_table, *subsections], axis=1)
        it_are_the_index_paths_show_all = (
            self.selection_path_name == self.path_column_names[0]
        )
        if it_are_the_index_paths_show_all:
            columns_without_real_paths = output_frame.columns.to_list()[1:]
            return output_frame[columns_without_real_paths]
        else:
            paths_count = len(self.path_column_names)
            potential_tag_columns = output_frame.columns.to_list()[paths_count:]
            output_columns = [self.selection_path_name] + potential_tag_columns
            return output_frame[output_columns]