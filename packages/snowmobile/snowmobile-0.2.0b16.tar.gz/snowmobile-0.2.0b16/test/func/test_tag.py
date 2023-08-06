"""
Tests for tag parsing.
"""
import pytest

from test import script as get_script


# noinspection PyProtectedMember
def _setup_for_test_tag_from_stripped_line():
    """Gets test cases and generates IDs for statement tags."""
    # get script with tag test cases
    script = get_script(script_name="no_tags.sql")

    # remove index from generated tag
    for s in script._statements_all.values():
        s.incl_idx_in_desc = False

    # generate test cases
    test_cases = [(s.nm_ge, s.nm_pr) for s in script.statements.values()]

    # generate IDs test cases/console output
    # ids = [
    #     f"FirstLine='{s.first_line}',Name='{s.nm}'" for s in script.statements.values()
    # ]
    ids = [
        f"nm_ge='{t[1]}', nm_pr='{t[0]}'"
        for t in test_cases
    ]

    return ids, test_cases


ids, test_cases = _setup_for_test_tag_from_stripped_line()


@pytest.mark.names
@pytest.mark.parametrize("tags", test_cases, ids=ids)
def test_tag_from_stripped_line(sn, tags):
    """Testing tag generation from sql statements in no_tags.sql."""
    tag_generated, tag_expected = tags
    assert tag_generated == tag_expected


@pytest.fixture()
def a_sample_tag(sn):
    """Testing __setattr__ on Name.."""
    from snowmobile.core.name import Name

    # noinspection SqlResolve
    return Name(
        configuration=sn.cfg,
        nm_pr="test-tag",
        sql="select * from sample_table",
        index=1,
    )


@pytest.mark.names
def test_set_item_on_tag(a_sample_tag):
    """Testing __setattr__ and __bool__ on Name.."""
    a_sample_tag.is_included = False
    a_sample_tag.__setitem__("is_included", False)
    assert not a_sample_tag.is_included
    assert not a_sample_tag


@pytest.mark.names
def test_repr_on_tag(a_sample_tag):
    """Testing __repr__ on Name.."""
    assert a_sample_tag.__repr__() == "statement.Name(nm='test-tag')"
