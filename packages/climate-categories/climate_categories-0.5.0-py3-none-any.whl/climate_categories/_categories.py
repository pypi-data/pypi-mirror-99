"""Classes to represent and query categorical systems."""

import datetime
import pathlib
import pickle
import typing

import natsort
import networkx as nx
import pandas
import strictyaml as sy
from ruamel.yaml import YAML


class Category:
    """A single category."""

    _strictyaml_schema = sy.Map(
        {
            "title": sy.Str(),
            sy.Optional("comment"): sy.Str(),
            sy.Optional("alternative_codes"): sy.Seq(sy.Str()),
            sy.Optional("info"): sy.MapPattern(sy.Str(), sy.Any()),
        }
    )

    def __init__(
        self,
        codes: typing.Tuple[str],
        categorization: "Categorization",
        title: str,
        comment: typing.Optional[str] = None,
        info: typing.Optional[dict] = None,
    ):
        self.codes = codes
        self.title = title
        self.comment = comment
        self.categorization = categorization
        if info is None:
            self.info = {}
        else:
            self.info = info

    @classmethod
    def from_spec(cls, code: str, spec: typing.Dict, categorization: "Categorization"):
        codes = [code]
        if "alternative_codes" in spec:
            codes += spec["alternative_codes"]
            del spec["alternative_codes"]
        return cls(
            codes=tuple(codes),
            categorization=categorization,
            title=spec["title"],
            comment=spec.get("comment", None),
            info=spec.get("info", None),
        )

    def to_spec(self) -> (str, typing.Dict[str, typing.Union[str, dict, list]]):
        """Turn this category into a specification ready to be written to a yaml file.

        Returns
        -------
        (code: str, spec: dict)
            Primary code and specification dict
        """
        code = self.codes[0]
        spec = {"title": self.title}
        if self.comment is not None:
            spec["comment"] = self.comment
        if len(self.codes) > 1:
            spec["alternative_codes"] = list(self.codes[1:])
        if self.info:
            spec["info"] = self.info
        return code, spec

    def __str__(self) -> str:
        return f"{self.codes[0]} {self.title}"

    def __eq__(self, other: "Category"):
        if not isinstance(other, Category):
            return False
        return any((x in other.codes for x in self.codes)) and (
            self.categorization is other.categorization
            or self.categorization.name.startswith(f"{other.categorization.name}_")
            or other.categorization.name.startswith(f"{self.categorization.name}_")
            or self.categorization.name == other.categorization.name
        )

    def __repr__(self) -> str:
        return f"<{self.categorization.name}: {self.codes[0]!r}>"

    def __hash__(self):
        return hash(self.categorization.name + self.codes[0])

    def __lt__(self, other):
        s = natsort.natsorted((self.codes[0], other.codes[0]))
        if s[0] == self.codes[0] and not self == other:
            return True
        else:
            return False


class HierarchicalCategory(Category):
    """A single category from a HierarchicalCategorization."""

    _strictyaml_schema = sy.Map(
        {
            "title": sy.Str(),
            sy.Optional("comment"): sy.Str(),
            sy.Optional("alternative_codes"): sy.Seq(sy.Str()),
            sy.Optional("info"): sy.MapPattern(sy.Str(), sy.Any()),
            sy.Optional("children"): sy.Seq(sy.Seq(sy.Str())),
        }
    )

    def __init__(
        self,
        codes: typing.Tuple[str],
        categorization: "HierarchicalCategorization",
        title: str,
        comment: typing.Optional[str] = None,
        info: typing.Optional[dict] = None,
    ):
        Category.__init__(self, codes, categorization, title, comment, info)
        self.categorization = categorization

    def to_spec(self) -> (str, typing.Dict[str, typing.Union[str, dict, list]]):
        """Turn this category into a specification ready to be written to a yaml file.

        Returns
        -------
        (code: str, spec: dict)
            Primary code and specification dict
        """
        code, spec = Category.to_spec(self)
        children = []
        for child_set in self.children:
            children.append(list(sorted((c.codes[0] for c in child_set))))
        if children:
            spec["children"] = children
        return code, spec

    @property
    def children(self) -> typing.List[typing.Set["HierarchicalCategory"]]:
        """The sets of subcategories comprising this category.

        The first set is canonical, the other sets are alternative.
        Only the canonical sets are used to calculate the level of a category."""
        return self.categorization.children(self)

    @property
    def parents(self) -> typing.Set["HierarchicalCategory"]:
        """The super-categories where this category is a member of any set of children.

        Note that all possible parents are returned, not "canonical" parents.
        """
        return self.categorization.parents(self)

    @property
    def level(self) -> int:
        """The level of the category.

        The canonical top-level category has level 1 and its children have level 2 etc.

        To calculate the level, only the first ("canonical") set of children is
        considered for intermediate categories.
        """
        return self.categorization.level(self)


class Categorization:
    """A single categorization system.

    A categorization system comprises a set of categories, and their relationships as
    well as metadata describing the categorization system itself.

    Use the categorization object like a dictionary, where codes can be translated
    to their meaning using ``cat[code]`` and all codes are available using
    ``cat.keys()``. Metadata about the categorization is provided in attributes.
    If `pandas` is available, you can access a `pandas.DataFrame` with all
    category codes, and their meanings at ``cat.df``.

    Attributes
    ----------
    name : str
        The unique name/code
    references : str
        Citable reference(s)
    title : str
        A short, descriptive title for humans
    comment : str
        Notes and explanations for humans
    institution : str
        Where the categorization originates
    last_update : datetime.date
        The date of the last change
    version : str, optional
        The version of the Categorization, if there are multiple versions
    hierarchical : bool
        True if descendants and ancestors are defined
    """

    hierarchical: bool = False

    _strictyaml_schema = sy.Map(
        {
            "name": sy.Str(),
            "title": sy.Str(),
            "comment": sy.Str(),
            "references": sy.Str(),
            "institution": sy.Str(),
            "last_update": sy.Str(),
            "hierarchical": sy.Bool(),
            sy.Optional("version"): sy.Str(),
            "categories": sy.MapPattern(sy.Str(), Category._strictyaml_schema),
        }
    )

    def _add_categories(self, categories: typing.Dict[str, typing.Dict]):
        for code, spec in categories.items():
            cat = Category.from_spec(code=code, spec=spec, categorization=self)

            self._primary_code_map[code] = cat
            for icode in cat.codes:
                self._all_codes_map[icode] = cat

    def __init__(
        self,
        *,
        categories: typing.Dict[str, typing.Dict],
        name: str,
        title: str,
        comment: str,
        references: str,
        institution: str,
        last_update: datetime.date,
        version: typing.Optional[str] = None,
    ):
        self._primary_code_map = {}
        self._all_codes_map = {}
        self.name = name
        self.references = references
        self.title = title
        self.comment = comment
        self.institution = institution
        self.last_update = last_update
        self.version = version

        self._add_categories(categories)

    @classmethod
    def from_yaml(
        cls, filepath: typing.Union[str, pathlib.Path, typing.IO[bytes]]
    ) -> "Categorization":
        """Read Categorization from a StrictYaml file."""
        try:
            yaml = sy.load(filepath.read(), schema=cls._strictyaml_schema)
        except AttributeError:
            with open(filepath) as fd:
                yaml = sy.load(fd.read(), schema=cls._strictyaml_schema)
        return cls.from_spec(yaml.data)

    @classmethod
    def from_spec(cls, spec: typing.Dict[str, typing.Any]) -> "Categorization":
        """Create Categorization from a Dictionary specification."""
        if spec["hierarchical"] != cls.hierarchical:
            raise ValueError(
                "Specification is for a hierarchical categorization, use"
                "HierarchicalCategorization.from_spec."
            )
        last_update = datetime.date.fromisoformat(spec["last_update"])
        return cls(
            categories=spec["categories"],
            name=spec["name"],
            title=spec["title"],
            comment=spec["comment"],
            references=spec["references"],
            institution=spec["institution"],
            last_update=last_update,
            version=spec.get("version", None),
        )

    @staticmethod
    def from_pickle(
        filepath: typing.Union[str, pathlib.Path, typing.IO[bytes]]
    ) -> "Categorization":
        """De-serialize Categorization from a file written by to_pickle.

        Note that this uses the pickle module, which executes arbitrary code in the
        provided file. Only load from pickle files that you trust."""
        return from_pickle(filepath)

    def to_spec(self) -> typing.Dict[str, typing.Any]:
        """Turn this categorization into a specification dictionary ready to be written
        to a yaml file.

        Returns
        -------
        spec: dict
            Specification dictionary understood by `from_spec`.
        """
        spec = {
            "name": self.name,
            "title": self.title,
            "comment": self.comment,
            "references": self.references,
            "institution": self.institution,
            "hierarchical": self.hierarchical,
            "last_update": self.last_update.isoformat(),
        }
        if self.version is not None:
            spec["version"] = self.version
        spec["categories"] = {}
        for cat in self.values():
            code, cat_spec = cat.to_spec()
            spec["categories"][code] = cat_spec

        return spec

    def to_yaml(self, filepath: typing.Union[str, pathlib.Path]) -> None:
        """Write to a YAML file."""
        spec = self.to_spec()
        yaml = YAML()
        yaml.default_flow_style = False
        with open(filepath, "w") as fd:
            yaml.dump(spec, fd)

    def to_pickle(self, filepath: typing.Union[str, pathlib.Path]) -> None:
        """Serialize to a file using python's pickle."""
        spec = self.to_spec()
        with open(filepath, "wb") as fd:
            pickle.dump(spec, fd, protocol=4)

    def keys(self) -> typing.KeysView[str]:
        """Iterate over the codes for all categories."""
        return self._primary_code_map.keys()

    def values(self) -> typing.ValuesView[Category]:
        """Iterate over the categories."""
        return self._primary_code_map.values()

    def items(self) -> typing.ItemsView[str, Category]:
        """Iterate over (primary code, category) pairs."""
        return self._primary_code_map.items()

    def all_keys(self) -> typing.KeysView[str]:
        """Iterate over all codes for all categories."""
        return self._all_codes_map.keys()

    def __iter__(self) -> typing.Iterable[str]:
        return iter(self._primary_code_map)

    def __getitem__(self, code: str) -> Category:
        """Get the category for a code."""
        return self._all_codes_map[code]

    def __contains__(self, code: str) -> bool:
        """Can the code be mapped to a category?"""
        return code in self._all_codes_map

    def __len__(self) -> int:
        return len(self._primary_code_map)

    def __repr__(self) -> str:
        return (
            f"<Categorization {self.name} {self.title!r} with {len(self)} categories>"
        )

    def __str__(self) -> str:
        return self.name

    @property
    def df(self) -> "pandas.DataFrame":
        """All category codes as a pandas dataframe."""
        titles = []
        comments = []
        alternative_codes = []
        for cat in self.values():
            titles.append(cat.title)
            comments.append(cat.comment)
            alternative_codes.append(cat.codes[1:])
        return pandas.DataFrame(
            index=self.keys(),
            data={
                "title": titles,
                "comment": comments,
                "alternative_codes": alternative_codes,
            },
        )

    def _extend_prepare(
        self,
        *,
        categories: typing.Optional[typing.Dict[str, typing.Dict]] = None,
        alternative_codes: typing.Optional[typing.Dict[str, str]] = None,
        name: str,
        title: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        last_update: typing.Optional[datetime.date] = None,
    ) -> typing.Dict[str, typing.Any]:
        spec = self.to_spec()

        spec["name"] = f"{self.name}_{name}"
        spec["references"] = ""
        spec["institution"] = ""

        if title is None:
            spec["title"] = f"{self.title} + {name}"
        else:
            spec["title"] = self.title + title

        if comment is None:
            spec["comment"] = f"{self.comment} extended by {name}"
        else:
            spec["comment"] = self.comment + comment

        if last_update is None:
            spec["last_update"] = datetime.date.today().isoformat()
        else:
            spec["last_update"] = last_update.isoformat()

        if categories is not None:
            spec["categories"].update(categories)

        if alternative_codes is not None:
            for alias, primary in alternative_codes.items():
                if "alternative_codes" not in spec["categories"][primary]:
                    spec["categories"][primary]["alternative_codes"] = []

                spec["categories"][primary]["alternative_codes"].append(alias)

        return spec

    def extend(
        self,
        *,
        categories: typing.Optional[typing.Dict[str, typing.Dict]] = None,
        alternative_codes: typing.Optional[typing.Dict[str, str]] = None,
        name: str,
        title: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        last_update: typing.Optional[datetime.date] = None,
    ) -> "Categorization":
        """Extend the categorization with additional categories, yielding a new
        categorization.

        Metadata: the ``name``, ``title``, ``comment``, and ``last_update`` are updated
        automatically (see below), the ``institution`` and ``references`` are deleted
        and the values for ``version`` and ``hierarchical`` are kept.
        You can set more accurate metadata (for example, your institution) on the
        returned object if needed.

        Parameters
        ----------
        categories: dict, optional
           Map of new category codes to their specification. The specification is a
           dictionary with the keys "title", optionally "comment", and optionally
           "alternative_codes".
        alternative_codes: dict, optional
           Map of new alternative codes. A dictionary with the new alternative code
           as key and existing code as value.
        name : str
           The name of your extension. The returned Categorization will have a name
           of "{old_name}_{name}", indicating that it is an extension of the underlying
           Categorization.
        title : str, optional
           A string to add to the original title. If not provided, " + {name}" will be
           used.
        comment : str, optional
           A string to add to the original comment. If not provided,
           " extended by {name}" will be used.
        last_update : datetime.date, optional
           The date of the last update to this extension. Today will be used if not
           provided.

        Returns
        -------
        Extended categorization : Categorization
        """
        spec = self._extend_prepare(
            name=name,
            categories=categories,
            title=title,
            comment=comment,
            last_update=last_update,
            alternative_codes=alternative_codes,
        )

        return Categorization.from_spec(spec)

    def __eq__(self, other):
        if not isinstance(other, Categorization):
            return False
        if self.name != other.name:
            return False
        return self._primary_code_map == other._primary_code_map


class HierarchicalCategorization(Categorization):
    """In a hierarchical categorization, descendants and ancestors (parents and
    children) are defined for each category.

    Attributes
    ----------
    total_sum : bool
        If the sum of the values of children equals the value of the parent for
        extensive quantities. For example, a Categorization containing the Countries in
        the EU and the EU could set `total_sum = True`, because the emissions of all
        parts of the EU must equal the emissions of the EU. On the contrary, a
        categorization of Industries with categories `Power:Fossil Fuels` and
        `Power:Gas` which are both children of `Power` must set `total_sum = False`
        to avoid double counting of fossil gas.
    canonical_top_level_category : HierarchicalCategory
        The level of a category is calculated with respect to the canonical top level
        category. Commonly, this will be the world total or a similar category. If the
        canonical top level category is not set (i.e. is ``None``), levels are not
        defined for categories.
    """

    hierarchical = True

    _strictyaml_schema = sy.Map(
        {
            "name": sy.Str(),
            "title": sy.Str(),
            "comment": sy.Str(),
            "references": sy.Str(),
            "institution": sy.Str(),
            "last_update": sy.Str(),
            "hierarchical": sy.Bool(),
            sy.Optional("version"): sy.Str(),
            "total_sum": sy.Bool(),
            sy.Optional("canonical_top_level_category"): sy.Str(),
            "categories": sy.MapPattern(
                sy.Str(), HierarchicalCategory._strictyaml_schema
            ),
        }
    )

    def _add_categories(self, categories: typing.Dict[str, typing.Dict]):
        for code, spec in categories.items():
            cat = HierarchicalCategory.from_spec(
                code=code, spec=spec, categorization=self
            )

            self._primary_code_map[code] = cat
            self._graph.add_node(cat)
            for icode in cat.codes:
                self._all_codes_map[icode] = cat

        for code, spec in categories.items():
            if "children" in spec:
                parent = self._all_codes_map[code]
                for i, child_set in enumerate(spec["children"]):
                    for child_code in child_set:
                        self._graph.add_edge(
                            parent, self._all_codes_map[child_code], set=i
                        )

    def __init__(
        self,
        *,
        categories: typing.Dict[str, typing.Dict],
        name: str,
        title: str,
        comment: str,
        references: str,
        institution: str,
        last_update: datetime.date,
        version: typing.Optional[str] = None,
        total_sum: bool,
        canonical_top_level_category: typing.Optional[str] = None,
    ):
        self._graph = nx.MultiDiGraph()
        Categorization.__init__(
            self,
            categories=categories,
            name=name,
            title=title,
            comment=comment,
            references=references,
            institution=institution,
            last_update=last_update,
            version=version,
        )
        self.total_sum = total_sum
        if canonical_top_level_category is None:
            self.canonical_top_level_category: typing.Optional[
                HierarchicalCategory
            ] = None
        else:
            self.canonical_top_level_category = self._all_codes_map[
                canonical_top_level_category
            ]

    def __getitem__(self, code: str) -> HierarchicalCategory:
        """Get the category for a code."""
        return self._all_codes_map[code]

    def values(self) -> typing.ValuesView[HierarchicalCategory]:
        """Iterate over the categories."""
        return self._primary_code_map.values()

    def items(self) -> typing.ItemsView[str, HierarchicalCategory]:
        """Iterate over (primary code, category) pairs."""
        return self._primary_code_map.items()

    @classmethod
    def from_spec(
        cls, spec: typing.Dict[str, typing.Any]
    ) -> "HierarchicalCategorization":
        """Create Categorization from a Dictionary specification."""
        if spec["hierarchical"] != cls.hierarchical:
            raise ValueError(
                "Specification is for a non-hierarchical categorization, use"
                "Categorization.from_spec."
            )
        last_update = datetime.date.fromisoformat(spec["last_update"])
        return cls(
            categories=spec["categories"],
            name=spec["name"],
            title=spec["title"],
            comment=spec["comment"],
            references=spec["references"],
            institution=spec["institution"],
            last_update=last_update,
            version=spec.get("version", None),
            total_sum=spec["total_sum"],
            canonical_top_level_category=spec.get("canonical_top_level_category", None),
        )

    def to_spec(self) -> typing.Dict[str, typing.Any]:
        """Turn this categorization into a specification dictionary ready to be written
        to a yaml file.

        Returns
        -------
        spec: dict
            Specification dictionary understood by `from_spec`.
        """
        # we can't call Categorization.to_spec here because we need to control ordering
        # in the returned dict so that we get nicely ordered yaml files.
        spec = {
            "name": self.name,
            "title": self.title,
            "comment": self.comment,
            "references": self.references,
            "institution": self.institution,
            "hierarchical": self.hierarchical,
            "last_update": self.last_update.isoformat(),
        }
        if self.version is not None:
            spec["version"] = self.version
        spec["total_sum"] = self.total_sum
        if self.canonical_top_level_category is not None:
            spec[
                "canonical_top_level_category"
            ] = self.canonical_top_level_category.codes[0]

        spec["categories"] = {}
        for cat in self.values():
            code, cat_spec = cat.to_spec()
            spec["categories"][code] = cat_spec

        return spec

    @property
    def _canonical_subgraph(self) -> nx.DiGraph:
        # TODO: from python 3.8 on, there is functools.cached_property to
        # automatically cache this - as soon as we drop python 3.7 support, we can
        # easily add it.
        return nx.DiGraph(
            self._graph.edge_subgraph(
                ((u, v, 0) for (u, v, s) in self._graph.edges(data="set") if s == 0)
            )
        )

    def _show_subtree(
        self,
        *,
        node: HierarchicalCategory,
        prefix="",
        last=False,
        format_func: typing.Callable[[HierarchicalCategory], str] = str,
        maxdepth: typing.Optional[int],
    ) -> str:
        if maxdepth is not None:
            maxdepth -= 1
        if prefix:
            if last:
                r = f"{prefix[:-1]}╰{format_func(node)}\n"
            else:
                r = f"{prefix[:-1]}├{format_func(node)}\n"
        else:
            r = f"{format_func(node)}\n"

        if maxdepth is not None and maxdepth == 0:
            return r

        child_sets = node.children
        if len(child_sets) == 0:
            return r
        elif len(child_sets) == 1:
            children = child_sets[0]
            if children:
                children_sorted = natsort.natsorted(children, key=format_func)
                for child in children_sorted[:-1]:
                    r += self._show_subtree(
                        node=child,
                        prefix=prefix + "│",
                        format_func=format_func,
                        maxdepth=maxdepth,
                    )
                r += self._show_subtree(
                    node=children_sorted[-1],
                    prefix=prefix + " ",
                    last=True,
                    format_func=format_func,
                    maxdepth=maxdepth,
                )
        else:
            prefix += "║"
            first = True
            for children in child_sets:
                if children:
                    if first:
                        r += f"{prefix[:-1]}╠╤══\n"
                        first = False
                    else:
                        r += f"{prefix[:-1]}╠╕\n"

                    children_sorted = natsort.natsorted(children, key=format_func)
                    for child in children_sorted[:-1]:
                        r += self._show_subtree(
                            node=child,
                            prefix=prefix + "│",
                            format_func=format_func,
                            maxdepth=maxdepth,
                        )
                    r += self._show_subtree(
                        node=children_sorted[-1],
                        prefix=prefix + " ",
                        last=True,
                        format_func=format_func,
                        maxdepth=maxdepth,
                    )
            r += f"{prefix[:-1]}╚═══\n"

        return r

    def show_as_tree(
        self,
        format_func: typing.Callable[[HierarchicalCategory], str] = str,
        maxdepth: typing.Optional[int] = None,
    ) -> str:
        """Format the hierarchy as a tree.

        Starting from top-level categories (i.e. categories without parents), the full
        tree of categories is show, with children connected to their parents using
        lines. If a parent category has one set of children, the children are connected
        to each other and the parent with a simple line. If a parent category has
        multiple sets of children, the sets are connected to parent with double lines
        and the children in a set are connected to each other with simple lines.

        Parameters
        ----------
        format_func: callable, optional
            Function to call to format categories for display. Each category is
            formatted for display using format_func(category), so format_func should
            return a string without line breaks, otherwise the tree will look weird.
            By default, str() is used, so that the first code and the title of the
            category are used.
        maxdepth: int, optional
            Maximum depth to show in the tree. By default, goes to arbitrary depth.

        Returns
        -------
        tree_str: str
            Representation of the hierarchy as formatted string. print() it for optimal
            viewing.
        """
        top_level_nodes = (node for node in self.values() if not node.parents)
        r = ""
        for top_level_node in top_level_nodes:
            r += (
                self._show_subtree(
                    node=top_level_node, format_func=format_func, maxdepth=maxdepth
                )
                + "\n"
            )
        return r

    def extend(
        self,
        *,
        categories: typing.Optional[typing.Dict[str, typing.Dict]] = None,
        alternative_codes: typing.Optional[typing.Dict[str, str]] = None,
        children: typing.Optional[typing.List[tuple]] = None,
        name: str,
        title: typing.Optional[str] = None,
        comment: typing.Optional[str] = None,
        last_update: typing.Optional[datetime.date] = None,
    ) -> "HierarchicalCategorization":
        """Extend the categorization with additional categories and relationships,
        yielding a new categorization.

        Metadata: the ``name``, ``title``, ``comment``, and ``last_update`` are updated
        automatically (see below), the ``institution`` and ``references`` are deleted
        and the values for ``version``, ``hierarchical``, ``total_sum``, and
        ``canonical_top_level_category`` are kept.
        You can set more accurate metadata (for example, your institution) on the
        returned object if needed.

        Parameters
        ----------
        categories: dict, optional
           Map of new category codes to their specification. The specification is a
           dictionary with the keys "title", optionally "comment", and optionally
           "alternative_codes".
        alternative_codes: dict, optional
           Map of new alternative codes. A dictionary with the new alternative code
           as key and existing code as value.
        children: list, optional
           List of ``(parent, (child1, child2, …))`` pairs. The given relationships will
           be inserted in the extended categorization.
        name : str
           The name of your extension. The returned Categorization will have a name
           of "{old_name}_{name}", indicating that it is an extension of the underlying
           Categorization.
        title : str, optional
           A string to add to the original title. If not provided, " + {name}" will be
           used.
        comment : str, optional
           A string to add to the original comment. If not provided,
           " extended by {name}" will be used.
        last_update : datetime.date, optional
           The date of the last update to this extension. Today will be used if not
           provided.

        Returns
        -------
        Extended categorization : HierarchicalCategorization
        """
        spec = self._extend_prepare(
            name=name,
            categories=categories,
            title=title,
            comment=comment,
            last_update=last_update,
            alternative_codes=alternative_codes,
        )

        if children is not None:
            for parent, child_set in children:
                if "children" not in spec["categories"][parent]:
                    spec["categories"][parent]["children"] = []
                spec["categories"][parent]["children"].append(child_set)

        return HierarchicalCategorization.from_spec(spec)

    @property
    def df(self) -> "pandas.DataFrame":
        """All category codes as a pandas dataframe."""
        titles = []
        comments = []
        alternative_codes = []
        children = []
        for cat in self.values():
            titles.append(cat.title)
            comments.append(cat.comment)
            alternative_codes.append(cat.codes[1:])
            children.append(
                tuple(tuple(sorted(c.codes[0] for c in cs)) for cs in cat.children)
            )
        return pandas.DataFrame(
            index=self.keys(),
            data={
                "title": titles,
                "comment": comments,
                "alternative_codes": alternative_codes,
                "children": children,
            },
        )

    def level(self, cat: typing.Union[str, HierarchicalCategory]) -> int:
        """The level of the given category.

        The canonical top-level category has level 1 and its children have level 2 etc.

        To calculate the level, first only the first ("canonical") set of children is
        considered. Only if no path from the canonical top-level category to the
        given category can be found all other sets of children are considered to
        calculate the level.
        """
        if not isinstance(cat, HierarchicalCategory):
            return self.level(self[cat])
        if not isinstance(self.canonical_top_level_category, HierarchicalCategory):
            raise ValueError(
                "Can not calculate the level without a canonical_top_level_category."
            )

        # first use the canonical subgraph for shortest paths
        csg = self._canonical_subgraph
        try:
            sp = nx.shortest_path_length(csg, self.canonical_top_level_category, cat)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            try:
                sp = nx.shortest_path_length(
                    self._graph, self.canonical_top_level_category, cat
                )
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                raise ValueError(
                    f"{cat.codes[0]!r} is not a transitive child of the "
                    f"canonical top level "
                    f"{self.canonical_top_level_category.codes[0]!r}."
                )

        return sp + 1

    def parents(
        self, cat: typing.Union[str, HierarchicalCategory]
    ) -> typing.Set[HierarchicalCategory]:
        """The direct parents of the given category."""
        if not isinstance(cat, HierarchicalCategory):
            return self.parents(self._all_codes_map[cat])

        return set(self._graph.predecessors(cat))

    def children(
        self, cat: typing.Union[str, HierarchicalCategory]
    ) -> typing.List[typing.Set[HierarchicalCategory]]:
        """The list of sets of direct children of the given category."""
        if not isinstance(cat, HierarchicalCategory):
            return self.children(self._all_codes_map[cat])

        children_dict = {}
        for (_, child, setno) in self._graph.edges(cat, "set"):
            if setno not in children_dict:
                children_dict[setno] = []
            children_dict[setno].append(child)

        children = [set(children_dict[x]) for x in sorted(children_dict.keys())]
        return children


def from_pickle(
    filepath: typing.Union[str, pathlib.Path, typing.IO[bytes]]
) -> typing.Union[Categorization, HierarchicalCategorization]:
    """De-serialize Categorization or HierarchicalCategorization from a file written by
    to_pickle.

    Note that this uses the pickle module, which executes arbitrary code in the
    provided file. Only load from pickle files that you trust."""
    try:
        spec = pickle.load(filepath)
    except TypeError:
        with open(filepath, "rb") as fd:
            spec = pickle.load(fd)

    return from_spec(spec)


def from_spec(
    spec: typing.Dict[str, typing.Any]
) -> typing.Union[Categorization, HierarchicalCategorization]:
    """Create Categorization or HierarchicalCategorization from a dict specification."""
    if spec["hierarchical"]:
        return HierarchicalCategorization.from_spec(spec)
    else:
        return Categorization.from_spec(spec)


def from_yaml(
    filepath: typing.Union[str, pathlib.Path, typing.IO[bytes]]
) -> typing.Union[Categorization, HierarchicalCategorization]:
    """Read Categorization or HierarchicalCategorization from a StrictYaml file."""
    try:
        yaml = sy.load(filepath.read())
        filepath.seek(0)
    except AttributeError:
        with open(filepath) as fd:
            yaml = sy.load(fd.read())
    hier = yaml.data["hierarchical"]
    if hier in ("yes", "true", "True"):
        cls = HierarchicalCategorization
    elif hier in ("no", "false", "False"):
        cls = Categorization
    else:
        raise ValueError(
            f"'hierarchical' must be 'yes', 'true', 'True', 'no', 'false' or 'False',"
            f" not {hier!r}."
        )
    return cls.from_yaml(filepath)
