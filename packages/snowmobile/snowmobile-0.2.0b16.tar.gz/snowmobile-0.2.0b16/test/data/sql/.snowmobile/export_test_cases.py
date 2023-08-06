"""
This file exists for the sole purpose of exporting different configurations of
markup_ddl.sql for testing purposes.

The relative 'markup_ddl.sql' path below assumes that this script is stored
within 'tests/func/data/sql/markup/.snowmobile' directory.
"""
from pathlib import Path
from typing import List, Dict, Tuple
import snowmobile


def get_testing_script(nm: str, results_limit: int = 1):
    path = Path(__file__).absolute().parent.parent / nm
    sn = snowmobile.connect(delay=True, config_file_nm="snowmobile_testing.toml")
    sn.cfg.script.markup.result_limit = results_limit
    return snowmobile.Script(path=path, sn=sn)


def export_markups(script_dtl: List[Tuple[str, bool, Dict]], args: List[Dict]):
    for s in script_dtl:
        script_nm, run, run_kwargs = s
        script = get_testing_script(nm=script_nm)
        if run:
            script.run(**run_kwargs)
        for arg in args:
            doc = script.doc()(**arg["config"])
            doc.save(**arg["save"])


args = [
    {"config": {"alt_file_prefix": "(default) "}, "save": {}},
    {"config": {"alt_file_prefix": "(no sql) "}, "save": {"md_only": True}},
    {
        "config": {"incl_markers": False, "alt_file_prefix": "(no markers) "},
        "save": {},
    },
    {
        "config": {
            "incl_markers": False,
            "sql_incl_export_disclaimer": False,
            "alt_file_prefix": "(no disclaimer, no markers) ",
        },
        "save": {"sql_only": True},
    },
]


script_dtl = [
    ("markup_no_results.sql", False, {}),
    ("markup_with_results.sql", True, {"on_failure": "c"}),
    ("markup_template_anchor.sql", False, {}),
]

export_markups(script_dtl=script_dtl, args=args)
