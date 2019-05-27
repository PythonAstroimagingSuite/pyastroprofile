#
# handles a profile
#
# a profile is a config file describing settings for a given application
#
# the profile can be specified by a name 'C8Mach1' or if a profile
# name is not supplied a default will be loaded
#
# the default must be specified - there is no default profile by default
#
#

import os
import glob
import logging
from configobj import ConfigObj

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
    print(config_glob)
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
                l = f.readline().strip()
                key, val = l.split('=')
                if key == 'default':
                    def_name = val
            except Exception:
                logging.error('Error determining default profile', exc_info=True)

    # zero length name is same as none
    if def_name is not None and len(def_name) < 1:
        def_name = None
    logging.debug(f'Using default profile = {def_name}')
    return def_name

class Profile:
    """Stores program settings which can be saved persistently"""
    def __init__(self, reldir, name=None):
        """Set some defaults for program settings

        reldir - location relative to top of default config location
              ex. "hfdfocus/devices" would create the dir "hfdfocus/device"

        name - name of config file
               If set to None then a default will be searched for.

        reldir = "hfdfocus/devices" and name = "C8F7.ini" would create
        a file  <configbasedir>/hfdfocus/C8F7.ini

        Will raise NoDefaultProfile is name is None and no profile is defined

        """
        self._config = ConfigObj(unrepr=True, file_error=True, raise_errors=True)
        self._config_reldir = reldir

        # if name is none see if a default exists
        if name == None or name == 'default':
            name = self._find_default()
            if name is None:
                raise NoDefaultProfile

        self._config_filename = name

        logging.debug(f'self._config_filname = {self._config_filename}')
        logging.debug(f'self._config_reldir = {self._config_reldir}')

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

    # FIXME This will break HORRIBLY unless passed an attribute already
    #       in the ConfigObj dictionary
    #
    def __getattr__(self, attr):
        #logging.info(f'{self.__dict__}')
        if not attr.startswith('_'):
            return self._config[attr]
        else:
            return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        #logging.info(f'setattr: {attr} {value}')
        if not attr.startswith('_'):
            self._config[attr] = value
        else:
            super().__setattr__(attr, value)

    def _get_config_dir(self):
        if os.name == 'nt':
            base_config_dir = get_base_config_dir()
            config_dir = os.path.join(base_config_dir, self._config_reldir)
        elif os.name == 'posix':
            base_config_dir = get_base_config_dir()
            config_dir = os.path.join(base_config_dir, self._config_reldir)
        else:
            logging.error('ProgramSettings: Unable to determine OS for config_dir loc!')
            config_dir = None
        return config_dir

    def _get_config_filename(self):
        return os.path.join(self._get_config_dir(), self._config_filename)

    def write(self):
        # NOTE will overwrite existing without warning!
        logging.debug(f'Configuration files stored in {self._get_config_dir()}')

        self._config.filename = self._get_config_filename()

        # check if config directory exists
        if not os.path.isdir(self._get_config_dir()):
            if os.path.exists(self._get_config_dir()):
                logging.error(f'write settings: config dir {self._get_config_dir()}' + \
                              f' already exists and is not a directory!')
                return False
            else:
                logging.info(f'write settings: creating config dir {self._get_config_dir()}')
                os.makedirs(self._get_config_dir())

        logging.info(f'config filename: {self._config.filename}')
        self._config.write()

    def read(self):
        logging.debug(f'Profile.read(): filename = {self._get_config_filename()}')
        try:
            config = ConfigObj(self._get_config_filename(), unrepr=True,
                               file_error=True, raise_errors=True)
        except Exception:
            logging.error('Error creating config object in Profile.read()', exc_info=True)
            config = None

        if config is None:
            logging.error('failed to read config file!')
            return False

        self._config.merge(config)
        return True