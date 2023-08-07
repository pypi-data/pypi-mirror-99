[<p align="center"><img src="https://github.com/ochronasec/ochrona-cli/raw/master/resources/ochrona_logo.png" width="500"/></p>](https://ochrona.dev)

[![Ochrona](https://img.shields.io/badge/secured_by-ochrona-blue)](https://ochrona.dev)
[![PyPI](https://img.shields.io/pypi/v/ochrona)](https://pypi.org/project/ochrona/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://travis-ci.com/ochronasec/ochrona-cli.svg?token=9JDALtMe5VnkYyLdqiN6&branch=master)](https://travis-ci.com/ochronasec/ochrona-cli)
[![codecov](https://codecov.io/gh/ochronasec/ochrona-cli/branch/master/graph/badge.svg?token=uWNZiXnXto)](https://codecov.io/gh/ochronasec/ochrona-cli)

- [Overview](#overview)
    + [Supported file types](#supported-file-types)
- [Installation](#installation)
    + [via pip](#via-pip)
    + [via pipenv](#via-pipenv)
    + [via poetry](#via-poetry)
- [Configuration](#configuration)
    + [via command line args](#via-command-line-args)
    + [via environment variables](#via-environment-variables)
    + [via .ochrona.yml](#via-ochronayml)
- [Usage Examples](#usage-examples)
    + [Default Mode](#default-mode)
    + [Standard error code with Junit XML reporting saved to file](#standard-error-code-with-junit-xml-reporting-saved-to-file)
    + [Safe Import Mode](#safe-import-mode)
    + [stdin Support](#stdin-support)
      - [Single dependency via stdin](#single-dependency-via-stdin)
      - [Multi-dependency via stdin](#multi-dependency-via-stdin)
    + [Docker Support](#docker-support)
      - [Dockerized Ochrona passing api key](#dockerized-ochrona-passing-api-key)
      - [Dockerized Ochrona with environment variables](#dockerized-ochrona-with-environment-variables)
- [Output Formats](#output-formats)
    + [Basic](#basic)
    + [Full](#full)
    + [XML (Junit)](#xml--junit-)
    + [JSON](#json)
- [Modes of Operation](#modes-of-operation)
- [DADA Support](#dada-support)
- [Represent!](#represent-)

# Overview
This module is the command line tool for accessing Ochrona Security, a solution for validating the dependencies used in python projects.

Ochrona requires a license to operate. We offer a free-tier license which allows up to 25 scans per month. You can [sign up for an API key on our Community plan](https://signup.ochrona.dev) or visit [ochrona.dev](https://ochrona.dev) to learn about our other usage tiers. 

We care deeply about Developer Experience (DX), if you have any feedback or run into issues please open an issue [here](https://github.com/ochronasec/ochrona-cli/issues).

### Supported file types
- `*requirements*.txt`
- `Pipfile.lock`
- `poetry.lock`
- `setup.py`
- `*constraints*.txt`
- `environment.yml`
- `tox.ini`

# Installation

### via pip
```
pip install ochrona
```

### via pipenv
```
pipenv install --dev ochrona
```

### via poetry
```
poetry add -D ochrona
```

# Configuration
### via command line args
| Arg              | Description                                                               | Type | Example                                                                    |
|------------------|---------------------------------------------------------------------------|------|----------------------------------------------------------------------|
| `--api_key`      | Ochrona API Key                                                           | str  | abc123                                                                     |
| `--dir`          | Directory to recursively search for dependencies files to scan [.]        | path | /User/me/my_project                                                        |
| `--exclude_dir`  | Directory names that should be excluded from recursive search. Comma separated   | str | build,dev                                                    |
| `--file`         | Single dependency file to scan                                            | file | /User/me/my_project/requirements.txt                                       |
| `--debug`        | Enable debug logging [False]                                              | bool | True                                                                       |
| `--silent`       | Silent mode [False]                                                       | bool | True                                                                       |
| `--report_type`  | The report type that's desired [BASIC]                                    | str  | XML                                                                        |
| `--output`       | Location for report output                                                | path | /User/me/my_project/logs                                                   |
| `--exit`         | Exit with Code 0 regardless of vulnerability findings. [False]            | bool | True                                                                       |
| `--ignore`       | Ignore a CVE or package                                                   | str  | requests                                                                   |
| `--include_dev`  | Include develop dependencies from Pipfile.lock [False]                    | bool | True                                                                       |
| `--project_name` | The name of your project. Setting this will enable `record` mode.         | str  | My Example Project                                                         |
| `--alert_config` | Alert configuration for use with DADA. This is expressed as a json string | str  | '{"alerting_addresses": "test@ochrona.dev", "alerting_rules": "not:boto3"}'|

### via environment variables
| Variable Name         | Corresponding Arg |
|-----------------------|-------------------|
| OCHRONA_API_KEY       | `--api_key`       |
| OCHRONA_DEBUG_LOGGING | `--debug`         |
| OCHRONA_IGNORED_VULNS | `--ignore`        |

### via .ochrona.yml
There is an empty `.ochrona.yml` file included in the repo. 
| Key | Description | Type | Example |
|-|-|-|-|
| `api_key` | Ochrona API Key | str | abc123 |
| `api_url` | This field can optionally set an alternative analysis url [https://api.ochrona.dev/python/analyze] | str | N/A |
| `alert_url` | For DADA users only, this field can optionally set an alternative alert registration url  [https://api.ochrona.dev/alerts/project-alerts] | str | N/A |
| `dir` | Directory to recursively search for dependencies files to scan [.] | path | /User/me/my_project |
| `exclude_dir` | Directory names that should be excluded from recursive search. | list | build |
| `file` | Single dependency file to scan | file | /User/me/my_project/requirements.txt |
| `debug` | Enable debug logging [false] | bool | true |
| `silent` | Silent mode [false] | bool | true |
| `report_type` | The report type that's desired [BASIC] | str | XML |
| `report_location` | Location for report output [.] | path | /User/me/my_project/logs |
| `exit` | Exit with Code 0 regardless of vulnerability findings [false] | bool | true |
| `ignore` | Ignore a CVE or package name | str | requests |
| `include_dev` | Include develop dependencies from files that support dev/required dependencies [false] | bool | true |
| `color_output` | Whether or not std out text should use color. Note: this is enabled by default when running in a non-Windows environment [true] | bool | false |
| `project_name` | For DADA users only, the name of your project. If using a multi-branched approach it  is recommended to specify the branch name here as well | str | My Example Project |
| `alert_config.alerting_addresses` | For DADA users only, this is the emails that should be notified in the event of a new  vulnerability that impacts the project.  | str | test@ohrona.dev |
| `alert_config.alerting_rules` | For DADA users only, these are the rules that dictate whether an alert should be raised. Valid operators include `not:``package_name` and `severity:`>=`float` | str | not:boto3,severity:>7.0 |

**Example**:
```
# api_key: <your key>
# debug: true
# silent: false
# dir: .
# report_type: JSON
# report_location: .
# ignore: requests
# include_dev: false
# color_output: false
# project_name: my_test_project
# alert_config:
#   alerting_addresses: test@web.com
#   alerting_rules: not:boto3
```

# Usage Examples
### Default Mode
```
$ ochrona 
```
This will search for any supported dependency files recursively from the run location. It will output rules in the `BASIC`
format to stdout. The program will exit with an error exit code if any confirmed vulnerabilities are found.

### Standard error code with Junit XML reporting saved to file
```
$ ochrona --exit --report_type XML --output ./output
```

### Safe Import Mode
In this mode ochrona acts as a safe wrapper around standard pip installs to ensure that a package and it's dependencies are safe before installing. This action preemptively checks a package against the Ochrona API and only imports if no vulnerabilities are found. It can be used with a base package (i.e. `requests`), or with a package pinned to an exact version (i.e. `requests==2.21.0`). It also supports importing a `requirements.txt` style, the pip equivalent of `pip install -r <file>`. 
```
$ ochrona --install <package_name>|<requirements.txt>
```

### stdin Support
Ochrona supports supplying dependencies via stdin and can accept a PEP-508 complaint (i.e. requirements.txt) formated string, or a single dependency. Single dependencies can be supplied as the first argument or piped.

#### Single dependency via stdin
```
$ ochrona urllib3==1.26.4
$ echo "urllib3==1.26.4" | ochrona
```

#### Multi-dependency via stdin
```
$ pip freeze | ochrona
$ pipenv lock -r | ochrona
$ cat requirements.txt | ochrona
```

### Docker Support
Ochrona can be run via Docker. This is useful for the paranoid who may worry that an installed module could have modified the Python package namespace and allow malicious packages to bypass Ochrona's security checks. We've added this support in response to [CVE-2020-5252](https://mulch.dev/blog/CVE-2020-5252-python-safety-vuln/) which was disclosed prior to Ochrona and affects several other similar tools. 

#### Dockerized Ochrona passing api key
```
$ pip freeze | docker run -i --rm ochrona/ochrona ochrona --api_key <API_KEY>
```
#### Dockerized Ochrona with environment variables
```
$ pip freeze | docker run -i -e OCHRONA_API_KEY=$OCHRONA_API_KEY --rm ochrona/ochrona ochrona
```

# Output Formats
Ochrona supports several built in output options include a `BASIC` and `FULL` plaintext reports, as well as a Junit style `XML` report or a `JSON` style report for incorporating with other tools.

### Basic
[<p align="center"><img src="https://github.com/ochronasec/ochrona-cli/raw/master/resources/ochrona_basic.png"/></p>](https://ochrona.dev)

### Full
[<p align="center"><img src="https://github.com/ochronasec/ochrona-cli/raw/master/resources/ochrona_full.png"/></p>](https://ochrona.dev)

### XML (Junit)
[<p align="center"><img src="https://github.com/ochronasec/ochrona-cli/raw/master/resources/ochrona_xml.png"/></p>](https://ochrona.dev)

### JSON
[<p align="center"><img src="https://github.com/ochronasec/ochrona-cli/raw/master/resources/ochrona_json.png"/></p>](https://ochrona.dev)

# Modes of Operation
Ochrona operates in two different modes, `ad-hoc` and `record`. By default it operates in `ad-hoc` mode, meaning your dependency usage is not recorded. When you are ready to deploy your application to production you should run Ochrona in `record` mode so it can record a snapshot of your dependency usage. To set Ochrona in `record` mode, all you need to do is include a `project_name` either as a command line argument (i.e. `--project_name`) or in your `.ochrona.yml` file. 

Each time Ochrona is run in `record` mode it will overwrite the snapshot for the specified project name. If you'd like to utilize DADA to record multiple branches of the same project it is recommended that you simply use a naming convention to support this (ex. `my-project` vs `my-project_develop`).

When you sign up for Ochrona you are also granted access to https://app.ochrona.dev, which is a management portal for viewing/editing projects and retrieving your scan history.

# DADA Support
DADA stands for Deployed Application Dependency Analysis. It is an additional feature from Ochrona that allows for monitoring of the dependencies used in their python applications after they've been deployed. This functionality can give advanced alerting when a new vulnerability is discovered for a dependency being used in your deployed application. A single DADA project is available for all community users with Extended and Enterprise users having larger allowances.

Utilizing the `alert_config` parameters are also important for using DADA. These parameters dictate whether there are any special alerting conditions and where you would like alert emails to be sent. DADA configurations can be supplied in the `.ochrona.yml` file, via command line, or set via the [web portal](https://app.ochrona.dev).

# Represent!
[![Ochrona](https://img.shields.io/badge/secured_by-ochrona-blue)](https://ochrona.dev)

Let the world know you're keeping your project safe with Ochrona. Add our shield to your `README.md` by adding the following line.
```
[![Ochrona](https://img.shields.io/badge/secured_by-ochrona-blue)](https://ochrona.dev)
```
