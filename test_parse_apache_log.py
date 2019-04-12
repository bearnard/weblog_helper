import pytest

from weblog_helper import parse_apache_log


@pytest.fixture
def valid_log_line():
    return ('78.29.246.2 - - [02/Jun/2015:22:13:41 -0700]'
            ' "GET /foo HTTP/1.1" 404 73 "-"'
            ' "Mozilla/4.0 (compatible; MSIE 8.0; Win32)" "redlug.com"')


@pytest.fixture
def invalid_log_line():
    return ('kjhkj 78.29.246.2 - - [02/Jun/2015:22:13:41 -0700]'
            ' "GET /foo HTTP/1.1" 404 73 "-"'
            ' "Mozilla/4.0 (compatible; MSIE 8.0; Win32)" "redlug.com"')


def test_parse_valid_apache_log_ip(valid_log_line):
    log = parse_apache_log(valid_log_line)
    assert log is not None
    assert log[0] == '78.29.246.2'


def test_parse_invalid_log(invalid_log_line):
    log = parse_apache_log(invalid_log_line)
    assert log is None
