#
# store equipment profiles
#
from dataclasses import dataclass

from pyastroprofile.ProfileDict import Profile, ProfileSection

class EquipmentProfile(Profile):

    @dataclass
    class Focuser(ProfileSection):
        driver : str = 'Focus Simulator'
        minpos : int = 5000
        maxpos : int = 10000

    @dataclass
    class Camera(ProfileSection):
        driver : str = 'CCD Simulator'

    @dataclass
    class Mount(ProfileSection):
        driver : str = 'Telescope Simulator'

    @dataclass
    class FilterWheel(ProfileSection):
        driver : str = 'FilterWheel Simulator'

    @dataclass
    class Telescope(ProfileSection):
        focal_length : int = 800
        aperture : int = 200

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)
        self.focuser = self.Focuser()
        self.camera = self.Camera()
        self.mount = self.Mount()
        self.filterwheel = self.FilterWheel()
        self.telescope = self.Telescope()

    def __repr__(self):
        return f'{self .__class__.__name__}(' \
               f'Focuser={self.focuser}),' \
               f'Focuser={self.camera}),' \
               f'Mount={self.mount}),' \
               f'FilterWheel={self.filterwheel},' \
               f'Telescope={self.telescope})'

    def to_dict(self):
        d = {}
        print(dir(self.focuser))
        d['Focuser'] = self.focuser._to_dict()
        d['Camera'] = self.camera._to_dict()
        d['Mount'] = self.mount._to_dict()
        d['FilterWheel'] = self.filterwheel._to_dict()
        d['Telescope'] = self.telescope._to_dict()
        return d

    def from_dict(self, d):
        self.focuser = self.Focuser()
        self.focuser._from_dict(d['Focuser'])
        self.camera = self.Camera()
        self.camera._from_dict(d['Camera'])
        self.mount = self.Mount()
        self.mount._from_dict(d['Mount'])
        self.filterwheel = self.FilterWheel
        self.filterwheel._from_dict(d['FilterWheel'])
        self.telescope = self.Telescope()
        self.telescope._from_dict(d['Telescope'])
