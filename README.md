# `weblog_helper` - A helper script to filter apache logs by ip.

## Features:
* Stream logs from an http/https endpoint or file on a filesystem.
* Filter logs by IP or CIDR.
* Extendable.

## Usage:

```
usage: weblog_helper.py [-h] [--ip IP] stream

Filter some apache logs.

positional arguments:
  stream      URL of log source

optional arguments:
  -h, --help  show this help message and exit
  --ip IP     Filter logs by ip
```

## Extending:
Part 2 asks for `CIDR` support to be added to the `--ip` arg.
Of course that can easily be done by looking for a `/` and then switching logic to test for CIDR ranges.

For illustrative purposes I'll attempt to show how the core functionality of `weblog_helper.py` can be extended/overridden by another script.

See `weblog_helper2.py` 

## Examples:
```
(.env) $ ./weblog_helper.py https://s3.amazonaws.com/syseng-challenge/public_access.log.txt --ip 180.180.230.89
180.180.230.89 - - [03/Jun/2015:08:21:11 -0700] "GET /wp-login.php?action=register HTTP/1.1" 404 88 "http://redlug.com/" "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17" "redlug.com"

(.env) $ ./weblog_helper2.py https://s3.amazonaws.com/syseng-challenge/public_access.log.txt --ip 180.180.230.0/24
180.180.230.89 - - [03/Jun/2015:08:21:11 -0700] "GET /wp-login.php?action=register HTTP/1.1" 404 88 "http://redlug.com/" "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17" "redlug.com"

```

## Tests:

```
(.env) $ pytest -v
========================================================= test session starts ==========================================================
platform darwin -- Python 3.7.2, pytest-4.4.0, py-1.8.0, pluggy-0.9.0 -- .env/bin/python3.7
cachedir: .pytest_cache
rootdir: weblog_helper
collected 7 items

test_ip_cidr_filter.py::test_ip_cidr_filter_true_for_cidr PASSED                                                                 [ 14%]
test_ip_cidr_filter.py::test_ip_cidr_filter_true_for_ip PASSED                                                                   [ 28%]
test_ip_cidr_filter.py::test_ip_cidr_filter_false_for_wrong_ip PASSED                                                            [ 42%]
test_ip_filter.py::test_ip_filter_true_for_exact_match PASSED                                                                    [ 57%]
test_ip_filter.py::test_ip_filter_false_for_wrong_ip PASSED                                                                      [ 71%]
test_parse_apache_log.py::test_parse_valid_apache_log_ip PASSED                                                                  [ 85%]
test_parse_apache_log.py::test_parse_invalid_log PASSED                                                                          [100%]

======================================================= 7 passed in 0.16 seconds =======================================================
```
## Future Improvements:
* Think of more test cases.
* Create an `ApacheLogLine` class with named attributes for each field, i.e `log.remote_ip` instead of `log[0]`
* Support recieving logs via `stdin`
* URL schema support validation.
* Support filtering on other fields.
* Multiple streams, for concurrent filtering.
* Turn parser into a module
* Support for multiple apache log formats