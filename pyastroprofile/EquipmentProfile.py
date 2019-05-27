#
# store equipment profiles
#

import astropy.units as u
from pyastroprofile.Profile import Profile

from astroplan import Observer

class EquipmentProfile(Profile):
    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        self.camera_driver = None
        self.mount_driver = None
        self.focuser_driver = None
        self.filterwheel_driver = None

