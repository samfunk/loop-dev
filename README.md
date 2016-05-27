# ![avant logo](https://avantprod.global.ssl.fastly.net/assets/v3/home2/logo-icon-dark-ddd7488b0288497a8f9ea2c5aa24f65d.png) Loop [![Build Status](https://travis-ci.org/kirillseva/loop.svg?branch=master)](https://travis-ci.org/kirillseva/loop)

## Hyperparameter optimization as a service

Fill in later

## Quick Start

### Install dependencies

```sh
$ brew install pyenv pyenv-virtualenv
$ pip install --upgrade pip
$ pyenv install 3.5.1
$ pyenv local 3.5.1
$ pyenv virtualenv loop
```

Or, if the above is not working, run the following commands in
the directory above where you git cloned this repo.
```sh
$ brew install pyenv pyenv-virtualenv
$ pip install --upgrade pip
$ pyenv install 3.5.1
$ mkdir virtualenvs #assuming you don't already have a virtualenv directory
$ virtualenv -p /Users/{{username}}/.pyenv/versions/3.5.1/bin/python3.5 virtualenvs/loop
$ source virtualenvs/loop/bin/activate
$ cd loop
```

### First Steps

```sh
$ pyvenv activate loop
$ pip install -r requirements.txt
```

### Set up Migrations

```sh
$ python manage.py db upgrade
```

### Run



### Tests

Tests go in /tests and can be run with

```sh
$ python -m unittest discover tests
```
