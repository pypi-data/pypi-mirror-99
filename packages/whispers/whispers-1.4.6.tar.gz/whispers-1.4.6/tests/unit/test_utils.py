import json
from pathlib import Path

import pytest

from tests.unit.conftest import FIXTURE_PATH, fixture_path, rule_path
from whispers import core
from whispers.cli import parse_args
from whispers.utils import (
    Secret,
    find_line_number,
    format_secret,
    format_stdout,
    line_begins_with_value,
    line_with_key_value,
    line_with_value,
    load_yaml_from_file,
    secret_checksum,
    similar_strings,
    simple_string,
    strip_string,
    truncate_all_space,
)


@pytest.mark.parametrize(
    ("rawstr", "expected"),
    [
        ("", ""),
        ("whis\npers", "whis pers"),
        ("whis\tpers", "whis pers"),
        ("whis\n\n\n\npers", "whis pers"),
        ("whis\n       pers", "whis pers"),
    ],
)
def test_truncate_all_space(rawstr, expected):
    assert truncate_all_space(rawstr) == expected


@pytest.mark.parametrize(
    "rawstr",
    [
        "'whispers'",
        "\"'whispers'\"",
        "''whispers\"",
        "whispers\n\n",
        "\t\twhispers",
        "whispers\r\n",
        '    \t\'whispers""\r\n',
    ],
)
def test_strip_string(rawstr):
    assert strip_string(rawstr) == "whispers"


@pytest.mark.parametrize(
    ("rawstr", "expectation"),
    [
        (None, ""),
        (1, "1"),
        ("~|wHisP3R5~|", "__whisp3r5__"),
    ],
)
def test_simple_string(rawstr, expectation):
    assert simple_string(rawstr) == expectation


@pytest.mark.parametrize(
    ("str1", "str2"),
    [
        ("whispers", "WHISPERS!!!"),
        ("W h  I S P e r s", "WHISPERS!!!"),
        pytest.param("AAAAAAA", "WHISPERS!!!", marks=pytest.mark.xfail),
    ],
)
def test_similar_strings(str1, str2):
    assert similar_strings(str1, str2)


@pytest.mark.parametrize(
    ("key", "value", "line"),
    [
        ("key", "value", "key=value"),
        ("key", "value", "{'key': 'value'}"),
        ("key", "value", "key -> value"),
        pytest.param("key", "value", "key=", marks=pytest.mark.xfail),
        pytest.param("key", "value", "{'key':", marks=pytest.mark.xfail),
        pytest.param("key", "value", "key ->", marks=pytest.mark.xfail),
    ],
)
def test_line_with_key_value(key, value, line):
    assert line_with_key_value(key, value, line)


@pytest.mark.parametrize(
    ("value", "line"),
    [
        ("value", "key=value"),
        ("value", "{'key': 'value'}"),
        ("value", "key -> value"),
        pytest.param("value", "key", marks=pytest.mark.xfail),
        pytest.param("value", "vaLUe", marks=pytest.mark.xfail),
    ],
)
def test_line_with_value(value, line):
    assert line_with_value(value, line)


@pytest.mark.parametrize(
    ("value", "line"),
    [
        ("value", "Value"),
        ("value", "'value'"),
        ("value", "\t\tvalue"),
        pytest.param("value", "---Value", marks=pytest.mark.xfail),
        pytest.param("value", "key=value", marks=pytest.mark.xfail),
        pytest.param("value", "\r\nvalue-2", marks=pytest.mark.xfail),
    ],
)
def test_line_begins_with_value(value, line):
    assert line_begins_with_value(value, line)


@pytest.mark.parametrize(
    ("src", "key", "value", "expectation"),
    [
        ("apikeys.yml", "", "", 0),
        ("apikeys.yml", "apikey", "", 0),
        ("apikeys.yml", "", "YXNkZmZmZmZm_HARDcoded", 11),
        ("apikeys.yml", "apikey", "YXNkZmZmZmZm_HARDcoded", 11),
        ("apikeys.yml", "GITHUBKEY", "YXNkZmZmZmZm_HARDcoded", 19),
        ("pip.conf", "username", "hardcoded1", 7),
    ],
)
def test_find_line_number_single(src, key, value, expectation):
    assert find_line_number(FIXTURE_PATH.joinpath(src), key, value, []) == expectation


@pytest.mark.parametrize(
    ("src", "linenumbers"),
    [("hardcoded.yml", [12, 14, 15, 16, 19]), ("privatekeys.yml", [5, 7, 11, 12, 13, 14])],
)
def test_find_line_number_all(src, linenumbers):
    args = parse_args([fixture_path(src)])
    secrets = core.run(args)
    for number in linenumbers:
        assert next(secrets).line == number


@pytest.mark.parametrize(
    ("rulefile", "expected_count"),
    [("empty.yml", 0), ("valid.yml", 1), ("multiple.yml", 4), ("invalid.yml", 0)],
)
def test_load_yaml_from_file(rulefile, expected_count):
    rulefile = Path(rule_path(rulefile))
    assert len(load_yaml_from_file(rulefile)) == expected_count


def test_secret_checksum():
    secret = Secret("file", 123, "key", "value", "message", "severity")
    assert secret_checksum(secret) == "6370fb4455c053420588d92bd292d371"


def test_format_secret():
    secret = Secret("file", 123, "key", "value", "message", "severity")
    assert format_secret(secret) == (
        "6370fb4455c053420588d92bd292d371:\n  "
        + 'file: "file"\n  line: "123"\n  key: "key"\n  '
        + 'value: "value"\n  message: "message"\n  severity: "severity"\n\n'
    )


def test_format_stdout():
    secret = Secret("file", 123, "key", "value", "message", "severity")
    secret_str = json.dumps(secret._asdict())
    assert format_stdout(secret) == secret_str
