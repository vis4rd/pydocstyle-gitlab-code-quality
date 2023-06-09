![GitLab CI](https://img.shields.io/badge/GitLab%20CI-%23181717.svg?style=flat-square&logo=gitlab&logoColor=white)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydocstyle-gitlab-code-quality?style=flat-square)
[![PyPI - License](https://img.shields.io/pypi/l/pydocstyle-gitlab-code-quality?style=flat-square)](LICENSE.md)
[![PyPI](https://img.shields.io/pypi/v/pydocstyle-gitlab-code-quality?style=flat-square)](https://pypi.org/project/pydocstyle-gitlab-code-quality/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pydocstyle-gitlab-code-quality?style=flat-square)

# pydocstyle-gitlab-code-quality

Generate [GitLab Code Quality report](https://docs.gitlab.com/ee/ci/testing/code_quality.html) from an output of [pydocstyle](https://github.com/PyCQA/pydocstyle).

## Usage

```bash
$ pydocstyle <file_path> | PYTHONHASHSEED=0 pydocstyle-gitlab-code-quality
```

The output of this command is printed to `stdout` in JSON format, which can be used as Code Quality report.

Environment variable `PYTHONHASHSEED=0` prevents randomized hashes, which are used by GitLab to determine changes between branches on merge request.

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
    - PYTHONHASHSEED=0 pydocstyle-gitlab-code-quality < pydocstyle-out.txt > codequality.json
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
