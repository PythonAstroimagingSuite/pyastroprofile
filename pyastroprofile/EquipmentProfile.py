#
# store equipment profiles
#
from pyastroprofile.Profile import Profile

class EquipmentProfile(Profile):
    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        self.camera_driver = None
        self.telescope_driver = None
        self.focuser_driver = None
        self.filterwheel_driver = None

        self.focuser_max_pos = None
        self.focuser_min_pos = None
        self.focuser_pref_dir = None


