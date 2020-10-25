#
# Profile handling based on dict
#
# Copyright 2020 Michael Fulbright
#
#
#    pyastroprofile is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
import os
import glob
import logging
from dataclasses import dataclass
import yaml

class NoDefaultProfile(Exception):
    """ raised if no default profile exists """
    pass

def get_base_config_dir():
    if os.name == 'nt':
        basedir = os.path.expandvars('%APPDATA%')
    elif os.name == 'posix':
        basedir = os.path.join(os.path.expanduser('~'), '.config')
    else:
        logging.error('ProgramSettings: Unable to determine OS for config_dir loc!')
        basedir = None
    return basedir

def find_profiles(loc):
    """ Assumes profiles end with .ini """
    config_glob = os.path.join(get_base_config_dir(), loc, '*.ini')
    #print(config_glob)
    ini_files = sorted(glob.glob(config_glob))
    return ini_files

def set_default_profile(loc, name):
    config_dir = os.path.join(get_base_config_dir(), loc)
    def_file = os.path.join(config_dir, 'DEFAULT_PROFILE')
    with open(def_file, 'w') as f:
        f.write(f'default={name}\n')

# FIXME duplication of method in Profile!
def get_default_profile(loc):
    """ See if DEFAULT_PROFILE file exists and check it for the
        name of the default profile """
    config_dir = os.path.join(get_base_config_dir(), loc)
    def_file = os.path.join(config_dir, 'DEFAULT_PROFILE')
    def_name = None
    if os.path.isfile(def_file):
        with open(def_file, 'r') as f:
            try:
                line = f.readline().strip()
                key, val = line.split('=')
                if key == 'default':
                    def_name = val
            except Exception:
                logging.error('Error determining default profile', exc_info=True)

    # zero length name is same as none
    if def_name is not None and len(def_name) < 1:
        def_name = None

    # test if profile exists
    if not os.path.isfile(def_name):
        def_name = None
    logging.debug(f'Using default profile = {def_name}')
    return def_name

@dataclass
class ProfileSection(object):
    def _property_keys(self):
        #logging.info(f'{self.__class__.__name__}._property_keys()')
        #logging.info(f'{self.__dict__}')
        #for k, v in self.__dict__.items():
        #    logging.info(f'   {k}   {v}')
        return sorted(x for x in self.__dict__ if x[0] != '_')

    def _to_dict(self):
        #logging.info(f'class {self.__class__.__name__}.to_dict():')
        d = {}
        #logging.info(f' property_keys = {self._property_keys()}')
        #logging.info(f' dir(self) = {dir(self)}')
        for k in self._property_keys():
            #logging.info(f'   {k}  {self.__dict__[k]}')
            d[k] = self.__dict__[k]
        return d

    def _from_dict(self, d):
        #logging.info(f'ProfileSection _from_dict {d}')
        for k, v in d.items():
            #logging.info(f' copying key {k} value = {v}')
            self.__dict__[k] = v
        #logging.info(f' final __dict__ = {self.__dict__}')

    def get(self, key, default=None):
        try:
            val = self.__getattribute__(key)
        except AttributeError:
            val = default
        return val

    def __repr__(self):
        s = f'{self.__class__.__name__}('
        ks = self.property_keys()
        i = 0
        #print(f'\n{ks}\n')
        for k in ks:
            if k == '_sectionname':
                continue
            s += f'{k}={self.__dict__[k]}'
            if i != len(ks) - 1:
                s += ', '
            i += 1
        s += ')'
        return s

class Profile:
    """Stores program settings which can be saved persistently"""

    def __init__(self, reldir, name=None):
        """Set some defaults for program settings

        reldir - location relative to top of default config location
                 If None then will be relative to current working directory!
              ex. "hfdfocus/devices" would create the dir "hfdfocus/device"

        name - name of config file
               If set to None then a default will be searched for.

        reldir = "hfdfocus/devices" and name = "C8F7.ini" would create
        a file  <configbasedir>/hfdfocus/C8F7.ini

        Will raise NoDefaultProfile is name is None and no profile is defined

        """
        #self._config = ConfigObj(unrepr=True, file_error=True, raise_errors=True)
        self._config_reldir = reldir

        # if name is none see if a default exists
        if name is None or name == 'default':
            name = self._find_default()
            if name is None:
                raise NoDefaultProfile

        self._config_filename = name

        logging.debug(f'self._config_filname = {self._config_filename}')
        logging.debug(f'self._config_reldir = {self._config_reldir}')

        self.sections = {}

    def add_section(self, sectionclass):
        self.sections[sectionclass._sectionname] = sectionclass
        self.__dict__[sectionclass._sectionname] = sectionclass()

#    def _find_default(self):
#        """ See if DEFAULT_PROFILE file exists and check it for the
#            name of the default profile """
#        def_file = os.path.join(self._get_config_dir(), "DEFAULT_PROFILE")
#        def_name = None
#        if os.path.isfile(def_file):
#            with open(def_file, 'r') as f:
#                try:
#                    def_name = f.readline().strip()
#                except Exception:
#                    logging.error('Error determining default profile', exc_info=True)
#
#        logging.debug(f'Using default profile = {def_name}')
#        return def_name

    def _find_default(self):
        # get_default_profile() accepts a relative path from base config dir
        return get_default_profile(self._config_reldir)

    def get_default(self):
        return self._find_default()

    def _get_config_dir(self):
        if self._config_reldir is None:
            return '.'
        if os.name == 'nt':
            base_config_dir = get_base_config_dir()
            config_dir = os.path.join(base_config_dir, self._config_reldir)
        elif os.name == 'posix':
            base_config_dir = get_base_config_dir()
            config_dir = os.path.join(base_config_dir, self._config_reldir)
        else:
            logging.error('ProgramSettings: Unable to determine OS '
                          'for config_dir loc!')
            config_dir = None
        return config_dir

    def _get_config_filename(self):
        return os.path.join(self._get_config_dir(), self._config_filename)

    def write(self):
        # NOTE will overwrite existing without warning!
        logging.debug(f'Configuration files stored in {self._get_config_dir()}')

        #self._config.filename = self._get_config_filename()

        # check if config directory exists
        if not os.path.isdir(self._get_config_dir()):
            if os.path.exists(self._get_config_dir()):
                logging.error('write settings: config dir'
                              f' {self._get_config_dir()}'
                              f' already exists and is not a directory!')
                return False
            else:
                logging.info('write settings: creating config dir '
                             f'{self._get_config_dir()}')
                os.makedirs(self._get_config_dir())

        logging.info(f'write() config filename: {self._get_config_filename()}')
        #logging.info(f'self._config = {self._config}')

        # to_dict() must be defined by child class
        dataobj = {}

        #logging.info(f'sections = {self.sections}')
        for k, v in self.sections.items():
            #logging.info(f' added key {k} value {v()._to_dict()}')
            dataobj[k] = self.__dict__[k]._to_dict()

        #dataobj = self.to_dict()
        #logging.info(f'to_dict = {dataobj}')

        yaml_f = open(self._get_config_filename(), 'w')
        yaml.dump(dataobj, stream=yaml_f, default_flow_style=False)
        yaml_f.close()

        return True

    def read(self):
        yaml_f = open(self._get_config_filename(), 'r')
        d = yaml.safe_load(stream=yaml_f)
        yaml_f.close()
        #logging.debug(f'read profile is {d}')

        # from_dict() must be defined in child
        #self.from_dict(d)
        for k, v in d.items():
            #logging.info(f'{k} {v} = {self.sections[k]()._from_dict(v)}')
            self.__dict__[k] = self.sections[k]()
            self.__dict__[k]._from_dict(v)

        return True

    def __repr__(self):
        s = f'{self.__class__.__name__}('
        ks = self.sections.keys()
        #print(self.sections)
        #print(f'\n{ks}\n')
        i = 0
        for k in ks:
            if k[0] == '_':
                continue
            #print(type(self.__dict__[k]))
            s += f'{k}={self.__dict__[k]}'
            if i != len(ks) - 1:
                s += ', '
            i += 1
        s += ')'
        return s
