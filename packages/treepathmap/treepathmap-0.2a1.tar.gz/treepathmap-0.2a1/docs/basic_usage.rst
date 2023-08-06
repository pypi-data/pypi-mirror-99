***********
Basic Usage
***********

.. contents::
    :local:

Important
=========

.. note::
   The path delimiters within the :class:`treepathmap.PathMap` are defined
   as an arrow '->'. This is intentional as the paths should not be mistaken
   for system file paths.

Examples
========

A simple nested collection of Sequences and Mappings will be used for the
following examples. Within this example two features of **treepathmap** will
be shown. The **additional paths** which are like a different view onto the
mapped nested collection and **meta attributes**, which provide the possibility
to tag tree nodes for later selection purposes.

The **meta attributes** are a feature of :class:`treepathmap.TreeNodeItems`.
Child *tree node items* inherit *meta attributes* from their parents.


.. doctest::

    >>> from treepathmap import map_tree, wh_is
    >>> sample_tree = {
    ...     "table": {
    ...         "hint": "eat now",
    ...         "basket": [
    ...             {"fruit": "apple", "color": "red"},
    ...             {"fruit": "apple", "color": "green"},
    ...             {"fruit": "banana", "color": "yellow"},
    ...         ],
    ...     },
    ...     "shelf": [
    ...         {"fruit": "apple", "color": "red"},
    ...         {"fruit": "banana", "color": "yellow"},
    ...         {"fruit": "banana", "color": "brown"},
    ...     ],
    ... }

Mapping of a tree
-----------------

Either provide a completely defined :class:`treepathmap.TreeNodeItems` or use
the default mapping method and customize the received *tree node items* of type
:class:`treepathmap.TreeNodeItem` by an own method. In this example the items
'color' and 'hint' will be used as meta attributes of the item and an additional
path will list the current items by fruit types.

.. hint::
   Meta attributes don't need to origin from the collection.

.. doctest::

    >>> counters = {}
    >>> from pandas import Series
    >>> META_ATTRIBUTE_KEYS = ["color", "hint"]
    >>> def get_meta_attributes(potential_collection):
    ...     if not isinstance(potential_collection, dict):
    ...         return None
    ...     return {
    ...         key: potential_collection[key]
    ...         for key in META_ATTRIBUTE_KEYS
    ...         if key in potential_collection
    ...     }
    ...
    >>> def add_path_and_meta_attributes(a_tree_node_item):
    ...     global META_ATTRIBUTE_KEYS
    ...     # Add meta attributes if exist
    ...     original_item = a_tree_node_item.prime_value
    ...     meta_attributes = get_meta_attributes(original_item)
    ...     if meta_attributes is not None and meta_attributes:
    ...         a_tree_node_item.add_meta_attributes(meta_attributes)
    ...     if not isinstance(original_item, dict):
    ...         return a_tree_node_item
    ...     # Add a different view
    ...     if "fruit" not in original_item:
    ...         return a_tree_node_item
    ...     fruit = original_item["fruit"]
    ...     global counters
    ...     if fruit not in counters:
    ...         counters[fruit] = 0
    ...
    ...     first_additional_path = 1
    ...     path_parts = (fruit+"s", counters[fruit])
    ...     a_tree_node_item.set_tree_path(first_additional_path, *path_parts)
    ...     counters[fruit] += 1
    ...     return a_tree_node_item
    ...

After the tree (nested collections) is mapped lets take a look on all tree nodes
(and leaves) within a table.

.. note::
    The direct representation of the *path map* is more detailed, than the
    str() representation invoked by print(), which resembles a table.

.. doctest::

    >>> mapped_tree = map_tree(
    ...     sample_tree, modify_default_path_map_item=add_path_and_meta_attributes
    ... )
    >>> print(mapped_tree)
                              additional_path_1                 meta_attributes
    ->table                                                    //hint/eat now//
    ->table->hint                                              //hint/eat now//
    ->table->basket                                            //hint/eat now//
    ->table->basket->0              ->apples->0     //color/red//hint/eat now//
    ->table->basket->0->fruit                       //color/red//hint/eat now//
    ->table->basket->0->color                       //color/red//hint/eat now//
    ->table->basket->1              ->apples->1   //color/green//hint/eat now//
    ->table->basket->1->fruit                     //color/green//hint/eat now//
    ->table->basket->1->color                     //color/green//hint/eat now//
    ->table->basket->2             ->bananas->0  //color/yellow//hint/eat now//
    ->table->basket->2->fruit                    //color/yellow//hint/eat now//
    ->table->basket->2->color                    //color/yellow//hint/eat now//
    ->shelf                                                                ////
    ->shelf->0                      ->apples->2                   //color/red//
    ->shelf->0->fruit                                             //color/red//
    ->shelf->0->color                                             //color/red//
    ->shelf->1                     ->bananas->1                //color/yellow//
    ->shelf->1->fruit                                          //color/yellow//
    ->shelf->1->color                                          //color/yellow//
    ->shelf->2                     ->bananas->2                 //color/brown//
    ->shelf->2->fruit                                           //color/brown//
    ->shelf->2->color                                           //color/brown//

Different views
---------------

The added *additional path* can be used to specify a different view on the
collection than it is originally structured.

.. doctest::

    >>> other_view_map = mapped_tree["additional_path_1"]
    >>> print(other_view_map)
                       additional_path_1                 meta_attributes
    ->table->basket->0       ->apples->0     //color/red//hint/eat now//
    ->table->basket->1       ->apples->1   //color/green//hint/eat now//
    ->table->basket->2      ->bananas->0  //color/yellow//hint/eat now//
    ->shelf->0               ->apples->2                   //color/red//
    ->shelf->1              ->bananas->1                //color/yellow//
    ->shelf->2              ->bananas->2                 //color/brown//

Selection of items
------------------

From any map selections can be done by either searching for parts of paths
using unix file pattern.

.. doctest::

    >>> apple_map = other_view_map.select("apples", "*")
    >>> print(apple_map)
                       additional_path_1                meta_attributes
    ->table->basket->0       ->apples->0    //color/red//hint/eat now//
    ->table->basket->1       ->apples->1  //color/green//hint/eat now//
    ->shelf->0               ->apples->2                  //color/red//

.. doctest::

    >>> apple_map = other_view_map.select("apples", "[02]")
    >>> print(apple_map)
                       additional_path_1              meta_attributes
    ->table->basket->0       ->apples->0  //color/red//hint/eat now//
    ->shelf->0               ->apples->2                //color/red//

The `meta` attribute of the path map leads to the selection via the
*meta attributes*, which is invoked by the `where` method.

.. note::
   The helper method `wh_is` (where is) combines both items to the correct
   search pattern for a where <key> is <value> statement.

.. doctest::

    >>> yellow_fruits = mapped_tree.meta.where(wh_is("color", "yellow"))
    >>> print(yellow_fruits)
                              additional_path_1                 meta_attributes
    ->table->basket->2             ->bananas->0  //color/yellow//hint/eat now//
    ->table->basket->2->fruit                    //color/yellow//hint/eat now//
    ->table->basket->2->color                    //color/yellow//hint/eat now//
    ->shelf->1                     ->bananas->1                //color/yellow//
    ->shelf->1->fruit                                          //color/yellow//
    ->shelf->1->color                                          //color/yellow//

Since the prior view shows every tree node/leaf related to the *where* selection
the *additional path* view can reduce the selection additionally, making it
more human readable.

.. doctest::

    >>> yellow_fruits = mapped_tree[1].meta.where(wh_is("color", "yellow"))
    >>> print(yellow_fruits)
                       additional_path_1                 meta_attributes
    ->table->basket->2      ->bananas->0  //color/yellow//hint/eat now//
    ->shelf->1              ->bananas->1                //color/yellow//


The `where` method used at the *path map level* requests arguments by groups of
two which are *path part*-*value* pairs. It searches for path with the path
part and selects them, if the have an equal value.

.. doctest::

    >>> apples = mapped_tree.where("fruit", "apple")
    >>> print(apples)
                              additional_path_1                meta_attributes
    ->table->basket->0->fruit                      //color/red//hint/eat now//
    ->table->basket->1->fruit                    //color/green//hint/eat now//
    ->shelf->0->fruit                                            //color/red//

While the `where` method of *tags* (e.g. meta attributes) also allows single
statements. In the current version `select` is reserved for selection of *tree
node paths* in which the order of the arguments is taken into account. `where`
selections doesn't need to provide any order or rather the order is ignored.

.. doctest::

    >>> red_apples = apples.meta.where("red")
    >>> print(red_apples)
                              additional_path_1              meta_attributes
    ->table->basket->0->fruit                    //color/red//hint/eat now//
    ->shelf->0->fruit                                          //color/red//


Tagging
=======

.. doctest::

    >>> fruits = mapped_tree["additional_path_1"]
    >>> fruits.tags["tag_group"].tag({"foo": 1, "bar": "a"})
    >>> print(fruits)
                       additional_path_1  ...         tag_group
    ->table->basket->0       ->apples->0  ...  //bar/a//foo/1//
    ->table->basket->1       ->apples->1  ...  //bar/a//foo/1//
    ->table->basket->2      ->bananas->0  ...  //bar/a//foo/1//
    ->shelf->0               ->apples->2  ...  //bar/a//foo/1//
    ->shelf->1              ->bananas->1  ...  //bar/a//foo/1//
    ->shelf->2              ->bananas->2  ...  //bar/a//foo/1//
    <BLANKLINE>
    [6 rows x 3 columns]


Limitations
===========

.. doctest::

    >>> map_tree("Something not being a collection of Sequence or Mapping.")
    Traceback (most recent call last):
    TypeError: Expected a Sequence or Mapping, got '<class 'str'>' instead.

    >>> map_tree({})
    Traceback (most recent call last):
        MINIMUM_POSSIBLE_PATH_COUNT
    ValueError: A path count lower than 1 is not supported.

    >>> map_tree({"one": "item"})
    ->one

In the current scope **treepathmap** does not features tracking of added tree nodes
to the origin collection. It's main purpose is to get selections and relations of
many nested entries.

In this example a smaller tree will be used.

.. doctest::

    >>> smaller_sample_tree = {
    ...     "shelf": [
    ...         {"fruit": "apple", "color": "red"},
    ...         {"fruit": "banana", "color": "yellow"},
    ...         {"fruit": "banana", "color": "brown"},
    ...     ],
    ... }
    >>> smaller_sample_map = map_tree(
    ...     smaller_sample_tree,
    ...     modify_default_path_map_item=add_path_and_meta_attributes
    ... )
    >>> fruits = smaller_sample_map[1]
    >>> print(fruits)
               additional_path_1   meta_attributes
    ->shelf->0       ->apples->3     //color/red//
    ->shelf->1      ->bananas->3  //color/yellow//
    ->shelf->2      ->bananas->4   //color/brown//

By using the *tree_items* attribute of :class:`treepathmap.PathMap` you get
access to the origin collections. Any changed here are reflected within the
origin, but not in the PathMap.

.. doctest::

    >>> yellow_fruits = smaller_sample_map[1].meta.where("color/yellow")
    >>> print(yellow_fruits)
               additional_path_1   meta_attributes
    ->shelf->1      ->bananas->3  //color/yellow//
    >>> for fruit in yellow_fruits.tree_items:
    ...     fruit["eatable"] = True
    >>> from doctestprinter import doctest_print
    >>> doctest_print(smaller_sample_tree, max_line_width=70)
    {'shelf': [{'fruit': 'apple', 'color': 'red'}, {'fruit': 'banana', 'color':
    'yellow', 'eatable': True}, {'fruit': 'banana', 'color': 'brown'}]}
    >>> print(yellow_fruits)
               additional_path_1   meta_attributes
    ->shelf->1      ->bananas->3  //color/yellow//

.. doctest::

    >>> fruits.tree_items[1:] = {"fruit": "banana", "color": "green", "eatable": False}
    >>> fruits_reselected = fruits[1]
    >>> print(fruits_reselected)
               additional_path_1   meta_attributes
    ->shelf->0       ->apples->3     //color/red//
    ->shelf->1      ->bananas->3  //color/yellow//
    ->shelf->2      ->bananas->4   //color/brown//

.. doctest::

    >>> doctest_print(smaller_sample_tree, max_line_width=70)
    {'shelf': [{'fruit': 'apple', 'color': 'red'}, {'fruit': 'banana', 'color':
    'green', 'eatable': False}, {'fruit': 'banana', 'color': 'green', 'eatable':
    False}]}

Remapping is necessary if the origin changed severly.

.. doctest::

    >>> smaller_sample_map = map_tree(
    ...     smaller_sample_tree,
    ...     modify_default_path_map_item=add_path_and_meta_attributes
    ... )
    >>> print(smaller_sample_map)
                        additional_path_1  meta_attributes
    ->shelf                                           ////
    ->shelf->0                ->apples->4    //color/red//
    ->shelf->0->fruit                        //color/red//
    ->shelf->0->color                        //color/red//
    ->shelf->1               ->bananas->5  //color/green//
    ->shelf->1->fruit                      //color/green//
    ->shelf->1->color                      //color/green//
    ->shelf->1->eatable                    //color/green//
    ->shelf->2               ->bananas->6  //color/green//
    ->shelf->2->fruit                      //color/green//
    ->shelf->2->color                      //color/green//
    ->shelf->2->eatable                    //color/green//