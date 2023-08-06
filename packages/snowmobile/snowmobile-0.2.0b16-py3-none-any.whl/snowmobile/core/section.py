"""

----

A :class:`Section` is created by a :class:`~snowmobile.core.Statement` or a
:class:`~snowmobile.core.cfg.Marker` when the :meth:`~snowmobile.Script.doc()`
method is called on an instance of :class:`~snowmobile.Script`.


.. note::

    :meth:`script.doc() <snowmobile.Script.doc()>` returns a
    :class:`~snowmobile.core.markup.Markup` instance containing a :class:`Section`
    for each statement or marker *within the script's
    context at the time* :meth:`~snowmobile.Script.doc()` *was called*.

    Respecting the script's context enables calling
    :meth:`script.doc() <snowmobile.Script.doc()>` on the instance of
    ``script`` returned by :meth:`script.filter() <snowmobile.Script.filter()>`
    and exporting an annotated markdown file and/or a tidied sql file that
    include only the contents within that context.


By default this results in two files being exported into a `.snowmobile` folder
in the same directory as the .sql file with which the instance of
:class:`~snowmobile.Script` was instantiated.

Header-levels and formatting of tagged information is configured in the
*snowmobile.toml* file, with defaults resulting in the following structure::

        ```md

        # Script Name.sql         *[script name gets an 'h1' header]
        ----

        - **Tag1**: Value1         [tags are bolded, associated values are not]
        - **Tag2**: Value2         [same for all tags/attributes found]
        - ...

        **Description**           *[except for the 'Description' section]
                                  *[this is just a blank canvas of markdown..]
                                  *[..but this is configurable]

        ## (1) create-table~dummy_name *[statements get 'h2' level headers]
        ----

        - **Tag1**: Value1       *[tags can also be validations arguments..
        - **Arg1**: Val2          [that snowmobile will run on the sql results]

        **Description**          *[statements get one of these too]

        **SQL**                  *[their rendered sql does as well]
            ...sql
                ...
                ...
            ...


        ## (2) update-table~dummy_name2
        ----
        [structure repeats for all statements in the script]

        ```

"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import pandas as pd

from . import Generic, Configuration, errors
from .cfg import Markup
from .utils import parsing as p


class Name(Generic):
    """Handles attribute-name parsing including identification of wildcards.

    """

    def __init__(self, nm: str, cfg: Configuration, is_title: Optional[bool] = None):
        super().__init__()

        cfg_md = cfg.script.markup
        cfg_script = cfg.script

        self.nm_raw = nm

        self.nm_stripped, self.flags = cfg.wildcards.partition_on_wc(attr_nm=nm)

        self.is_paragraph = cfg_script.patterns.wildcards.wc_paragraph in self.flags
        self.is_no_reformat = cfg_script.patterns.wildcards.wc_as_is in self.flags
        self.is_omit_nm = cfg_script.patterns.wildcards.wc_omit_attr_nm in self.flags

        self.is_results = self.check_reserved_nm(
            attr_name=self.nm_stripped,
            searching_for=cfg_md.attrs.reserved["query-results"].attr_nm,
        )
        self.is_sql = self.check_reserved_nm(
            attr_name=self.nm_stripped,
            searching_for=cfg_md.attrs.reserved["rendered-sql"].attr_nm,
        )

        if self.is_omit_nm:
            self.nm_adj = str()
            self.is_paragraph = True
        elif self.is_no_reformat:
            self.nm_adj = self.nm_stripped
        elif self.nm_stripped in cfg_md.attrs.from_namespace:
            self.nm_adj = cfg_md.attrs.from_namespace.get(self.nm_stripped)
        else:
            self.nm_adj = self.nm_stripped.title() if not is_title else self.nm_stripped

        self.specified_position = cfg_md.attrs.get_position(attr=self.nm_stripped)

    @staticmethod
    def check_reserved_nm(attr_name: str, searching_for: str) -> bool:
        """Safely checks for key terms within attribute names.

        Args:
            attr_name (str):
                Attribute name that we are checking (e.g. 'Results\\*')
            searching_for (str):
                Keyword we are searching for (e.g. 'results')

        """
        attr_name, searching_for = attr_name.lower(), searching_for.lower()
        len_attr, len_kw = len(attr_name), len(searching_for)
        if len_attr >= len_kw:
            return attr_name.startswith(searching_for)
        else:
            return False

    def __repr__(self):
        return f"Name(nm='{self.nm_raw}', nm_adj='{self.nm_adj}')"

    def __str__(self):
        return f"Name(nm='{self.nm_raw}', nm_adj='{self.nm_adj}')"


# TESTS: Add tests for Item
class Item(Name):
    """Represents a piece of text/content within a header section."""

    _DELIMITER = "~"
    _INDENT_CHAR = "\t"

    def __init__(
        self,
        index: int,
        flattened_attrs: Tuple,
        cfg: Configuration,
        results: Optional[pd.DataFrame] = None,
        sql_md: Optional[str] = None,
    ):
        cfg_md = cfg.script.markup
        self.is_first: bool = bool()

        self.cfg_md: Markup = cfg_md
        self.index = index
        self.indent, nested, in_script_value = flattened_attrs

        self._split = nested.split(self._DELIMITER)

        super().__init__(nm=self._split[-1], cfg=cfg)

        self.depth = len(self._split) - 1
        self.indent: str = self._INDENT_CHAR * self.depth
        parent = self._split[self.depth - 1]
        self.parent = Name(nm=parent, cfg=cfg)

        self._is_reserved: bool = False
        if self.is_results:
            self.value = self.as_results(results=results, cfg_md=cfg_md)
            self._is_reserved = True
        elif self.is_sql:
            self.value = sql_md
            self._is_reserved = True
        else:
            self.value = in_script_value

    def is_sibling(self, other: Item) -> bool:
        return self.parent.nm_adj == other.parent.nm_adj

    def update(self, items: List[Item]):
        first_index_at_level = min({i.index for i in items if self.is_sibling(i)})
        if self.index == first_index_at_level and self.depth != 0:
            self.is_first = True
        return self

    @staticmethod
    def as_results(results: pd.DataFrame, cfg_md: Markup):
        results_cfg = cfg_md.attrs.reserved["query-results"]

        display_record_limit = (
            cfg_md.result_limit if cfg_md.result_limit != -1 else results.shape[0]
        )
        results_sub = results.head(display_record_limit)
        if results_cfg.default_format == "markdown":
            return results_sub.to_markdown(index=False)
        else:
            return results_sub.to_html(index=False)

    @property
    def _as_md_parent(self):
        parent_indent = (self.depth - 1) * self._INDENT_CHAR
        return f"{parent_indent}{self.cfg_md.bullet_char} {self.parent.nm_adj}"

    @property
    def _as_md(self):
        attr_nm = self._format_attr(attr=self.nm_adj)
        attr_value = self._format_attr(attr=self.value, is_value=True)
        if not self.is_paragraph:
            return f"{self.indent}{self.cfg_md.bullet_char} {attr_nm}: {attr_value}"
        elif attr_nm:
            return f"\n{attr_nm}\n{attr_value}"
        else:
            return f"\n{attr_value}"

    def _format_attr(self, attr: str, is_value: bool = False):
        if self._is_reserved or self.is_no_reformat or self.is_paragraph:
            return attr
        wrap_character = (
            self.cfg_md.attr_nm_wrap_char
            if not is_value
            else self.cfg_md.attr_value_wrap_char
        )
        return f"{wrap_character}{attr}{wrap_character}"

    @property
    def md(self):
        if not self.is_first:
            return self._as_md
        else:
            return f"{self._as_md_parent}\n{self._as_md}"

    def __repr__(self):
        return f"section.Item('{self.nm_adj}')"

    def __str__(self):
        return f"section.Item('{self.nm_adj}')"


# TESTS: Add tests for Section
class Section(Generic):
    """Represents any (1-6 level) header section within `Script Name (doc).md`.


    This class is intended to be accessed as an attribute of
    `snowmobile.Script` and shouldn't need to be instantiated directly.

    In order to keep the core parsing functionality available without
    requiring execution of any statements in the script but also including
    execution data if available, the current implementation is heavily
    reliant on properties over attributes to reconcile what's populated in
    the `statements' and `executed` attributes of the `Script` object.



    Attributes:
        hx (str): String form of the markdown header tag (e.g. '#' for h1),
            based on the script/statement header-level specifications in
            `snowmobile.toml`.
        h_contents (str): Text to place in the header.
        index (int): The index position of the associated information, which
            indicates the statement number and is left as `None' for a script
            section.
        parsed (dict): Parsed arguments from within the sql script, returned
            from ``utils.parsing.parse_multiline()``.
        sql (str): Raw sql, will be `None` in the case of the top-level
            script-section if included.
        is_marker (bool): Indicating of whether the section metadata is
            script-level (as opposed to statement-level).

    """

    def __init__(
        self,
        cfg: Configuration,
        is_marker: bool = None,
        h_contents: Optional[str] = None,
        index: Optional[int] = None,
        parsed: Optional[Dict] = None,
        raw: Optional[str] = None,
        sql: Optional[str] = None,
        results: Optional[pd.DataFrame] = None,
        incl_raw: bool = False,
        is_multiline: bool = False,
    ):
        """Instantiation of a ``script.Section`` object.

        Args:
            is_marker: Indicating of whether the section metadata is
                script-level (as opposed to statement-level).
            h_contents: Text to place in the header.
            index: The index position of the associated information,
                which indicates the statement number and is left as `None' for
                 a script section.
            parsed: Parsed arguments from within the sql script, returned
                from `utils.parsing.parse_multiline()`.
            sql: Raw sql, will be `None` in the case of the top-level
                script-section if included.

        """
        super().__init__()

        self.cfg: Configuration = cfg
        self.is_marker = is_marker or bool()
        self.is_multiline = is_multiline
        self.sql: str = sql
        self.results = results
        self.index: int = index
        self.raw = raw or str()
        self.incl_raw = incl_raw

        self._name = Name(nm=h_contents, cfg=cfg, is_title=True)
        if len(self._name.flags) > 1:
            raise errors.InvalidTagsError(
                msg=self._exception_invalid_title(raw=h_contents)
            )
        self.hx = self.cfg.markdown.pref_header(
            is_marker=self.is_marker,
            from_wc=self._name.flags[0] if self._name.flags else str(),
        )
        self.h_contents = self._name.nm_adj

        grouped_attrs = self.cfg.attrs.group_parsed_attrs(parsed)
        self.parsed: Dict = self.reorder_attrs(parsed=grouped_attrs, cfg=cfg)
        self.items: List[Item] = self.parse_contents(cfg=cfg)

    def reorder_attrs(self, parsed: dict, cfg: Configuration) -> Dict:
        """Re-orders parsed attributes based on configuration."""
        parsed = self.cfg.attrs.add_reserved_attrs(parsed, self.is_marker)
        specified_position_to_attr_nm: Dict[int, str] = {
            Name(nm=k, cfg=cfg).specified_position: k
            for k in parsed
            if Name(nm=k, cfg=cfg).specified_position
        }
        for position in sorted(specified_position_to_attr_nm):
            attr_nm = specified_position_to_attr_nm[position]
            parsed[attr_nm] = parsed.pop(attr_nm)  # re-inserting in order
        return parsed

    def parse_contents(self, cfg: Configuration) -> List[Item]:
        """Unpacks sorted dictionary of parsed attributes into formatted Items."""
        # how is the sql getting included in the statements but not the
        # markers?
        flattened = p.dict_flatten(
            attrs=self.parsed, bullet_char=cfg.script.markup.bullet_char
        )
        items = [
            Item(
                index=i,
                flattened_attrs=v,
                cfg=cfg,
                results=self.results,
                sql_md=self.sql_md,
            )
            for i, v in enumerate(flattened, start=1)
        ]
        return [i.update(items=items) for i in items]

    @property
    def header(self) -> str:
        """Constructs the header for a section.

        Uses specifications in `snowmobile.toml` to determine:
            (1) The level of the header depending on whether it's a
                statement section or a script section.
            (2) Whether or not to include the statement index as part of the
                header.

        Returns:
            Formatted header line as a string.

        """
        if self.is_marker or not self.cfg.markdown.incl_index_in_sh:
            return f"{self.hx} {self.h_contents}"
        else:
            return f"{self.hx} ({self.index}) {self.h_contents}"

    @property
    def sql_md(self) -> str:
        """Returns renderable sql or an empty string if script-level section."""
        sql = self.cfg.script.power_strip(
            val_to_strip=("" if self.is_marker else self.sql),
            chars_to_strip=[";", " ", "\n"],
        )
        if self.incl_raw:
            raw = self.cfg.script.as_parsable(self.raw, self.is_multiline)
            sql = f"{raw}\n{sql}"
        if not self.is_marker:
            sql = f"{sql};"
        if self.is_marker and not self.incl_raw:
            return str()
        char = "\n"
        return f"```sql\n{sql.strip(char)}\n```"

    @property
    def body(self):
        return "\n".join(i.md for i in self.items)

    @property
    def md(self) -> str:
        """Constructs a full section as a string from various components.

        Returns:
            Renderable string of the section.

        """
        return "\n".join([self.header, self.body])

    @staticmethod
    def _exception_invalid_title(raw: str) -> str:
        """Invalid title message; isolating to avoid cluttering __init__ method."""
        return f"""
Multiple sets of wildcards detected in the below statement or marker title; only
a single set of unescaped wildcards is permitted.
```
{raw}
```
"""

    def __repr__(self):
        return f"script.Section({str(vars(self))})"

    def __str__(self):
        return f"script.Section('{self.h_contents}')"
