import logging
from collections import defaultdict
from datetime import datetime
from functools import cached_property, wraps
from typing import Literal

import requests

from src import config

log = logging.getLogger(__name__)
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def if_allowed():
    """Allows to process request only if limit is not exceeded"""

    def inner(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._has_limit():
                return func(self, *args, **kwargs)
            else:
                log.error('Limit exceeded, try again later')

        return wrapper

    return inner


class Analyzer:
    def __init__(
            self,
            repo: str,
            date_from: datetime = None,
            date_to: datetime = None,
            branch: str = 'master'
    ):
        self.repo = repo
        self.date_from = date_from
        self.date_to = date_to
        self.branch = branch

        self.contributors = defaultdict(int)
        self.prs = defaultdict(int)
        self.issues = defaultdict(int)

    def _has_limit(self):
        response = self.session.get(f'{config.BASE_URL}/rate_limit')
        response.raise_for_status()
        limit = response.json().get('rate', {}).get('remaining')
        return limit > 0

    @cached_property
    def session(self):
        session = requests.Session()
        session.headers['Authorization'] = f'token {config.TOKEN}'
        return session

    @if_allowed()
    def _get(self, url, **params) -> list:
        response = self.session.get(
            f'{config.BASE_URL}/repos/{self.repo}{url}',
            params=params
        )
        response.raise_for_status()

        return response.json()

    def get_stats(self):
        contributors = self.get_contributors()
        prs = self.get_prs()
        issues = self.get_issues()

        return {
            'contributors': contributors,
            'prs': prs,
            'issues': issues,
        }

    def get_contributors(self):
        since = self._format_date(self.date_from)
        until = self._format_date(self.date_to)
        data = self._get(
            '/commits',
            sha=self.branch,
            since=since,
            until=until
        )
        for item in data or []:
            author = item.get('author')
            if not author:
                continue

            commit = item.get('commit')
            if not commit:
                continue

            commit_date_str = commit.get('author', {}).get('date')
            if not commit_date_str:
                continue

            commit_date = datetime.strptime(commit_date_str, DATE_FORMAT)

            if (not self._date_in_range(commit_date)
                    or len(self.contributors) > config.CONTRIBUTORS_LENGTH):
                continue

            self.contributors[author.get('login')] += 1

        return dict(
            sorted(
                self.contributors.items(),
                key=lambda record: record[1],
                reverse=True
            )
        )

    def get_prs(self, page=1):
        data = self._get(
            '/pulls',
            base=self.branch,
            sort='created',
            direction='desc',
            page=page,
        )

        has_next = self._process(data, 'pr')
        if has_next:
            self.get_prs(page + 1)

        return self.prs

    def get_issues(self, page=1):
        data = self._get(
            '/issues',
            sort='created',
            direction='desc',
            page=page,
        )

        has_next = self._process(data, 'issue')
        if has_next:
            self.get_issues(page + 1)

        return self.issues

    def _process(self, data: list, to_count: Literal['pr', 'issue']):
        if to_count == 'pr':
            old_days = config.OLD_PR_DAYS
            storage = self.prs
        elif to_count == 'issue':
            old_days = config.OLD_ISSUE_DAYS
            storage = self.issues
        else:
            raise ValueError(
                f'Invalid param to count: {to_count}, expected pr or issue'
            )

        for item in data or []:
            date_opened_str = item.get('created_at')
            if not date_opened_str:
                continue
            date_opened = datetime.strptime(date_opened_str, DATE_FORMAT)
            if not self._date_in_range(date_opened):
                continue

            item_state = item.get('state')
            if item_state == 'open':
                storage['open'] += 1
                start_date = self.date_from or datetime.now()
                if (start_date - date_opened).days > old_days:
                    storage['old'] += 1
            elif item_state == 'closed':
                storage['closed'] = + 1

        has_next = False
        if data:
            date_opened_str = data[0].get('created_at')
            if date_opened_str:
                date_opened = datetime.strptime(date_opened_str, DATE_FORMAT)
                if self._date_in_range(date_opened):
                    has_next = True

        return has_next

    @staticmethod
    def _format_date(date: datetime):
        return date.strftime(DATE_FORMAT) if date else None

    def _date_in_range(self, date):
        if self.date_from and not self.date_to:
            return date > self.date_from
        elif not self.date_from and self.date_to:
            return date < self.date_to
        elif self.date_from and self.date_to:
            return self.date_from < date < self.date_to
        else:
            return True
