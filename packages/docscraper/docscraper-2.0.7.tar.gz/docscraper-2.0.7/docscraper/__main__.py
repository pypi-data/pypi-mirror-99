#!/usr/bin/env python3
import argparse
from .api import crawl


def check_times(t):
    """ Check time range to confirm 1 or 2 values provided.

    :param t: time range tuple
    :type t: tuple
    """
    if 1 > len(t) > 2:
        raise argparse.ArgumentTypeError('Times should have at least 1 '
                                         'argument but not more than 2.')
    return


def parse_arguments():
    """ Parse and return command-line arguments.
    :return: An argparse namespace object containing the command-line
    argument values.
    :rtype: argparse.Namespace

    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--domains', nargs='+',
                        help='one or more allowed domains', required=True)

    parser.add_argument('-s', '--start_urls', nargs='+',
                        help='one or more start urls', required=True)

    parser.add_argument('-o', '--outpath', help='directory path for output.',
                        default='./output')

    parser.add_argument('-e', '--extensions', nargs='*',
                        help='one or more document extensions (e.g., ".pdf")')

    parser.add_argument('-t', '--times', nargs='?',
                        type=check_times,
                        help='one or two timestamps in YYYYmmddHHMMSS format')

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_arguments()

    if args.extensions is None:
        args.extensions = ['.pdf', '.doc', '.docx']

    if len(args.times) == 1:
        args.times = args.times[0]

    crawl(args.domains, args.start_urls,
          args.outpath, args.extensions, args.times)

