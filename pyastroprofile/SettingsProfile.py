#
# store observatory profiles
#

from pyastroprofile.ProfileDict import Profile, ProfileSection

class SettingsProfile(Profile):

    class PlateSolveSettings(ProfileSection):
        def __init__(self):
            self.pixelscale = 5.7

    class AutoFocusSettings(ProfileSection):
        def __init__(self):
            self.start_hfr = 25.0
            self.near_hfr = 12.0
            self.focus_delay = 0.0
            self.focus_dir = 'IN'
            self.exposure_start = 1.0
            self.exposure_max = 8.0
            self.exposure_min = 0.5

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        # define attributes for this profile
        # NOTE altitude is in meters
        self.platesolve_settings = self.PlateSolveSettings()
        self.autofocus_settings = self.AutoFocusSettings()

    def __repr__(self):
        return f'SettingsProfile(platesolve_settings={self.platesolve_settings}, '\
               f'autofocus_settings={self.autofocus_settings})'

    def to_dict(self):
        d ={}
        d['platesolve'] = self.platesolve_settings.to_dict()
        d['autofocus'] = self.autofocus_settings.to_dict()
        print(f'settingsprofile to_dict = {d}')
        return d

    def from_dict(self, d):
        print('from dict: ', d)
        self.platesolve_settings = self.PlateSolveSettings()
        self.platesolve_settings.from_dict(d['platesolve'])
        self.autofocus_settings = self.AutoFocusSettings()
        self.autofocus_settings.from_dict(d['autofocus'])
