"""
Base class for all :class:`Statement` objects.
"""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, Optional, Union, Tuple

import pandas as pd
import sqlparse
from IPython.display import Markdown, display
from pandas.io.sql import DatabaseError as pdDataBaseError
from snowflake.connector.errors import DatabaseError, ProgrammingError

from . import ExceptionHandler, Section, Name, errors, cfg
from . import Generic, Snowmobile  # isort: skip


class Statement(Name, Generic):
    """Base class for all :class:`Statement` objects.

    Home for attributes and methods that are associated with **all** statement
    objects, generic or QA.

    Attributes:
        sn (snowmobile.connect):
            :class:`snowmobile.connect` object.
        statement (Union[sqlparse.sql.Statement, str]):
            A :class:`sqlparse.sql.Statement` object.
        index (int):
            The context-specific index position of a statement within a script;
            can be `None`.
        _index (int):
            The original index position of a statement as read from the source;
            This is used to restore the index position of a given statement
            before exiting a specified context within :class:`snowmobile.Script`.
        patterns (config.Pattern):
            :class:`config.Pattern` object for more succinct access to
            values specified in **snowmobile.toml**.
        results (pd.DataFrame):
            The results of the statement if executed as a :class:`pandas.DataFrame`.
        outcome (int):
            Numeric indicator of outcome; defaults to `0` and is modified
            based on the outcome of statement execution and/or QA validation
            for derived classes.
        outcome_txt (str):
            Plain text of outcome ('skipped', 'failed', 'completed', 'passed').
        outcome_html (str):
            HTML text for the outcome as an admonition/information banner
            based on the following mapping of :attr:`outcome_txt` to
            admonition argument:
                *   `failed` ------> `warning`
                *   `completed` --> `info`
                *   `passed` -----> `success`
        start_time (int):
            Unix timestamp of the query start time if executed; 0 otherwise.
        end_time (int):
            Unix timestamp of the query end time if executed; 0 otherwise.
        execution_time (int):
            Execution time of the query in seconds if executed; 0 otherwise.
        execution_time_txt (str):
            Plain text description of execution time if executed; returned in
            seconds if execution time is less than 60 seconds, minutes otherwise.
        attrs_raw (str):
            A raw string of the tag/attributes associated with the statement.
        attrs_parsed (dict):
            A parsed dictionary of the tag/attributes associated with the statement.
        is_tagged (bool):
            Indicates whether or not the statement is tagged by the user.
        is_multiline (bool):
            Indicates whether or not a statement tag is a multiline tag; will
            be `False` by default if :attr:`is_tagged` is `False`.
        first_keyword (sqlparse.sql.Token):
            The first keyword within the statement as a :class:`sqlparse.sql.Token`.
        sql (str):
            The sql associated with the statement as a raw string.
        tag (Name):
            Statement's :class:`~snowmobile.core.name.Name`.

    """

    # fmt: off
    _PROCESS_OUTCOMES: Dict[Any, Any] = {
        -3: ("success", "passed"),
        -2: ("warning", "failed"),
        -1: ("-", "error: post-processing"),
        # -- derived end
        0: ("-", ""),
        # -- base start
        1: ("-", "error: execution"),
        2: ("success", "completed"),
    }

    _DERIVED_FAILURE_MAPPING = {
        'qa-diff': errors.QADiffFailure,
        'qa-empty': errors.QAEmptyFailure
    }
    # fmt: on

    def __init__(
        self,
        sn: Snowmobile,
        statement: Union[sqlparse.sql.Statement, str],
        index: Optional[int] = None,
        attrs_raw: Optional[str] = None,
        e: Optional[ExceptionHandler] = None,
        **kwargs,
    ):
        Generic.__init__(self)

        self._index: int = index
        self._outcome: int = int()

        self.outcome: bool = True
        self.executed: bool = bool()

        self.sn = sn
        self.statement: sqlparse.sql.Statement = sn.cfg.script.ensure_sqlparse(
            statement
        )

        self.patterns: cfg.Pattern = sn.cfg.script.patterns
        self.results: pd.DataFrame = pd.DataFrame()

        self.start_time: int = int()
        self.end_time: int = int()
        self.execution_time: int = int()
        self.execution_time_txt: str = str()

        self.attrs_raw = attrs_raw or str()
        self.is_multiline = "\n" in self.attrs_raw
        self.is_tagged: bool = bool(self.attrs_raw)
        self._sql = sn.cfg.script.isolate_sql(s=self.statement)
        self.attrs_parsed, nm = self.parse()

        Name.__init__(
            self, index=index, sql=self.sql, nm_pr=nm, configuration=self.sn.cfg
        )

        self.e = e or ExceptionHandler(within=self)

    @property
    def sql(self):
        """Raw sql from statement, including result limit if enabled."""
        if self.sn.cfg.script.result_limit in [-1, 0]:
            return self._sql
        return f"{self._sql}\nlimit {self.sn.cfg.script.result_limit}"

    def parse(self) -> Tuple[Dict, str]:
        """Parses a statement tag into a valid dictionary.

        Uses the values specified in **snowmobile.toml** to parse a
        raw string of statement arguments into a valid dictionary.

        note:
            *   If :attr:`is_multiline` is `True` and `name` is not included
                within the arguments, an assertion error will be thrown.
            *   If :attr:`is_multiline` is `False`, the raw string within
                the tag will be treated as the name.
            *   The :attr:`tag` attribute is set once parsing is completed
                and name has been validated.

        Returns (dict):
            Parsed tag arguments as a dictionary.

        """
        if not self.is_tagged:
            return dict(), str()

        if self.is_multiline:
            attrs_parsed = self.sn.cfg.script.parse_str(block=self.attrs_raw)
            if "name" in attrs_parsed:
                name = attrs_parsed.pop("name")
            else:
                try:
                    name = self.sn.cfg.script.parse_name(raw=self.attrs_raw)
                except errors.InvalidTagsError as e:
                    raise e

            return attrs_parsed, name

        return dict(), self.attrs_raw

    def start(self):
        """Sets :attr:`start_time` attribute."""
        self.start_time = time.time()

    def end(self):
        """Updates execution time attributes.

        In total, sets:
            *   :attr:`end_time`
            *   :attr:`execution_time`
            *   :attr:`execution_time_txt`

        """
        self._outcome, self.outcome, self.executed = 2, True, True
        self.end_time = time.time()
        self.execution_time = int(self.end_time - self.start_time)
        self.execution_time_txt = (
            f"{self.execution_time}s"
            if self.execution_time < 60
            else f"{int(self.execution_time/60)}m"
        )

    @property
    def attrs_total(self) -> Dict:
        """Parses namespace for attributes specified in **snowmobile.toml**.

        Searches attributes for those matching the keys specified in
        ``script.markdown.attributes.aliases`` within **snowmobile.toml**
        and adds to the existing attributes stored in :attr:`attrs_parsed`
        before returning.

        Returns (dict):
            Combined dictionary of statement attributes from those explicitly
            provided within the script and from object's namespace if specified
            in **snowmobile.toml**.

        """
        current_namespace = {
            **self.sn.cfg.attrs_from_obj(
                obj=self, within=list(self.sn.cfg.attrs.from_namespace)
            ),
            **self.sn.cfg.methods_from_obj(
                obj=self, within=list(self.sn.cfg.attrs.from_namespace)
            ),
        }
        namespace_overlap_with_config = set(
            current_namespace
        ).intersection(  # all from current namespace
            self.sn.cfg.attrs.from_namespace
        )  # snowmobile.toml
        attrs = {k: v for k, v in self.attrs_parsed.items()}  # parsed from .sql
        for k in namespace_overlap_with_config:
            attr = current_namespace[k]
            attr_value = attr() if isinstance(attr, Callable) else attr
            if attr_value:
                attrs[k] = attr_value
        return attrs

    def trim(self) -> str:
        """Statement as a string including only the sql and a single-line tag name.

        note:
            The tag name used here will be the user-provided tag from the
            original script or a generated :attr:`Name.nm` if a tag was not
            provided for a given statement.

        """
        patterns = self.sn.cfg.script.patterns
        open_p, close_p = patterns.core.to_open, patterns.core.to_close
        return f"{open_p}{self.nm}{close_p}\n{self.sql};\n"

    def render(self) -> Statement:
        """Renders the statement's sql as markdown in Notebook/IPython environments."""
        display((Markdown(self.as_section().sql_md)))
        return self

    @property
    def is_derived(self):
        """Indicates whether or not it's a generic or derived (QA) statement."""
        return self.anchor in self.sn.cfg.QA_ANCHORS

    @property
    def lines(self) -> int:
        """Depth of the statement's sql by number of lines."""
        return len(self.sql.split("\n"))

    def as_section(self, incl_raw: Optional[bool] = None) -> Section:
        """Returns current statement as a :class:`Section` object."""
        return Section(
            index=self.index,
            h_contents=self.nm,
            parsed=self.attrs_total,
            raw=self.attrs_raw,
            sql=self.sql,
            cfg=self.sn.cfg,
            results=self.results,
            incl_raw=incl_raw,
            is_multiline=self.is_multiline,
        )

    def set_state(
        self,
        index: Optional[int] = None,
        ctx_id: Optional[int] = None,
        in_context: Optional[bool] = None,
        filters: dict = None,
    ) -> Statement:
        """Sets current state/context on a statement object.

        Args:
            ctx_id (int):
                Unix timestamp the :meth:`script.filter()` context manager was
                invoked.
            filters (dict):
                Kwargs passed to :meth:`script.filter()`.
            index (int):
                Integer to set as the statement's index position.

        """
        if index:
            self.index = index
        if ctx_id:
            self.e.set(ctx_id=ctx_id)
        if isinstance(in_context, bool):
            self.e.set(in_context=in_context)
        if filters:
            super().scope(**filters)
        return self

    def reset(
        self,
        index: bool = False,
        ctx_id: bool = False,
        in_context: bool = False,
        scope: bool = False,
    ) -> Statement:
        """Resets attributes on the statement object to reflect as if read from source.

        In its current form, includes:
            *   Resetting the statement/tag's index to their original values.
            *   Resetting the :attr:`is_included` attribute of the statement's
                :attr:`tag` to `True`.
            *   Populating :attr:`error_last` with errors from current context.
            *   Caching current context's timestamp and resetting back to `None`.

        """
        if index:
            self.index = self._index
        if ctx_id:
            self.e.reset(ctx_id=True)
        if in_context:
            self.e.reset(in_context=True)
        if scope:
            super().scope(**{})
        return self

    def process(self):
        """Used by derived classes for post-processing the returned results."""
        return self

    def run(
        self,
        as_df: bool = True,
        lower: bool = True,
        render: bool = False,
        on_error: Optional[str] = None,
        on_exception: Optional[str] = None,
        on_failure: Optional[str] = None,
        ctx_id: Optional[int] = None,
    ) -> Statement:
        """Run method for all statement objects.

        Args:
            as_df (bool):
                Store results of query as :class:`pandas.DataFrame` or
                :class:`SnowflakeCursor`.
            lower (bool):
                Lower case column names in :attr:`results` DataFrame if
                `as_df=True`.
            render (bool):
                Render the sql executed as markdown.
            on_error (str):
                Behavior if an execution/database error is encountered
                    * `None`: default behavior, exception will be raised
                    * `c`: continue with execution
            on_exception (str):
                Behavior if an exception is raised in the **post-processing**
                of results from a derived class of :class:`Statement` (
                :class:`Empty` and :class:`Diff`).
                    * `None`: default behavior, exception will be raised
                    * `c`: continue with execution
            on_failure (str):
                Behavior if no error is encountered in execution or post-processing
                but the result of the post-processing has turned the statement's
                :attr:`outcome` attribute to False, indicating the results
                returned by the statement have failed validation.
                    * `None`: default behavior, exception will be raised
                    * `c`: continue with execution

        Returns (Statement):
            Statement object post-executing query.

        """

        self.e.set(ctx_id=(ctx_id or -1))
        try:
            if self:
                self.start()
                self.results = self.sn.query(self.sql, as_df=as_df, lower=lower)
                self.end()
                self.e.set(outcome=2)

        except (ProgrammingError, pdDataBaseError, DatabaseError) as e:
            self.e.collect(e=e).set(outcome=1)

        finally:  # only post-process when execution did not raise database error
            if self.e.outcome != 1:
                self.process()
        # fmt: off

        # ---------------------------
        if (
            self.e.seen(             # db error raised during execution
                of_type=errors.db_errors, to_raise=True
            )
            and on_error != "c"      # stop on execution error
        ):
            raise self.e.get(
                of_type=errors.db_errors,
                to_raise=True,
                first=True,
            )
        # ---------------------------
        if (
            self.e.seen(             # post-processing error occurred
                of_type=errors.StatementPostProcessingError,
                to_raise=True,
            )
            and on_exception != "c"  # stop on post-processing exception
        ):
            raise self.e.get(
                of_type=errors.StatementPostProcessingError,
                to_raise=True,
                first=True,
            )
        # ---------------------------
        if (
            self.is_derived        # is child class with `.process()` method
            and not self.outcome   # outcome of `.process()` did not pass
            and on_failure != "c"  # stop on failure of `.process()`
        ):
            raise self.e.get(
                of_type=list(self._DERIVED_FAILURE_MAPPING.values()),
                to_raise=True,
                first=True,
            )
        # ---------------------------
        # fmt: on

        if render:
            self.render()

        return self

    def set_sql(self, sql: str) -> None:
        """Public entry point to manually set the statement's .sql attribute."""
        self._sql = sql

    @staticmethod
    def _validate_parsed(attrs_parsed: Dict):
        """Returns args to verify 'name' attribute is present in a multiline tag."""
        condition, msg = (
            attrs_parsed.get("name"),
            f"Required attribute 'name' not found in multi-line tag's "
            f"arguments;\n attributes found are: {','.join(list(attrs_parsed))}",
        )
        return condition, msg

    def outcome_txt(self, _id: Optional[int] = None) -> str:
        """Outcome as a string."""
        return self._PROCESS_OUTCOMES[_id or self.e.outcome or 0][1]

    @property
    def outcome_html(self) -> str:
        """Outcome as an html admonition banner."""
        # TODO: Move this to patterns
        alert = self._PROCESS_OUTCOMES[self.e.outcome or 0][0]
        return f"""
<div class="alert-{alert}">
<center><b>====/ {self.outcome_txt()} /====</b></center>
</div>""".strip()

    def __bool__(self):
        """Determined by the value of :attr:`Name.is_included`."""
        return self.is_included

    def __str__(self) -> str:
        return f"Statement('{self.nm}')"

    def __repr__(self) -> str:
        return f"Statement('{self.nm}')"
