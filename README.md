![Deprecated](https://img.shields.io/badge/deprecated-red?style=flat-square)
![GitLab CI](https://img.shields.io/badge/GitLab%20CI-%23181717.svg?style=flat-square&logo=gitlab&logoColor=white)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydocstyle-gitlab-code-quality?style=flat-square)
[![PyPI - License](https://img.shields.io/pypi/l/pydocstyle-gitlab-code-quality?style=flat-square)](LICENSE.md)
[![PyPI](https://img.shields.io/pypi/v/pydocstyle-gitlab-code-quality?style=flat-square)](https://pypi.org/project/pydocstyle-gitlab-code-quality/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pydocstyle-gitlab-code-quality?style=flat-square)

# pydocstyle-gitlab-code-quality

Generate [GitLab Code Quality report](https://docs.gitlab.com/ee/ci/testing/code_quality.html) from an output of [pydocstyle](https://github.com/PyCQA/pydocstyle).

## Deprecation notice!

> [!IMPORTANT]
> The `pydocstyle-gitlab-code-quality` is no longer actively maintained, because `pydocstyle` has been officialy deprecated in favor of [Ruff](https://github.com/astral-sh/ruff).

## Usage

```bash
# passing pydocstyle output through stdin (output printed to stdout)
pydocstyle main.py | pydocstyle-gitlab-code-quality > codequality.json
# or
pydocstyle-gitlab-code-quality < pydocstyle_out.txt > codequality.json

# using CLI flags (output printed directly to a file)
pydocstyle-gitlab-code-quality --input pydocstyle_out.txt --output codequality.json
```

## CLI configuration

`pydocstyle-gitlab-code-quality` allows for the following CLI arguments:

| flag                         | example                 | default           | description                                                   |
| ---------------------------- | ----------------------- | ----------------- | ------------------------------------------------------------- |
| `--minor <CODE>...`          | `--minor=D100,D101`     | *empty*           | Error codes to be displayed with MINOR severity.              |
| `--major <CODE>...`          | `--major=D102,D103`     | *empty*           | Error codes to be displayed with MAJOR severity.              |
| `--critical <CODE>...`       | `--critical=D104,D105`  | *empty*           | Error codes to be displayed with CRITICAL severity.           |
| `-i, --ignore <CODE>...`     | `--ignore=D106,D107`    | *empty*           | Error codes to be omitted from Code Quality report.           |
| `-f, --file, --input <FILE>` | `-f pydocstyle_out.txt` | *empty*           | Path to the file with pydocstyle output.                      |
| `-o, --output <FILE>`        | `-o codequality.json`   | *empty*           | Path to the file where the Code Quality report will be saved. |
| `--no-stdout`                | N/A                     | `False`           | Do not print the Code Quality report to stdout.               |
| `--log-file <FILE>`          | `--log-file latest.log` | `pgcq_latest.log` | Path to the file where the log will be saved.                 |
| `--enable-logging`           | N/A                     | `False`           | Enable logging to a file. For debugging purposes only.        |

By default, all error codes are reported with INFO severity.

In case the same error code from `pydocstyle` has been provided to many severity options, the highest severity level takes precedence.

### Example `.gitlab-ci.yml` file

```yaml
image: python:alpine
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/
    - venv/

before_script:
  - python --version  # For debugging
  - python -m venv venv
  - . venv/bin/activate

codequality:
  script:
    - pip install pydocstyle pydocstyle-gitlab-code-quality
    - pydocstyle program.py > pydocstyle-out.txt
    - pydocstyle-gitlab-code-quality --input pydocstyle-out.txt --output codequality.json
  artifacts:
    when: always
    reports:
      codequality: codequality.json
  allow_failure: true
```

## Credits

This script was inspired by [mypy-gitlab-code-quality](https://github.com/soul-catcher/mypy-gitlab-code-quality). Thanks!

## License

The project is licensed under MIT - a free and open-source license. For more information, please see [the license file](LICENSE.md).
