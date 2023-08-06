from typing import (
    Any,
    Dict,
    Mapping,
    Union,
    List,
    Hashable,
    Sequence,
    Generator,
    Iterable,
    Optional,
)
from abc import ABC, abstractmethod

import numpy
import pandas
from pandas import DataFrame, Series
from trashpanda import (
    override_left_with_right_series,
    override_left_with_right_dataframe,
    add_missing_indexes_to_series,
    get_intersection,
    add_columns_to_dataframe,
)

from treepathmap import (
    TreeNodePaths,
    split_tree_path,
    TreePathParts,
    create_selection_pattern,
    convert_to_where_searchable_parts,
    turn_iterables_to_unixfilepatterns,
    convert_metaattributes_to_pathlike,
)

__all__ = [
    "TreeNodeItem",
    "ATreeNodeItem",
    "ATreeNode",
    "TreeNodeItems",
    "select_indexes_from_series",
    "RelatedGroupTags",
    "WhereSelectable",
    "IrregularTags",
]


ATreeNodeItem = object
ATreeNode = Union[Sequence, Mapping]
REAL_PATH_INDEX = 0

PATH_MAP_ITEM_KEYS = ["tree_node_paths", "parent_tree_node"]
MINIMUM_POSSIBLE_PATH_COUNT = 1
DEFAULT_FIRST_PATH_NAME = "real_path"
DEFAULT_PATH_NAME_TEMPLATE = "additional_path_{}"
DEFAULT_METAATTRIBUTES_COLUMN_NAME = "meta_attributes"


def select_sub_series_from_series(
    combined_attributes: Series, selection_pattern: str
) -> Series:
    """
    Returns all entries of the pathmap which fits to the `query` at the
    `target_column_name`.

    Examples:
        >>> from treepathmap.selectables import select_sub_series_from_series
        >>> from treepathmap import convert_to_where_searchable_parts
        >>> search_pattern = convert_to_where_searchable_parts("k1/2")[0]
        >>> empty_series = Series([], index=[], dtype=str)
        >>> select_sub_series_from_series(empty_series, search_pattern)
        Series([], dtype: object)
        >>> from pandas import Series
        >>> sample_series = Series(
        ...     ["/k1/1/", "/k1/2/", "/k1/2/k2/2", "/k1/1/k2/4"],
        ...     name="meta_attributes",
        ...     index=["->a", "->a->b", "->a->b->c", "->a->b->d"]
        ... )
        >>> select_sub_series_from_series(sample_series, search_pattern)
        ->a->b           /k1/2/
        ->a->b->c    /k1/2/k2/2
        Name: meta_attributes, dtype: object
        >>> search_pattern = convert_to_where_searchable_parts("3")[0]
        >>> select_sub_series_from_series(sample_series, search_pattern)
        Series([], Name: meta_attributes, dtype: object)

    Args:
        combined_attributes(Series):
            Table from which items will be selected.

        selection_pattern(str):
            A regular expression by which the entries are selected.

    Returns:
        Series:
            Selected items in regard of the `query` within the
            `target_column_name`.
    """
    assert isinstance(combined_attributes, Series), ""
    selected_indexes = combined_attributes.str.match(selection_pattern)
    selected_map = combined_attributes.loc[selected_indexes]
    return selected_map


def select_indexes_from_series(
    series: Series,
    selection_pattern: str,
    pre_selection_indexes: Optional[pandas.Index] = None,
) -> pandas.Index:
    """
    Returns all entries of the pathmap which fits to the `query` at the
    `target_column_name`.

    Examples:
        >>> from treepathmap.selectables import select_indexes_from_series
        >>> test_column = Series(["Arnold", "Beth", "Ceasar"], name="sample")
        >>> select_indexes_from_series(series=test_column, selection_pattern="Beth")
        Int64Index([1], dtype='int64')

    Args:
        series(DataFrame):
            Table from which items will be selected.

        selection_pattern(str):
            A regular expression by which the entries are selected.

        pre_selection_indexes(pandas.Index):
            Selection is done from this collection of indexes only.

    Returns:
        pandas.Index:
            Selected items in regard of the `query` within the
            `target_column_name`.
    """
    if pre_selection_indexes is not None:
        possible_indexes_mask = series.index.isin(pre_selection_indexes)
        select_from_these_items = series.loc[possible_indexes_mask]
        nothing_remained_then_leave_early = select_from_these_items.empty
        if nothing_remained_then_leave_early:
            return select_from_these_items.index.copy()
    else:
        select_from_these_items = series
    index_mask = select_from_these_items.str.match(selection_pattern)
    return select_from_these_items.index[index_mask]


class TreeNodeItem(Mapping):
    """
    A path map item represents the mapping of a real system path to a virtual
    representation.

    Examples:

        One or more *tree node paths* are assigned to a path map item, being
        able to contain additional meta attributes, by which a selection can
        be applied. Here the item is located in a container at the *key* **path**.

        >>> from treepathmap import TreeNodePaths, TreeNodePath, TreeNodeItem
        >>> paths_of_map_item = TreeNodePaths(
        ...     tree_paths=[
        ...         TreeNodePath("the", "real", "path"),
        ...         TreeNodePath("another", "path")
        ...     ],
        ...     meta_attributes={"meta_1": 1}
        ... )
        ...

        A path map item is defined by either the *tree node paths* and the
        actual container in which the *item* is located. Here the item at the
        key **path** has the value */a_place_somewhere*.

        >>> sample_item = TreeNodeItem(
        ...     tree_node_paths=paths_of_map_item,
        ...     ref_parent_container={"path": "/a_place_somewhere", "some": "thing"}
        ... )
        ...
        >>> sample_item
        TreeNodeItem(->the->real->path: in a dict)
        >>> sample_item.real_key
        'path'
        >>> sample_item.parent_container
        {'path': '/a_place_somewhere', 'some': 'thing'}
        >>> sample_item.prime_value
        '/a_place_somewhere'
        >>> sample_item.meta_attributes
        {'meta_1': 1}

    """

    def __init__(
        self,
        tree_node_paths: TreeNodePaths,
        ref_parent_container: ATreeNode = None,
    ):
        if not isinstance(tree_node_paths, TreeNodePaths):
            raise TypeError(
                "Expected TreeNodePaths for *tree_node_paths*, got {} instead".format(
                    tree_node_paths.__class__.__name__
                )
            )
        self.tree_node_paths = tree_node_paths
        self.parent_tree_node = ref_parent_container
        real_path = str(self.tree_node_paths.tree_paths[0])
        self._container_key = split_tree_path(real_path)[-1]

    def __iter__(self):
        return iter(PATH_MAP_ITEM_KEYS)

    def __getitem__(self, item):
        if item == PATH_MAP_ITEM_KEYS[0]:
            return self.tree_node_paths
        if item == PATH_MAP_ITEM_KEYS[1]:
            return self.parent_tree_node
        raise KeyError(
            "{} only contains keys {}".format(
                self.__class__.__name__, PATH_MAP_ITEM_KEYS
            )
        )

    def __len__(self):
        return 2

    @property
    def path_count(self):
        return self.tree_node_paths.path_count

    @property
    def real_key(self) -> Hashable:
        """
        The real key is the key (either index for sequences or hashable for mappings)
        by which the item is assigned within the container.

        Returns:
            Hashable
        """
        return self.tree_node_paths.tree_paths[0].container_key

    @property
    def prime_value(self) -> Any:
        """
        The prime value is the value assigned within the container at

        Returns:

        """
        return self.parent_tree_node[self.real_key]

    @property
    def meta_attributes(self):
        return self.tree_node_paths.meta_attributes

    @property
    def parent_container(self):
        return self.parent_tree_node

    @property
    def real_path(self) -> str:
        return str(self.tree_node_paths.tree_paths[REAL_PATH_INDEX])

    @prime_value.setter
    def prime_value(self, new_value: Any):
        self.parent_tree_node[self.real_key] = new_value

    def join(
        self,
        tree_sub_paths: List[TreePathParts] = "",
        meta_attributes: dict = None,
        ref_parent_container=None,
    ) -> "TreeNodeItem":
        """
        Examples:
            >>> sample_data = {"level_0": {"level_1": 1}}
            >>> from treepathmap import TreeNodePaths, RootNodePath, TreeNodePath
            >>> root_item = TreeNodeItem(TreeNodePaths([RootNodePath()]))
            >>> level_0 = root_item.join(
            ...     [TreeNodePath("level_0")],
            ...     ref_parent_container=sample_data
            ... )
            ...
            >>> print(level_0)
            TreeNodeItem(->level_0: in a dict)
            >>> level_1 = level_0.join(
            ...     [['level_1']],
            ...     ref_parent_container=sample_data["level_0"]
            ... )
            ...
            >>> print(level_1)
            TreeNodeItem(->level_0->level_1: in a dict)

        Args:
            tree_sub_paths:
            meta_attributes:
            ref_parent_container:

        Returns:
            TreeNodeItem
        """
        child_tree_node_paths = self.tree_node_paths.join(
            tree_sub_paths=tree_sub_paths, meta_attributes=meta_attributes
        )
        return TreeNodeItem(
            child_tree_node_paths, ref_parent_container=ref_parent_container
        )

    def add_meta_attributes(self, additional_meta_attributes: dict):
        self.tree_node_paths.add_meta_attributes(additional_meta_attributes)

    def set_tree_path(self, index_of_path: int, *tree_node_path_parts: TreePathParts):
        self.tree_node_paths.set_tree_path(index_of_path, *tree_node_path_parts)

    def __repr__(self):
        return "{}({}: in a {})".format(
            self.__class__.__name__,
            self.real_path,
            self.parent_tree_node.__class__.__name__,
        )

    def __str__(self):
        return self.__repr__()

    def detailed_item_string(self):
        tree_paths_output = str(self.tree_node_paths)
        return "{}\n    parent container type: {}".format(
            tree_paths_output, self.parent_tree_node.__class__.__name__
        )

    def print(self):
        print(self.detailed_item_string())


def _create_default_path_names(path_count: int) -> List[str]:
    # Suppressed for doctesting.
    # noinspection PyProtectedMember
    """
    Creates default names. The number resembles the index within the list.
    The first items gets **DEFAULT_FIRST_PATH_NAME**.

    Examples:
        >>> from treepathmap.selectables import _create_default_path_names
        >>> _create_default_path_names(2)
        ['real_path', 'additional_path_1']

    Args:
        path_count(int):
            Count of path names.

    Raises:
        ValueError:
            If path_count is lower than 1.

    Returns:
        List[str]:
            Default path names.
    """
    if path_count < MINIMUM_POSSIBLE_PATH_COUNT:
        raise ValueError(
            "A path count lower than {} is not supported.".format(
                MINIMUM_POSSIBLE_PATH_COUNT
            )
        )
    default_path_names = [DEFAULT_FIRST_PATH_NAME]
    for index in range(1, path_count):
        default_path_names.append(DEFAULT_PATH_NAME_TEMPLATE.format(index))
    return default_path_names


def _check_or_create_path_names(
    existing_path_count: int, path_names: List[str] = None
) -> List[str]:
    # Suppressed for doctesting.
    # noinspection PyProtectedMember
    """

    Examples:
        >>> from treepathmap.selectables import _check_or_create_path_names
        >>> _check_or_create_path_names(2)
        ['real_path', 'additional_path_1']
        >>> _check_or_create_path_names(2, ["my_path", "another_path"])
        ['my_path', 'another_path']

    Args:
        existing_path_count(int):
            Path count of the existing *TreeNodeItems* from which a PathMap
            might be created.

        path_names(List[str]):
            Names of the paths different, which are used instead of the
            defaults.

    Raises:
        ValueError:
            If count provided *additional_path_names* is unequal to path count of the
            first item.

    Returns:
        List[str]
            Path map items.
    """
    create_defaults_due_no_path_names = path_names is None
    if create_defaults_due_no_path_names:
        return _create_default_path_names(existing_path_count)

    count_of_path_names = len(path_names)
    path_name_count_doesnt_fit = existing_path_count != count_of_path_names
    if path_name_count_doesnt_fit:
        raise ValueError(
            "Provided 'additional_path_names' suggest {} paths, but the first path item"
            "has a path count of {}.".format(count_of_path_names, existing_path_count)
        )
    return [str(path_name) for path_name in path_names]


class TreeNodeItems(Mapping):
    """
    Examples:
        >>> from treepathmap import TreeNodeItem, TreeNodePaths, TreeNodeItems
        >>> sample_container = {"a": {"b": "a value"}}
        >>> sample_items = TreeNodeItems(
        ...     TreeNodeItem(TreeNodePaths([["->a"]]), sample_container),
        ...     TreeNodeItem(TreeNodePaths([["->a->b"]]), sample_container),
        ... )
        >>> sample_items
        TreeNodeItems(->a, ->a->b)
        >>> first_path = sample_items.real_paths[0]
        >>> sample_items[first_path]
        TreeNodeItem(->a: in a dict)
        >>> inserted = sample_items.add(TreeNodeItem(TreeNodePaths([["->a->b->c"]])))
        >>> sample_items
        TreeNodeItems(->a, ->a->b, ->a->b->c)
        >>> inserted = sample_items.add_many(
        ...     [
        ...         TreeNodeItem(TreeNodePaths([["->a"]])),
        ...         TreeNodeItem(TreeNodePaths([["->d"]]))
        ...     ]
        ... )
        >>> sample_items
        TreeNodeItems(->a, ->a->b, ->a->b->c, ->d)
        >>> inserted = sample_items.add_many(
        ...     {
        ...         "not_true": TreeNodeItem(TreeNodePaths([["->a"]])),
        ...         "still_not": TreeNodeItem(TreeNodePaths([["->e"]]))
        ...     }
        ... )
        >>> sample_items.path_column_count
        1
        >>> sample_items
        TreeNodeItems(->a, ->a->b, ->a->b->c, ->d, ->e)
        >>> sample_items.real_paths
        ['->a', '->a->b', '->a->b->c', '->d', '->e']
        >>> sample_items.drop_items(["->a->b", "->a->b->c"])
        >>> sample_items
        TreeNodeItems(->a, ->d, ->e)
        >>> sample_items.real_paths
        ['->a', '->d', '->e']

        >>> sample_items_from_scratch = TreeNodeItems()
        >>> sample_items_from_scratch.add(TreeNodeItem(TreeNodePaths([["->a"]])))
        '->a'
        >>> sample_items_from_scratch.add(TreeNodeItem(TreeNodePaths([["->b"]])))
        '->b'
        >>> sample_items_from_scratch
        TreeNodeItems(->a, ->b)
        >>> sample_items_from_scratch.real_paths
        ['->a', '->b']

    """

    def __init__(self, *tree_node_items):
        self._path_column_count = 0
        self._tree_node_items = {}
        self._real_paths = []
        self.__setitem__ = self._tree_node_items.__setitem__
        self._map_any_path_map_items(tree_node_items_to_add=tree_node_items)
        self._paths_changed = False

    def __repr__(self):
        paths = ", ".join(list(self._tree_node_items))
        return "{}({})".format(self.__class__.__name__, paths)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self._tree_node_items)

    def __getitem__(self, real_path: str) -> TreeNodeItem:
        assert isinstance(
            real_path, str
        ), "The real path needs to be a str. Got {} instead.".format(type(real_path))
        return self._tree_node_items[real_path]

    def __len__(self) -> int:
        return len(self._tree_node_items)

    @property
    def path_column_count(self) -> int:
        return self._path_column_count

    def items(self) -> Generator[Dict[str, TreeNodeItem], None, None]:
        yield from self._tree_node_items.items()

    def pop(self, real_path: str) -> TreeNodeItem:
        popped_item = self._tree_node_items.pop(real_path)
        index = self._real_paths.index(real_path)
        self._real_paths.pop(index)
        return popped_item

    def drop_items(self, real_paths: Iterable[str]):
        """
        Drops the requested *real paths* from this map.

        Args:
            real_paths(Iterable[str):
                The *real paths* which will be removed.
        """
        for real_path_to_drop in real_paths:
            self._tree_node_items.pop(real_path_to_drop)
        self._update_real_paths()

    @property
    def real_paths(self):
        if self._paths_changed:
            self._update_real_paths()
        return self._real_paths

    def _map_any_path_map_items(
        self, tree_node_items_to_add: Union[Mapping, Sequence]
    ) -> List[str]:
        """

        Args:
            tree_node_items_to_add:

        Returns:
            List[str]:
                Real paths (indexes) of the added tree node items.
        """
        if isinstance(tree_node_items_to_add, Sequence):
            if len(tree_node_items_to_add) == 0:
                return
            first_item = tree_node_items_to_add[0]
            if not isinstance(first_item, TreeNodeItem):
                raise TypeError(
                    "A sequence of TreeNodeItems is expected but got a "
                    "{} of {}".format(type(tree_node_items_to_add), type(first_item))
                )
            return self._map_path_map_items_from_sequence(tree_node_items_to_add)
        elif isinstance(tree_node_items_to_add, Mapping):
            return self._map_path_map_items_from_mapping(tree_node_items_to_add)

    def _map_path_map_items_from_mapping(
        self, incoming_tree_node_items: Sequence[TreeNodeItem]
    ) -> List[str]:
        """

        Args:
            incoming_tree_node_items:

        Returns:
            List[str]:
                Real paths (indexes) of the added tree node items.
        """
        inserted_real_paths = []
        for must_not_be_valid, path_map_item in incoming_tree_node_items.items():
            freshly_added_real_path = self.add(path_map_item)
            inserted_real_paths.append(freshly_added_real_path)
        self._update_real_paths()
        return inserted_real_paths

    def _map_path_map_items_from_sequence(
        self, incoming_path_map_items: Mapping[str, TreeNodeItem]
    ) -> List[str]:
        """

        Args:
            tree_node_items_to_add:

        Returns:
            List[str]:
                Real paths (indexes) of the added tree node items.
        """
        inserted_real_paths = []
        for path_map_item in incoming_path_map_items:
            freshly_added_real_path = self.add(path_map_item)
            inserted_real_paths.append(freshly_added_real_path)
        self._update_real_paths()
        return inserted_real_paths

    def _update_real_paths(self):
        self._real_paths = list(self._tree_node_items)
        self._paths_changed = False

    def _set_column_count(self, path_column_count):
        if self._path_column_count < path_column_count:
            self._path_column_count = path_column_count

    def add(self, new_path_map_item: TreeNodeItem) -> str:
        if not isinstance(new_path_map_item, TreeNodeItem):
            raise TypeError(
                "Only types of `{}` are allowed.".format(TreeNodeItem.__name__)
            )
        freshly_added_real_path = new_path_map_item.real_path
        self._tree_node_items[freshly_added_real_path] = new_path_map_item
        self._paths_changed = True
        self._set_column_count(new_path_map_item.path_count)
        return freshly_added_real_path

    def add_many(
        self, new_path_map_items: Union[Sequence[TreeNodeItem], Mapping]
    ) -> List[str]:
        return self._map_any_path_map_items(new_path_map_items)

    def get_raw_path_map_table(self) -> List[List[str]]:
        """
        Prepares the path map items to be transformed into a *pandas.DataFrame*
        and splits *meta attributes* and *reference parent containers* as a
        dictionary.

        Examples:
            >>> from treepathmap import TreeNodeItem, TreeNodePaths, TreeNodeItems
            >>> sample_data = TreeNodeItems(
            ...     TreeNodeItem(TreeNodePaths([["a", "path"]])),
            ...     TreeNodeItem(TreeNodePaths([["another", "path"], ["additional"]]))
            ... )
            >>> sample_data.get_raw_path_map_table()
            [['->a->path', ''], ['->another->path', '->additional']]

        Args:
            self(TreeNodeItems):
                Path map items to be transformed.

        Returns:
            List[List[List]:
                The *path map* and its meta potential_tree items.
        """
        unfolded_path_map_items = []
        max_count = self.path_column_count
        for real_path, path_map_item in self.items():
            paths_of_item = [
                str(path) for path in path_map_item.tree_node_paths.tree_paths
            ]
            number_of_blank_paths_to_add = max_count - len(paths_of_item)
            if number_of_blank_paths_to_add > 0:
                paths_of_item.extend([""] * number_of_blank_paths_to_add)
            unfolded_path_map_items.append(paths_of_item)
        return unfolded_path_map_items

    def to_dataframe(self, path_names: List[str] = None) -> DataFrame:
        """

        Examples:
            >>> from treepathmap import TreeNodeItem, TreeNodePaths, TreeNodeItems
            >>> sample_items = TreeNodeItems(
            ...     TreeNodeItem(TreeNodePaths([["->a"]])),
            ...     TreeNodeItem(TreeNodePaths([["->a->b"], ["->b"]])),
            ...     TreeNodeItem(TreeNodePaths([["->a->c"], ["->c"]]))
            ... )
            ...
            >>> sample_frame = sample_items.to_dataframe(
            ...     path_names=["my_path", "alternative_path"]
            ... )
            ...
            >>> from doctestprinter import doctest_print
            >>> doctest_print(sample_frame)
                   my_path alternative_path
            ->a        ->a
            ->a->b  ->a->b              ->b
            ->a->c  ->a->c              ->c

        Args:
            self(TreeNodeItems):
                A list of all items/objects within a tree-like nested potential_tree
                structure.

            path_names(List[str]):
                Names of the paths different, which are used instead of the
                defaults.

        Raises:
            ValueError:
                If count provided *additional_path_names* is unequal to path count of the
                first item.

        Returns:
            DataFrame
        """
        actual_path_names = _check_or_create_path_names(
            self.path_column_count, path_names
        )
        raw_path_map = self.get_raw_path_map_table()
        real_path_as_index = [rows[0] for rows in raw_path_map]
        path_map_table = DataFrame(
            raw_path_map, columns=actual_path_names, index=real_path_as_index
        )
        return path_map_table

    def print_full_items(self):
        for real_path, item in self._tree_node_items.items():
            item.print()


class SelectablePaths(object):
    """
    Examples:
        >>> from treepathmap import TreeNodeItems, TreeNodePaths, TreeNodeItem
        >>> sample_items = TreeNodeItems(
        ...     TreeNodeItem(TreeNodePaths([["->a"], ["x"]])),
        ...     TreeNodeItem(TreeNodePaths([["->a->b"], [""]])),
        ...     TreeNodeItem(TreeNodePaths([["->a->b->d"], ["y"]])),
        ...     TreeNodeItem(TreeNodePaths([["->a->c"], [""]])),
        ...     TreeNodeItem(TreeNodePaths([["->a->c->e"], ["->y"]]))
        ... )
        ...
        >>> sample_paths = SelectablePaths(tree_path_table=sample_items.to_dataframe())
        >>> from doctestprinter import doctest_print
        >>> doctest_print(sample_paths)
                   real_path additional_path_1
        ->a              ->a               ->x
        ->a->b        ->a->b
        ->a->b->d  ->a->b->d               ->y
        ->a->c        ->a->c
        ->a->c->e  ->a->c->e               ->y
        >>> sample_paths.loc["->a"]
        real_path            ->a
        additional_path_1    ->x
        Name: ->a, dtype: object
        >>> doctest_print(sample_paths["additional_path_1"])
        ->a          ->x
        ->a->b
        ->a->b->d    ->y
        ->a->c
        ->a->c->e    ->y
        Name: additional_path_1, dtype: object

        Items can be selected using parts of the path, unix file name pattern or
        regular expressions.
        >>> sample_paths.select("real_path", ["*"])
        Index(['->a', '->a->b', '->a->b->d', '->a->c', '->a->c->e'], dtype='object')
        >>> sample_paths.select("real_path", ["g"])
        Index([], dtype='object')
        >>> sample_paths.select("real_path", ["a"])
        Index(['->a'], dtype='object')
        >>> sample_paths.select("real_path", ["a", "*"])
        Index(['->a->b', '->a->b->d', '->a->c', '->a->c->e'], dtype='object')
        >>> sample_paths.select("real_path", ["a", ["d", "e"]])
        Index(['->a->b->d', '->a->c->e'], dtype='object')
        >>> sample_paths.select("real_path", [["b", "c"], "*"])
        Index(['->a->b->d', '->a->c->e'], dtype='object')

        Other path definitions works as different views on the nested containers
        in the background.

        >>> sample_paths.select("additional_path_1", ["*"])
        Index(['->a', '->a->b->d', '->a->c->e'], dtype='object')
        >>> sample_paths.select("additional_path_1", ["x"])
        Index(['->a'], dtype='object')
        >>> sample_paths.select("additional_path_1", ["y"])
        Index(['->a->b->d', '->a->c->e'], dtype='object')
        >>> sample_paths.select("additional_path_1", ["z"])
        Index([], dtype='object')

    """

    def __init__(self, tree_path_table: DataFrame):
        self._tree_path_table: DataFrame = tree_path_table

    def __str__(self):
        return str(self._tree_path_table)

    def __getitem__(self, columns):
        return self._tree_path_table[columns]

    def drop(self, *args, **kwargs):
        self._tree_path_table.drop(*args, **kwargs)

    def insert_tree_path_table_section_at(
        self, table_section_to_insert: DataFrame, insertion_position: int
    ):
        just_needs_to_be_added = insertion_position >= len(self._tree_path_table)

        existing_columns = self._tree_path_table.columns
        missing_columns = existing_columns.difference(table_section_to_insert.columns)
        table_section_to_insert = add_columns_to_dataframe(
            table_section_to_insert, missing_columns, ""
        )

        if just_needs_to_be_added:
            parts_to_be_concatenated = [self._tree_path_table, table_section_to_insert]
        else:
            table_head = self._tree_path_table[:insertion_position]
            table_tail = self._tree_path_table[insertion_position:]
            parts_to_be_concatenated = [table_head, table_section_to_insert, table_tail]
        new_tree_path_table = pandas.concat(parts_to_be_concatenated)
        self._tree_path_table = new_tree_path_table

    @property
    def empty(self):
        return self._tree_path_table.empty

    @property
    def index(self) -> pandas.Index:
        return self._tree_path_table.index

    @property
    def loc(self):
        return self._tree_path_table.loc

    @property
    def columns(self):
        return self._tree_path_table.columns

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

            *search_parts:
                Tree path parts which are parts of the requested tree items
                paths.

        Returns:
            PathMapSelection:
                Selection of augmented tree items.
        """
        if not isinstance(search_parts, (list, tuple)):
            raise TypeError("search_parts must be a list or tuple.")
        if selection_path_name is None:
            raise ValueError("target_column_name cannot be None.")
        if selection_path_name not in self._tree_path_table.columns:
            available_columns = "', '".join(self._tree_path_table.columns)
            raise KeyError(
                "{} not found in available paths "
                "'{}'.".format(selection_path_name, available_columns)
            )
        fitting_search_parts = turn_iterables_to_unixfilepatterns(search_parts)
        selection_query = create_selection_pattern(*fitting_search_parts)
        requested_paths = self._tree_path_table[selection_path_name]
        selected_indexes = select_indexes_from_series(
            series=requested_paths,
            selection_pattern=selection_query,
            pre_selection_indexes=pre_selection_indexes,
        )
        return selected_indexes

    def copy_dataframe(self) -> DataFrame:
        return self._tree_path_table.copy()


def get_indexes_where_these_parts_apply(
    where_searchables: Series, search_parts: Iterable[str]
) -> pandas.Index:
    """
    Examples:
        >>> from treepathmap.selectables import get_indexes_where_these_parts_apply
        >>> from treepathmap import convert_to_where_searchable_parts
        >>> from pandas import Series
        >>> sample_series = Series(
        ...     ["/k1/1/", "/k1/2/", "/k1/2/k2/2/", "/k1/1/k2/4/"],
        ...     name="meta_attributes",
        ...     index=["->a", "->a->b", "->a->b->c", "->a->b->d"]
        ... )
        >>> search_pattern = convert_to_where_searchable_parts("2", "k2/2")
        >>> get_indexes_where_these_parts_apply(sample_series, search_pattern)
        Index(['->a->b->c'], dtype='object')
        >>> search_pattern = convert_to_where_searchable_parts("3")
        >>> get_indexes_where_these_parts_apply(sample_series, search_pattern)
        Index([], dtype='object')

    Args:
        where_searchables():
        search_parts:

    Returns:
        pandas.Index
    """
    if not isinstance(search_parts, Iterable) and isinstance(search_parts, str):
        raise TypeError(
            "search_parts must be an Iterable of strings. "
            "Got '{}' instead.".format(type(search_parts))
        )
    selected_attributes = where_searchables.copy()
    for where_searchable_search_part in search_parts:
        if selected_attributes.empty:
            return selected_attributes.index.copy()
        selected_attributes = select_sub_series_from_series(
            combined_attributes=selected_attributes,
            selection_pattern=where_searchable_search_part,
        )
    return selected_attributes.index.copy()


MetaAttributes = Dict[str, Union[int, str]]
RealPath = str
MetaItems = Dict[RealPath, MetaAttributes]


class ContainsMetaAttributes(ABC):
    @property
    @abstractmethod
    def meta_attributes(self) -> Dict[str, Union[int, str]]:
        pass

    @property
    @abstractmethod
    def real_path(self) -> str:
        pass


def convert_meta_items_to_dataframe(meta_items: MetaItems, column_name: str) -> Series:
    """
    Examples:
        >>> from collections import namedtuple
        >>> sample_meta_items = {
        ...     "->a": {"k1": 1},
        ...     "->a->b": {"k1": 2},
        ...     "->a->b->c": {"k2": 2, "k1": 2},
        ... }
        >>> convert_meta_items_to_dataframe(
        ...     meta_items=sample_meta_items, column_name="sample"
        ... )
        ->a                //k1/1//
        ->a->b             //k1/2//
        ->a->b->c    //k1/2//k2/2//
        Name: sample, dtype: object

    Args:
        meta_items:
        column_name:

    Returns:

    """
    real_paths = []
    meta_item_path_likes = []
    for real_path, meta_attributes in meta_items.items():
        real_paths.append(real_path)
        item_path_like = convert_metaattributes_to_pathlike(meta_attributes)
        meta_item_path_likes.append(item_path_like)

    return Series(meta_item_path_likes, name=column_name, index=real_paths)


class WhereSelectable(ABC):
    @property
    @abstractmethod
    def where_searchables(self) -> Series:
        """
        A *Series* of prepared strings from which the *where* selection is
        performed using regular expressions.

        Returns:
            Series
        """

    def where(
        self,
        *search_parts,
        pre_selection_indexes: Optional[pandas.Index] = None,
    ) -> pandas.Index:
        """

        Args:
            search_parts(Iterable[str]):
                The selection patterns for which indexes are retrieved.

            pre_selection_indexes(Optional[pandas.Index]):
                Sets the preliminary selection of items, from which the
                selection by the *search parts* is done.

        Returns:
            pandas.Index
        """
        if pre_selection_indexes is not None:
            existing_indexes = self.where_searchables.index
            possible_indexes_mask = existing_indexes.isin(pre_selection_indexes)
            select_from_these_items = self.where_searchables.loc[possible_indexes_mask]
            nothing_remained_then_leave_early = select_from_these_items.empty
            if nothing_remained_then_leave_early:
                return select_from_these_items.index.copy()
            requested_indexes = get_indexes_where(
                where_searchables=select_from_these_items, raw_search_parts=search_parts
            )
        else:
            requested_indexes = get_indexes_where(
                where_searchables=self.where_searchables, raw_search_parts=search_parts
            )
        return requested_indexes

    def __call__(
        self,
        *search_parts,
        pre_selection_indexes: Optional[pandas.Index] = None,
    ) -> pandas.Index:
        return get_indexes_where(
            self.where_searchables,
            search_parts,
            pre_selection_indexes=pre_selection_indexes,
        )

    def get_subsection(self, indexes: pandas.Index) -> "WhereSelectable":
        """
        Creates an instance containing the requested *indexes* only.

        Args:
            indexes:
                Indexes the subsection should contain.

        Returns:
            WhereSelectable
        """
        pass

    def get_series(self, target_indexes: Union[List, pandas.Index]) -> pandas.Series:
        """
        Returns a series containing the requested indexes. Only returned existing
        indexes.

        Args:
            target_indexes:
                The indexes for which items should be returned.

        Returns:
            pandas.Series

        """
        return get_intersection(
            source=self.where_searchables, targeted_indexes=target_indexes
        )


def get_preselected_series(
    full_series: Series, pre_selection_indexes: Optional[pandas.Index] = None
) -> pandas.Series:
    """
    Examples:
        >>> from treepathmap.selectables import get_preselected_series
        >>> from pandas import Series
        >>> sample_series = Series(list(range(3)), index=list(iter("abc")))
        >>> get_preselected_series(sample_series, ["b", "c", "d"])
        b    1
        c    2
        dtype: int64
        >>> get_preselected_series(sample_series)
        a    0
        b    1
        c    2
        dtype: int64

    Args:
        full_series:
        pre_selection_indexes:

    Returns:

    """
    assert pre_selection_indexes is None or isinstance(
        pre_selection_indexes, Iterable
    ), "pre_selection_indexes needs to be an Iterable or None."
    if pre_selection_indexes is not None:
        return get_intersection(
            source=full_series, targeted_indexes=pre_selection_indexes
        )
    return full_series


def get_indexes_where(
    where_searchables: Series,
    raw_search_parts: Iterable[str],
    pre_selection_indexes: Optional[pandas.Index] = None,
) -> pandas.Index:
    """

    Args:
        *raw_search_parts:

    Returns:
        pandas.Index
    """
    fitting_search_parts = turn_iterables_to_unixfilepatterns(raw_search_parts)
    where_search_patterns = convert_to_where_searchable_parts(*fitting_search_parts)

    pre_selected_where_searchables = get_preselected_series(
        full_series=where_searchables, pre_selection_indexes=pre_selection_indexes
    )
    selected_indexes = get_indexes_where_these_parts_apply(
        where_searchables=pre_selected_where_searchables,
        search_parts=where_search_patterns,
    )

    return selected_indexes


class IrregularTags(WhereSelectable):
    """
    *IrregularTags* defines tree node items tagged irregulary with key-value
    attributes.

    Notes:
        In this context the term irregularry means that in worst case every
        entry could have an unique key. Containing N items this would lead
        to a N x N Table with (N² - N) empty values. Therefore this group
        stores the tags/meta attributes in a Mapping.

    Examples:
        >>> from treepathmap.selectables import IrregularTags
        >>> from treepathmap import wh_is
        >>> sample_meta_items = {
        ...     "->a": {"k1": 1},
        ...     "->a->b": {"k1": 2},
        ...     "->a->b->c": {"k2": 1, "k1": 2},
        ...     "->a->b->d": {"k2": 2, "k1": 1},
        ... }
        >>> sample_group = IrregularTags(
        ...     name="meta_attributes", meta_items=sample_meta_items
        ... )
        >>> sample_group
        ->a                //k1/1//
        ->a->b             //k1/2//
        ->a->b->c    //k1/2//k2/1//
        ->a->b->d    //k1/1//k2/2//
        Name: meta_attributes, dtype: object
        >>> sample_group.where(1)
        Index(['->a', '->a->b->c', '->a->b->d'], dtype='object')
        >>> sample_group.where("1")
        Index(['->a', '->a->b->c', '->a->b->d'], dtype='object')
        >>> sample_group.where(wh_is("k2", 1))
        Index(['->a->b->c'], dtype='object')
        >>> sample_group.where(wh_is(1, "k2"))
        Index([], dtype='object')
        >>> sample_group.where(1, "k2")
        Index(['->a->b->c', '->a->b->d'], dtype='object')

        >>> sample_group.where("k1/1", pre_selection_indexes=["->a->b", "->a->b->c"])
        Index([], dtype='object')

        >>> sample_group.get_subsection(["->a", "->a->b->c"])
        ->a                //k1/1//
        ->a->b->c    //k1/2//k2/1//
        Name: meta_attributes, dtype: object

    """

    def __init__(
        self,
        name: str,
        meta_items: Optional[MetaItems] = None,
        where_searchables: Optional[Series] = None,
    ):
        self._name = name
        self.meta_items: Series = Series(meta_items)
        if where_searchables is not None:
            equal_length = len(where_searchables) == len(meta_items)
            assert (
                equal_length
            ), "Given where_searchables and meta_items do not have an equal length."
            self._where_searchables = where_searchables
        elif meta_items is not None:
            self._where_searchables: Series = convert_meta_items_to_dataframe(
                meta_items=meta_items, column_name=name
            )
        else:
            self._where_searchables: Series = Series()

    @property
    def name(self):
        return self._name

    def get_subsection(self, indexes: pandas.Index) -> "IrregularTags":
        mask_of_requested_indexes = self._where_searchables.index.isin(indexes)
        requested_indexes = self._where_searchables.index[mask_of_requested_indexes]
        return IrregularTags(
            name=self.name,
            meta_items=self.meta_items.loc[requested_indexes],
            where_searchables=self._where_searchables.loc[requested_indexes],
        )

    @property
    def where_searchables(self) -> Series:
        return self._where_searchables

    def __repr__(self):
        return str(self._where_searchables)

    def add_meta_items(self, meta_items: MetaItems):
        new_overriding_items = convert_meta_items_to_dataframe(
            meta_items=meta_items, column_name=self.name
        )
        self._where_searchables = override_left_with_right_series(
            left_target=self._where_searchables,
            overriding_right=new_overriding_items,
        )


class RelatedGroupTags(WhereSelectable):
    """
    *RelatedGroupTags* defines tree node items tagged by a group of key-value
    attributes, which should support grouping of tree node items.

    Notes:
        The *related group* term states the existance of more than 1 unique
        set of attributes. All tagged items share the same attribute names
        (keys) leading to an N-item x M-attribute table.

    Examples:
        >>> from treepathmap import wh_is
        >>> from treepathmap.selectables import RelatedGroupTags
        >>> sample_tags = RelatedGroupTags("foo")
        >>> sample_tags.tag(["->a", "->b", "->c"], {"foo": 1, "bar": "a"})
        >>> sample_tags
            bar foo               foo
        ->a   a   1  //bar/a//foo/1//
        ->b   a   1  //bar/a//foo/1//
        ->c   a   1  //bar/a//foo/1//
        >>> sample_tags.tag(["->c", "->d"], {"foo": 3, "bar": "b"})
        >>> sample_tags
            bar foo               foo
        ->a   a   1  //bar/a//foo/1//
        ->b   a   1  //bar/a//foo/1//
        ->c   b   3  //bar/b//foo/3//
        ->d   b   3  //bar/b//foo/3//
        >>> sample_tags.tag(["->d", "->e"], {"foo": 5, "x": "c"})
        >>> sample_tags
             bar foo    x                    foo
        ->a    a   1  NaN   //bar/a//foo/1//x///
        ->b    a   1  NaN   //bar/a//foo/1//x///
        ->c    b   3  NaN   //bar/b//foo/3//x///
        ->d    b   5    c  //bar/b//foo/5//x/c//
        ->e  NaN   5    c   //bar///foo/5//x/c//

        >>> sample_tags.where(wh_is("bar", "b"), wh_is("foo", "5"))
        Index(['->d'], dtype='object')
        >>> sample_tags.where(wh_is("x", ""))
        Index(['->a', '->b', '->c'], dtype='object')

        >>> sample_tags.where("x/c", pre_selection_indexes=["->a", "->b", "->c"])
        Index([], dtype='object')

        >>> sample_tags.get_subsection(["->a", "->d"])
            bar foo    x                    foo
        ->a   a   1  NaN   //bar/a//foo/1//x///
        ->d   b   5    c  //bar/b//foo/5//x/c//
    """

    WHERE_COLUMN = "where"
    """
    Examples:
        pass

    """

    def __init__(
        self,
        name: Optional[str] = None,
        tags: Optional[DataFrame] = None,
        where_searchables: Optional[Series] = None,
    ):
        if name is None:
            self._name = RelatedGroupTags.WHERE_COLUMN
        else:
            self._name = name
        assert tags is None or isinstance(
            tags, DataFrame
        ), "tags must be a pandas.DataFrame."
        assert where_searchables is None or isinstance(
            where_searchables, Series
        ), "where_searchables must be a pandas.Series."
        if tags is None:
            self._tags: DataFrame = DataFrame()
        else:
            self._tags: DataFrame = tags

        if where_searchables is not None:
            self._where_searchables: Series = where_searchables
            equal_length = len(where_searchables) == len(tags)
            assert (
                equal_length
            ), "Given where_searchables and meta_items do not have an equal length."
        elif tags is not None:
            self._new_column_was_tagged = True
            self._update_indexes()
        else:
            self._where_searchables = Series(name=name, dtype=str)
        self._new_column_was_tagged: bool = False

    @property
    def name(self):
        return self._name

    @property
    def where_searchables(self) -> Series:
        return self._where_searchables

    @property
    def not_initialized(self) -> bool:
        return self._tags is None

    def get_subsection(self, indexes: pandas.Index) -> "RelatedGroupTags":
        mask_of_requested_indexes = self._where_searchables.index.isin(indexes)
        requested_indexes = self._where_searchables.index[mask_of_requested_indexes]
        return RelatedGroupTags(
            name=self._name,
            tags=self._tags.loc[requested_indexes],
            where_searchables=self._where_searchables.loc[requested_indexes],
        )

    def tag(
        self,
        indexes: pandas.Index,
        values_to_tag: Dict[str, Union[int, str]],
    ):
        """

        Args:
            indexes:
            values_to_tag:

        Returns:

        """
        item_count = len(indexes)
        tag_row_values = list(values_to_tag.values())
        tag_column_names = pandas.Index(values_to_tag)
        column_count = len(tag_column_names)
        values_to_tag = numpy.full(
            (item_count, column_count), tag_row_values, dtype=numpy.object
        )
        freshly_tagged = DataFrame(
            data=values_to_tag, index=indexes, columns=tag_column_names
        )

        non_existing_columns = tag_column_names.difference(self._tags.columns)
        a_new_column_will_be_added = not non_existing_columns.empty
        self._tags = override_left_with_right_dataframe(self._tags, freshly_tagged)
        if a_new_column_will_be_added:
            self._new_column_was_tagged = True

        changed_indexes = freshly_tagged.index
        self._where_searchables = add_missing_indexes_to_series(
            target_series=self._where_searchables, new_indexes=changed_indexes
        )
        self._update_indexes(changed_indexes=changed_indexes)

    def _allocate_new_column(self, column_name: str, dtype):
        self._tags[column_name] = numpy.NaN
        self._tags[column_name] = self._tags[column_name].astype(dtype=dtype)

    @staticmethod
    def convert_tags_to_where_searchables(row: Series) -> str:
        """
        Examples:
            >>> from pandas import DataFrame
            >>> import numpy as np
            >>> from treepathmap.selectables import RelatedGroupTags
            >>> sample_frame = DataFrame(
            ...     np.arange(4).reshape(2, 2), columns=["x", "y"]
            ... )
            >>> enable_where = RelatedGroupTags.convert_tags_to_where_searchables
            >>> result = sample_frame.apply(func=enable_where, axis=1)
            >>> result
            0    //x/0//y/1//
            1    //x/2//y/3//
            dtype: object

        Args:
            row:

        Returns:
            str
        """
        return convert_metaattributes_to_pathlike(meta_attributes=row)

    def _update_indexes(self, changed_indexes: Optional[pandas.Index] = None):
        if self._new_column_was_tagged or changed_indexes is None:
            self._where_searchables = self._tags.apply(
                func=RelatedGroupTags.convert_tags_to_where_searchables, axis=1
            )
            self._new_column_was_tagged = False
        else:
            changed_items: DataFrame = self._tags.loc[changed_indexes]
            updated_items = changed_items.apply(
                func=RelatedGroupTags.convert_tags_to_where_searchables, axis=1
            )
            self._where_searchables.loc[changed_indexes] = updated_items
        self._where_searchables.name = self._name

    def __repr__(self):
        return str(pandas.concat([self._tags, self.where_searchables], axis=1))

    def __str__(self):
        return str(self._tags)