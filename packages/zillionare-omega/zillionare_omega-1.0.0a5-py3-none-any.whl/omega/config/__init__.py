#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Aaron-Yang [code@jieyu.ai]
Contributors:

"""
import logging
import os
import sys
from os import path

import cfg4py
from termcolor import colored

logger = logging.getLogger(__name__)


def get_config_dir():
    if os.environ[cfg4py.envar] == "PRODUCTION":
        _dir = path.expanduser("~/zillionare/omega/config")
    elif os.environ[cfg4py.envar] == "TEST":
        _dir = path.expanduser("~/.zillionare/omega/config")
    else:
        _dir = path.normpath(path.join(path.dirname(__file__), "../config"))

    sys.path.insert(0, _dir)
    return _dir


def check_env():
    server_roles = ["PRODUCTION", "TEST", "DEV"]
    if os.environ.get(cfg4py.envar) not in ["PRODUCTION", "TEST", "DEV"]:
        print(
            f"请设置环境变量{colored(cfg4py.envar, 'red')}为["
            f"{colored(server_roles, 'red')}]之一。"
        )
        sys.exit(-1)
