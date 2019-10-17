import os
import yaml
import logging

from pyastroprofile.ProfileDict import get_base_config_dir
from pyastroprofile.EquipmentProfile import EquipmentProfile
from pyastroprofile.ObservatoryProfile import ObservatoryProfile
from pyastroprofile.SettingsProfile import SettingsProfile

# FIXME this should be something globally configured!
ASTROPROFILE_ROOT_RELDIR = 'astroprofiles'

ASTROPROFILE_EXT = '.yaml'

def get_astroprofile_base_dir():
    """
    Returns the base directory for astroprofile files.
    """
    return os.path.join(get_base_config_dir(), ASTROPROFILE_ROOT_RELDIR)

class AstroProfile:
    """
    This class acts as a container to hold other profiles.

    :param reldir: Path relative to the system configuration directory
                   to store the yaml settings file.
    :param name: The name of the settings file **WITHOUT** the '.yaml' extension.

    Currently the profiles stored are:
        * equipment (:class:`EquipmentProfile`)
        * observatory (:class:`ObservatoryProfile`)
        * settings (:class:`SettingsProfile`)

    Access is done as follows::

        from pyastroprofile.AstroProfile import AstroProfile
        ap = AstroProfile()
        ap.read('myastroprofile')
        print('latitude is ', ap.observatory.location.latitude)
        print('camera driver is ', ap.equipment.camera.driver)
        print('pixelscale is ', ap.settings.platesolve.pixelscale)
        ap.observatory.location.altitude = 300.0
        ap.equipment.focuser.driver = 'Focuser Simulator'
        ap.write()

    The astroprofile is stored in the file in the directory
    :func:`get_astroprofile_base_dir` and contains the names of
    the individual profile files for the different profiles
    contained by the :class:`AstroProfile`.
    """
    def __init__(self):
        #: Use to access the equipment profile.
        self.equipment = None
        #: Use to access the observatory profile.
        self.observatory = None
        #: Use to access the settings profile.
        self.settings = None

    def _create_section(self, section, name):
        return section(reldir=os.path.join(get_astroprofile_base_dir(), section._conf_rel_dir),
                       name=name)

    def create_reference(self, ref_name, equipment_profile,
                              observatory_profile, settings_profile,
                              overwrite=False):
        """
        Creates an astroprofile reference file which declares the
        other profiles to be contained within this astroprofile.

        :param str ref_name: Name of the reference file.
        :param str equipment_profile: Name of the equipment profile.
        :param str observatory_profile: Name of the observatory profile.
        :param str settings_profile: Name of the settings profile.
        :param bool overwrite: Whether to overwrite existing file or not.
        """
        path = get_astroprofile_base_dir()
        # FIXME might be better to have extension a constant?
        def_fname = os.path.join(path, ref_name + ASTROPROFILE_EXT)
        if os.path.isfile(def_fname) and not overwrite:
            logging.error(f'Reference file {ref_name} already exists and overwrite=False')
            return False
        d = {
                'equipment' : equipment_profile,
                'observatory' : observatory_profile,
                'settings' : settings_profile
             }

        with open(def_fname, 'w') as f:
            yaml.dump(d, stream=f)

        return True

    # an astroprofile is a text file which contains the names of the
    # equipment, observatory, and settings profiles
    def read(self, name):
        """
        Read an :class:`AstroProfile`.

        :param str name: Name of astroprofile file to be loaded.
        """
        path = get_astroprofile_base_dir()
        def_fname = os.path.join(path, name + ASTROPROFILE_EXT)
        logging.info(f'Loading astroprofile file {def_fname}')
        ap = None
        if os.path.isfile(def_fname):
            with open(def_fname, 'r') as f:
                ap = yaml.safe_load(stream=f)
            if ap is None:
                return False

            # find components
            equip_profile = ap.get('equipment', None)
            obs_profile = ap.get('observatory', None)
            set_profile = ap.get('settings', None)

            l = [equip_profile, obs_profile, set_profile]
            if not (l.count(None) == 0):
                return False

            self.equipment = self._create_section(EquipmentProfile, equip_profile)
            self.observatory = self._create_section(ObservatoryProfile, obs_profile)
            self.settings = self._create_section(SettingsProfile, set_profile)
            self.equipment.read()
            self.observatory.read()
            self.settings.read()

            return True

        return False

    def __repr__(self):
        return f'AstroProfile(equipment={self.equipment}, observatory={self.observatory}, ' \
               f'settings={self.settings})'

