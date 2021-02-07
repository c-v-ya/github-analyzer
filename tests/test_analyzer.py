from datetime import datetime, timedelta
from unittest.mock import patch


def test_contribs(analyzer_patched, contributors_resp):
    analyzer_patched._get.return_value = contributors_resp
    contributors = analyzer_patched.get_contributors()

    assert len(contributors) == 2
    assert contributors.get('test-1') == 2


def test_contribs_date_from(analyzer_patched, contributors_resp):
    analyzer_patched.date_from = datetime.now() - timedelta(hours=2)
    analyzer_patched._get.return_value = contributors_resp
    contributors = analyzer_patched.get_contributors()

    assert len(contributors) == 2
    assert contributors.get('test-1') == 1
    assert contributors.get('test-2') == 1


def test_contribs_date_to(analyzer_patched, contributors_resp):
    analyzer_patched.date_to = datetime.now() - timedelta(days=10)
    analyzer_patched._get.return_value = contributors_resp
    contributors = analyzer_patched.get_contributors()

    assert len(contributors) == 1
    assert contributors.get('test-1') == 1
    assert contributors.get('test-2') is None


def test_contribs_date_from_to_includes(analyzer_patched, contributors_resp):
    analyzer_patched.date_from = datetime.now() - timedelta(days=60)
    analyzer_patched.date_to = datetime.now() - timedelta(days=10)
    analyzer_patched._get.return_value = contributors_resp
    contributors = analyzer_patched.get_contributors()

    assert len(contributors) == 1
    assert contributors.get('test-1') == 1
    assert contributors.get('test-2') is None


def test_contribs_date_from_to_empty(analyzer_patched, contributors_resp):
    analyzer_patched.date_from = datetime.now() - timedelta(days=160)
    analyzer_patched.date_to = datetime.now() - timedelta(days=120)
    analyzer_patched._get.return_value = contributors_resp
    contributors = analyzer_patched.get_contributors()

    assert len(contributors) == 0
    assert contributors.get('test-1') is None
    assert contributors.get('test-2') is None


def test_process_prs(analyzer_patched, prs_issues):
    analyzer_patched._process(prs_issues, 'pr')
    prs = analyzer_patched.prs

    assert len(prs) == 3
    assert prs.get('open') == 3
    assert prs.get('old') == 1


def test_process_issues(analyzer_patched, prs_issues):
    analyzer_patched._process(prs_issues, 'issue')
    issues = analyzer_patched.issues

    assert len(issues) == 3
    assert issues.get('open') == 3
    assert issues.get('old') == 2


def test_process_date_from(analyzer_patched, prs_issues):
    analyzer_patched.date_from = datetime.now() - timedelta(days=20)
    analyzer_patched._process(prs_issues, 'pr')
    prs = analyzer_patched.prs

    assert len(prs) == 2
    assert prs.get('open') == 2
    assert prs.get('old') is None


def test_process_date_to(analyzer_patched, prs_issues):
    analyzer_patched.date_to = datetime.now() - timedelta(days=20)
    analyzer_patched._process(prs_issues, 'pr')
    prs = analyzer_patched.prs

    assert len(prs) == 3
    assert prs.get('open') == 1
    assert prs.get('old') == 1


def test_process_date_empty(analyzer_patched, prs_issues):
    analyzer_patched.date_from = datetime.now() - timedelta(days=160)
    analyzer_patched.date_to = datetime.now() - timedelta(days=120)
    analyzer_patched._process(prs_issues, 'pr')
    prs = analyzer_patched.prs

    assert len(prs) == 0
    assert prs.get('open') is None
    assert prs.get('old') is None


@patch('src.analyzer.Analyzer._has_limit')
def test_limit_exceeded(mock_limit, analyzer, caplog):
    mock_limit.return_value = False
    stats = analyzer.get_stats()

    assert 'Limit exceeded' in caplog.text
    assert len(stats) == 3
    assert len(stats.get('contributors')) == 0
    assert len(stats.get('prs')) == 0
    assert len(stats.get('issues')) == 0
