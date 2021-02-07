from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from src.analyzer import Analyzer, DATE_FORMAT


@pytest.fixture
@patch('src.analyzer.Analyzer._get')
def analyzer_patched(mock_get):
    a = Analyzer('test')
    a._get = mock_get
    return a


@pytest.fixture
def analyzer():
    return Analyzer('test')


@pytest.fixture
def contributors_resp():
    now = datetime.now()
    _32_ago = now - timedelta(days=32)
    return [
        {
            'author': {
                'login': 'test-1'
            },
            'commit': {
                'author': {
                    'date': now.strftime(DATE_FORMAT)
                }
            }
        }, {
            'author': {
                'login': 'test-1'
            },
            'commit': {
                'author': {
                    'date': _32_ago.strftime(DATE_FORMAT)
                }
            }
        },
        {
            'author': {
                'login': 'test-2'
            },
            'commit': {
                'author': {
                    'date': now.strftime(DATE_FORMAT)
                }
            }
        },
    ]


@pytest.fixture
def prs_issues():
    now = datetime.now()
    _32_ago = now - timedelta(days=32)
    _15_ago = now - timedelta(days=15)
    return [
        {
            'state': 'open',
            'created_at': now.strftime(DATE_FORMAT)
        },
        {
            'state': 'open',
            'created_at': _32_ago.strftime(DATE_FORMAT)
        },
        {
            'state': 'open',
            'created_at': _15_ago.strftime(DATE_FORMAT)
        },
        {
            'state': 'closed',
            'created_at': now.strftime(DATE_FORMAT)
        },
        {
            'state': 'closed',
            'created_at': _32_ago.strftime(DATE_FORMAT)
        },
        {
            'state': 'closed',
            'created_at': _15_ago.strftime(DATE_FORMAT)
        },
    ]
