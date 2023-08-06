[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![CircleCI](https://circleci.com/gh/circleci/circleci-docs.svg?style=shield)](https://app.circleci.com/pipelines/github/mashi/codecov-validator?branch=main)


# Description
Validates the codecov.yml configuration file.

This code is simply the curl command described in the (codecov documentation)[https://docs.codecov.io/docs/codecov-yaml]
converted in python.


## Instructions (Development)
Create a virtual environment and install the required packages with
```
python3 -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
pre-commit install
```
