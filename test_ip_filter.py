import pytest


from weblog_helper import ip_filter


@pytest.fixture
def log():
    return (
        '69.30.245.58', '02/Jun/2015:19:05:40 -0700',
        'GET /wp-login.php?action=register HTTP/1.1', '404',
        '88', 'http://redlug.com/',
        'Opera/9.80 (Windows NT 6.2; Win64; x64)' +
        'Presto/2.12.388 Version/12.17',
        'redlug.com')


def test_ip_filter_true_for_exact_match(log):
    assert ip_filter(log, '69.30.245.58') is True


def test_ip_filter_false_for_wrong_ip(log):
    assert ip_filter(log, '69.30.245.51') is False


def test_ip_filter_true_none_ip(log):
    assert ip_filter(log, None) is True
