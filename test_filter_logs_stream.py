import pytest


from weblog_helper import filter_logs, file_stream_logs, ip_filter


@pytest.fixture
def valid_log_filtered_output():
    return (
        '106.208.0.17 - - [03/Jun/2015:08:26:52 -0700] '
        '"GET /pdf/che_sos.pdf HTTP/1.1" 200 207560 '
        '"https://www.google.co.in/" '
        '"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.95 Safari/537.36" "redlug.com"\n'
        '106.208.0.17 - - [03/Jun/2015:08:26:58 -0700] '
        '"GET /pdf/che_sos.pdf HTTP/1.1" 206 32768 '
        '"http://redlug.com/pdf/che_sos.pdf" "Mozilla/5.0 '
        '(Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.95 Safari/537.36" "redlug.com"\n')


def test_filter_logs_output_valid(capfd,  valid_log_filtered_output):
    filter_logs('test_data/stream.sample.log', '106.208.0.17', ip_filter)
    out, _ = capfd.readouterr()
    assert out == valid_log_filtered_output
