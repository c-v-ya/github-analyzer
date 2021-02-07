# GitHub Analyzer

Analyzes GitHub repository for top 30 active contributors, opened and old pull requests and issues.
PR is considered old if it's open for more than 30 days.
Issue is considered old if it's open for more than 14 days.

Those numbers are configurable via `config.py`.

## Prerequisites

Set `TOKEN` environment variable as in `.env.example`.

## Example Output

```shell
2021-02-07 00:00:00,000 - INFO     __main__     main:52 - {
  "contributors": {
    "rogerluan": 7,
    "joshdholtz": 4,
    "DavidBrunow": 2,
    "ainame": 2,
    "nimau": 1,
    "felginep": 1,
    "sanzaru": 1,
    "sztwiorok": 1,
    "gsavit": 1,
    "yunhao": 1,
    "kohtenko": 1,
    "jgongo": 1,
    "fstaine": 1,
    "johndbritton": 1,
    "krish722": 1,
    "everlof": 1,
    "tbodt": 1,
    "Econa77": 1,
    "thilek": 1
  },
  "prs": {
    "open": 73,
    "old": 49
  },
  "issues": {
    "open": 173,
    "old": 135
  }
}
```

## Usage

### Shell

```shell
$ python main.py -h
usage: main.py [-h] [-df DATE_FROM] [-dt DATE_TO] [-b BRANCH] repo

positional arguments:
  repo                  GitHub public repo

optional arguments:
  -h, --help            show this help message and exit
  -df DATE_FROM, --date_from DATE_FROM
                        Analyze from date - YYYY-MM-DD
  -dt DATE_TO, --date_to DATE_TO
                        Analyze to date - YYYY-MM-DD
  -b BRANCH, --branch BRANCH
                        Branch name to analyze. Defaults to master
```

### Docker

First build an image with `docker build . -t analyzer`.

Create `.env` file, use `.env.example` for the reference.

Run `docker run --rm --env-file .env --name analyzer analyzer fastlane/fastlane`.