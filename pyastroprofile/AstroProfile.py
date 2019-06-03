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
    return os.path.join(get_base_config_dir(), ASTROPROFILE_ROOT_RELDIR)

class AstroProfile:
    def __init__(self):
        self.equipment = None
        self.observatory = None
        self.settings = None

    def _create_section(self, section, name):
        return section(reldir=os.path.join(get_astroprofile_base_dir(), section._conf_rel_dir),
                       name=name)

    def create_reference(self, ref_name, equipment_profile,
                              observatory_profile, settings_profile,
                              overwrite=False):
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
        path = get_astroprofile_base_dir()
        def_fname = os.path.join(path, name + ASTROPROFILE_EXT)
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

