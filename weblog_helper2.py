#!/usr/bin/env python
import iptools

from weblog_helper import build_cli_parser, filter_logs


# A filter function to filter only logs
# with a remote ip field in a CIDR range.
def ip_cidr_filter(log, cidr):
    if cidr is None:
        return True
    cidr = iptools.IpRange(cidr)
    ip = log[0]
    if ip in cidr:
        return True
    return False


def cli():
    parser = build_cli_parser()
    parser.add_argument('--ip', help='Filter logs by CIDR ip range.')
    args = parser.parse_args()
    filter_logs(args.stream, args.ip, ip_cidr_filter)


if __name__ == '__main__':
    cli()
