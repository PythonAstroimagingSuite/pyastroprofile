#
# store observatory profiles
#
from dataclasses import dataclass
from pyastroprofile.ProfileDict import Profile, ProfileSection

class SettingsProfile(Profile):
    # where this should go under astroprofile directory hierarchy
    _conf_rel_dir = 'settings'

    @dataclass
    class PlateSolveSettings(ProfileSection):
        pixelscale : float = 5.7
        _sectionname : str = 'platesolve'

    @dataclass
    class AutoFocusSettings(ProfileSection):
        start_hfr : float = 25.0
        near_hfr : float = 12.0
        focus_delay : float = 0.0
        focus_dir : str = 'IN'
        exposure_start : float = 1.0
        exposure_max : float = 8.0
        exposure_min : float = 0.5
        _sectionname : str = 'autofocus'

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        # define attributes for this profile
        # NOTE altitude is in meters
#        self.platesolve_settings = self.PlateSolveSettings()
#        self.autofocus_settings = self.AutoFocusSettings()

        self.add_section(self.PlateSolveSettings)
        self.add_section(self.AutoFocusSettings)

#    def __repr__(self):
#        return f'SettingsProfile(platesolve_settings={self.platesolve_settings}, '\
#               f'autofocus_settings={self.autofocus_settings})'

#    def to_dict(self):
#        d ={}
#        d['platesolve'] = self.platesolve_settings.to_dict()
#        d['autofocus'] = self.autofocus_settings.to_dict()
#        print(f'settingsprofile to_dict = {d}')
#        return d

#    def from_dict(self, d):
#        print('from dict: ', d)
#        self.platesolve_settings = self.PlateSolveSettings()
#        self.platesolve_settings.from_dict(d['platesolve'])
#        self.autofocus_settings = self.AutoFocusSettings()
#        self.autofocus_settings.from_dict(d['autofocus'])
