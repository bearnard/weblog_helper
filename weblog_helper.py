#!/usr/bin/env python
import re
import sys
import argparse

import requests

LINE_REGEX = re.compile(
   r'([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" "(.*?)"')


def parse_apache_log(line):
    result = re.match(LINE_REGEX, line)
    if result:
        return result.groups()


# Support both web urls and local files.
def stream_logs(stream):
    if re.match("http[s]?://", stream):
        return url_stream_logs(stream)
    return file_stream_logs(stream)


# Log files could be large, lets stream them so we don't have
# to wait for or download the whole file.
def url_stream_logs(url):
    req = requests.get(url, stream=True)
    if req.status_code != 200:
        raise Exception(
            'Unable to stream logs from: {} status code: {}'.format(
                url, req.status_code))
    for line_bytes in req.iter_lines():
        line = str(line_bytes, 'utf-8')
        yield line.strip(), parse_apache_log(line)


# If we happen to have the log file on a filesystem.
# Also here we generate lines to avoid loading the whole file
# into memory.
def file_stream_logs(path):
    with open(path, 'r') as fh:
        for line in fh:
            yield line.strip(), parse_apache_log(line)


# A simple ip filter to match the exact ip.
def ip_filter(log, ip):
    if ip is None or log[0] == ip:
        return True
    return False


# Iterate through the stream of logs and
# only print logs that the filter function allows.
def filter_logs(stream, filter_value, filter_func):
    for line, log in stream_logs(stream):
        if filter_func(log, filter_value):
            print(line)


def build_cli_parser():
    parser = argparse.ArgumentParser(description='Filter some apache logs.')
    parser.add_argument(
        'stream', help='URL of log source or path to log file.')
    return parser


def cli():
    parser = build_cli_parser()
    parser.add_argument('--ip', help='Filter logs by single ip address.')
    args = parser.parse_args()
    filter_logs(args.stream, args.ip, ip_filter)


if __name__ == '__main__':
    cli()
