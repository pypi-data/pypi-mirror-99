#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of pspman.
#
# pspman is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pspman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pspman.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Configuration

'''


import os
from pathlib import Path
import typing
import yaml
from .errors import PathNameError


def _config_dir(config: typing.Union[str, os.PathLike] = None) -> Path:
    '''
    Guess the default configuration path based on XDG_CONFIG_HOME variable
    Following paths are checked in order until a feasable target is found

        * ``config``
        * ${XDG_CONFIG_HOME}/pspman
        * ${HOME}/.config/pspman
        * ${HOME}/.pspman
        * ${PWD}/.pspman

    Args:
        config: recommended config directory

    Returns:
        Path to config dir

    '''
    if config:
        config_path = Path(config)
        if config_path.is_dir():
            # Deliberately not creating anew
            return config_path.resolve()
        else:
            err_str = f"Configuration directory '{config}' does not exist."\
                + f"Do you mean {config_path.parent}?"
            raise FileNotFoundError(err_str)
    config_var = os.environ.get('XDG_CONFIG_HOME')
    if config_var is not None:
        config_path = Path(config_var).joinpath('pspman')
        config_path.mkdir(parents=True, exist_ok=True)
        return config_path.resolve()
    home_dir = os.environ.get('HOME')
    if home_dir is None:
        # On which wierd operating system is this installed!
        config_path = Path(".pspman")
        config_path.mkdir(parents=True, exist_ok=True)
        return config_path.resolve()
    config_dir = Path(home_dir).joinpath('.config')
    config_path = config_dir.joinpath('pspman')
    if config_dir.is_dir():
        config_path.mkdir(parents=True, exist_ok=True)
        return config_path.resolve()
    # Why don't you have .config!
    config_path = Path(home_dir).joinpath('.pspman')
    config_path.mkdir(parents=True, exist_ok=True)
    return config_path.resolve()


def _data_dir(data: str = None) -> Path:
    '''
    Guess the default data path based on XDG_DATA_HOME variable
    Following paths are checked in order until a feasable target is found

        * ``data``
        * ${XDG_DATA_HOME}/pspman
        * ${HOME}/.local/share/pspman
        * ${HOME}/.pspman
        * ${PWD}/.pspman

    Args:
        data: recommended data directory

    Returns:
        path to config dir

    '''
    if data:
        data_path = Path(data)
        if data_path.is_dir():
            # Deliberately not creating anew
            return data_path.resolve()
        else:
            err_str = f"Data path '{data_path}' does not exist." + \
                f"Do you mean {data_path.parent}?"
            raise FileNotFoundError(err_str)
    data_var = os.environ.get('XDG_DATA_HOME')
    if data_var is not None:
        data_path = Path(data_var).joinpath('pspman')
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path.resolve()
    home_dir = os.environ.get('HOME')
    if home_dir is None:
        # On which wierd operating system is this installed!
        data_path = Path(".pspman")
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path.resolve()
    data_dir = Path(home_dir).joinpath('.local', 'share')
    data_path = data_dir.joinpath('pspman')
    if data_dir.is_dir():
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path.resolve()
    # Why don't you have .data!
    data_path = Path(home_dir).joinpath('.pspman')
    data_path.mkdir(parents=True, exist_ok=True)
    return data_path.resolve()


class GroupDB():
    '''
    Group database information

    Args:
        **kwargs:

            * data: create object using data as __dict__
            * arg in Attributes: Hard-set attributes
            * rest are ignored

    Attributes:
        grp_path: path to Group
        name: custom-name for group [default: leaf of path]
        exists: whether path exists
        locked: locked by another process?
        clone_type: type of clones (0[default], -1, 1)

            * 1: all projects are installable
            * -1: no project is installable (all are pull-only)
            * 0: heterogenous

    '''
    def __init__(self, **kwargs):
        grp_path = kwargs.get('grp_path')
        if grp_path is None:
            self._grp_path: typing.Optional[str] = None
        else:
            self._grp_path = str(grp_path)
        self.clone_type = int(kwargs.get('clone_type', 0))

        # Infer from parent.__dict__
        if 'data' in kwargs:
            self.merge(kwargs['data'])
            del kwargs['data']

        self.name = str(kwargs.get('name', self.get_name()))

    @property
    def locked(self) -> bool:
        if self.grp_path.joinpath('.proc.lock').exists():
            return True
        return False

    @locked.setter
    def locked(self, val):
        # Do nothing, shouldn't get hard-set
        return

    @locked.deleter
    def locked(self):
        # Do nothing, shouldn't get hard-set
        return

    @property
    def grp_path(self) -> Path:
        if self._grp_path:
            return Path(self._grp_path).resolve()
        raise ValueError('Value for path not provided')

    @grp_path.setter
    def grp_path(self, value: typing.Union[str, os.PathLike]):
        self._grp_path = str(Path(value).resolve())

    @property
    def exists(self) -> bool:
        if self.grp_path is None:
            return False
        return self.grp_path.is_dir()

    @exists.setter
    def exists(self, val):
        # Do nothing, shouldn't get hard-set
        return

    @exists.deleter
    def exists(self):
        # Do nothing, shouldn't get hard-set
        return

    def get_name(self) -> str:
        '''
        Infer name from filepath
        '''
        if hasattr(self, 'name'):
            return self.name
        if self.grp_path is None:
            raise PathNameError()
        return self.grp_path.stem

    def mk_structure(self):
        '''
        Generate a directory structure for the GitGroup
        '''
        self.grp_path.mkdir(parents=True, exist_ok=True)
        dir_struct = ("bin", "etc", "include", "lib", "lib64", "libexec",
                      "programs", "share", "src", "tmp", "usr")
        for workdir in dir_struct:
            self.grp_path.joinpath(workdir).mkdir(parents=True, exist_ok=True)

    def merge(self, data: typing.Dict[str, object]) -> None:
        '''
        Update values that are ``None`` type using ``data``.
        Doesn't change set values

        Args:
            data: source for update

        '''
        for key, val in data.items():
            setattr(self, key, self.__dict__.get(key) or val)

    def __repr__(self) -> str:
        '''
        Representation
        '''
        clone_type = ('heterogenous',  'install', 'pull-only')[self.clone_type]
        locked = ('No', 'Yes')[int(self.locked)]
        return f'''
        name: {self.name}
        path: {self.grp_path}
        exists: {self.exists}
        locked: {locked}
        clone_type: {clone_type}
        '''

class MetaConfig():
    '''
    Meta-Config bearing information about all GroupDBs

    Args:
        kwargs:

            * arg in Attributes: Hard-set attributes
            * rest are ignored

    Attributes:
        meta_db_dirs: registry of all GroupDBs
        config_dir: pspman configuration directory
        data_dir: pspman default data directory
        opt_in: opted installation methods

    '''
    def __init__(self, **kwargs):
        self.meta_db_dirs: typing.Dict[str, GroupDB] =\
            kwargs.get('meta_db_dirs') or {}
        self.config_dir = _config_dir(kwargs.get('config_dir'))
        self.data_dir = _data_dir(kwargs.get('data_dir'))
        self.opt_in: typing.List[str] = kwargs.get('opt_in') or []
        for group in (kwargs.get('meta_db_dirs') or {}).values():
            self.add(group)

    def add(self, group: typing.Union[GroupDB, dict]):
        '''
        Add (don't overwrite) Group

        Args:
            group: Group (or its __dict__) to be added
        '''
        if isinstance(group, dict):
            group = GroupDB(data=group)
        if group.name in self.meta_db_dirs:
            return
        if group.grp_path == self.data_dir and group.name != 'default':
            # Default prefix
            return
        self.meta_db_dirs[group.name] = group

    def remove(self, name: str):
        '''
        Remove group

        Args:
            name: name of group to remove

        '''
        if name in self.meta_db_dirs:
            del self.meta_db_dirs[name]

    def prune(self):
        '''
        If any group doesn't exist anymore, remove it
        '''
        zombies: typing.List[str] = []
        for name, group in self.meta_db_dirs.items():
            if not group.exists:
                zombies.append(name)
        for name in zombies:
            self.remove(name)

    def load(self, psp_config_file: typing.Union[os.PathLike, str]) -> bool:
        '''
        Load meta configuration

        Args:
            psp_config_dir: yaml file containing GroupDB meta data

        Returns:
            ``True`` if file was successfully loaded
        '''
        psp_config = Path(psp_config_file)
        if not psp_config.is_file():
            return False
        with open(psp_config, 'r') as conf_fh:
            groups_data: typing.Dict[str, dict] = yaml.safe_load(conf_fh)
        for group in groups_data.values():
            self.add(group)
        return True

    def store(self):
        '''
        Refresh a configuration file

        '''
        psp_config = self.config_dir.joinpath('config.yml')
        with open(psp_config, 'w') as conf_fh:
            for group_name, group_db in self.meta_db_dirs.items():
                yaml.dump({group_name: group_db.__dict__}, conf_fh)


def read_config(config_file: str = None) -> MetaConfig:
    '''
    Read and maintain default configurations

    Args:
        config_file: path to file containing configurations

    Returns:
        Configuration
    '''
    psp_config = _config_dir(config_file).joinpath('config.yml')
    config = MetaConfig()
    if config.load(psp_config):
        config.prune()
        return config
    init_msg = [
        'PSPMan is not initialized',
        '',
        "To initialize: run without '# ':",
        "# \033[0;97;40mpspman init\033[0m:",
        '',
        "Check help for omitting some installation methods: run without '# ':",
        "# \033[0;97;40mpspman init -h\033[0m:",
        '',
    ]
    print("\n    ".join(init_msg))
    return config
