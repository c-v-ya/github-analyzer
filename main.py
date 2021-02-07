import argparse
import json
import logging
from datetime import datetime

from requests import RequestException

from src.analyzer import Analyzer

log = logging.getLogger(__name__)


def valid_date(date_str: str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        msg = f'Invalid date format for {date_str}. Must be YYYY-MM-DD'
        raise argparse.ArgumentTypeError(msg)


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        'repo', type=str,
        help='GitHub public repo',
    )
    arg_parser.add_argument(
        '-df', '--date_from', type=valid_date,
        help='Analyze from date - YYYY-MM-DD',
    )
    arg_parser.add_argument(
        '-dt', '--date_to', type=valid_date,
        help='Analyze to date - YYYY-MM-DD',
    )
    arg_parser.add_argument(
        '-b', '--branch', type=str, default='master',
        help='Branch name to analyze. Defaults to master',
    )

    args = arg_parser.parse_args()

    repo = args.repo
    date_from = args.date_from
    date_to = args.date_to
    branch = args.branch

    analyzer = Analyzer(
        repo=repo,
        date_from=date_from,
        date_to=date_to,
        branch=branch,
    )

    result = {}
    try:
        result = analyzer.get_stats()
    except RequestException as e:
        log.error(f'Error getting stats: {e}')

    log.info(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
