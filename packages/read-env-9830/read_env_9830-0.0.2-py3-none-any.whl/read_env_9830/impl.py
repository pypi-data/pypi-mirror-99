# -*- coding: utf-8 -*-

"""
read_env_9830
=============

Problem
-------

1. A brief informal statement of the problem

  - give examples

2. The precise correctness conditions required of a solution


Solution
--------

3. Describe the solution

  - Whenever needed, explain the "why" of the design

"""


# Imports

import logging
from functools import partial
from pathlib import Path
import os

logger = logging.getLogger(__name__)


# Implementation


def get_env_value(
    name, is_path=False, is_bool=False, is_optional=False, is_int=False, is_float=False
):
    try:
        val = os.environ[name]
    except KeyError as e:
        if is_optional:
            return None
        else:
            msg = f'''Expected: env variable exists. Actual: env variable does not exist. env variable: {name}'''
            raise AssertionError(msg)

    if is_path:
        return Path(val).resolve()
    elif is_bool:
        return val == "true"
    elif is_int:
        return int(val)
    elif is_float:
        return float(val)
    else:
        return val


get_env_path = partial(get_env_value, is_path=True)
get_env_bool = partial(get_env_value, is_bool=True)
get_env_int = partial(get_env_value, is_int=True)
get_env_float = partial(get_env_value, is_float=True)


# Interface
# Exported through the __init__.py file
