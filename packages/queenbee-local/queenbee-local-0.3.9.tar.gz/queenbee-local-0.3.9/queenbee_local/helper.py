"""Collection of utility functions."""
import os
import json
import shutil

from typing import Union, Dict, List
from distutils.dir_util import copy_tree
from distutils.errors import DistutilsFileError
from multiprocessing import cpu_count


def tab_forward(input: str, indent: int = 0):
    rep = '\n' + '\t' * indent
    string = rep.join(input.split('\n'))
    return ('\t' * indent + string).replace('\t', '    ')


def to_camel_case(name: str):
    return ''.join(n.capitalize() for n in name.split('-'))


def to_snake_case(name: str):
    return ''.join(n.lower() for n in name.replace('-', '_'))


def parse_input_args(args):
    """Parse input arguments for a recipe module."""
    user_values = {}
    if not 2 <= len(args) <= 4:
        raise ValueError(f'Number of arguments must be between 2-4 not {len(args)}.\n')
    if len(args) == 2:
        # only project folder is provided
        # no inputs file - set the workers to default
        project_folder = args[1]
        workers = cpu_count() - 1
    else:
        project_folder = args[1]
        input_file = args[2]
        try:
            workers = args[3]
        except IndexError:
            workers = cpu_count() - 1
        try:
            with open(input_file) as inp:
                user_values = json.load(inp)
        except Exception as e:
            raise ValueError(f'Failed to load input_file: {input_file}\n{e}')

    return project_folder, user_values, workers


def parse_user_recipe_args(user_values: Union[List, Dict]) -> Dict[str, str]:
    """parse inputs.json recipe inputs provided by user."""
    if isinstance(user_values, list):
        # update schema
        values = {}
        for item in user_values:
            try:
                k, v = item['name'], item['value']
            except KeyError:
                # artifact
                try:
                    k, v = item['name'], item['source']['path']
                except KeyError:
                    raise ValueError(f'Invalid input argument: {item}')
            values[k] = v
    else:
        values = dict(user_values)

    return values


def update_params(input_params: Dict, user_values: Union[List, Dict]) -> Dict[str, str]:
    """Update input params based on values provided by user."""
    values = parse_user_recipe_args(user_values)
    params = {}
    for k, v in values.items():
        params[to_snake_case(k)] = v
    input_params.update(params)
    return input_params


def _change_permission(dst):
    for root, dirs, files in os.walk(dst):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)
        for f in files:
            os.chmod(os.path.join(root, f), 0o777)


def _copy_artifacts(src, dst):
    """copy file or folder."""
    if os.path.normpath(src) == os.path.normpath(dst):
        # input and output files are the same file
        return
    try:
        # try to copy the folder
        copy_tree(src, dst)
        _change_permission(dst)
    except DistutilsFileError:
        # create the folder if doesn't exist
        dirname = os.path.dirname(dst)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        shutil.copy(src, dst)
        _change_permission(dirname)
