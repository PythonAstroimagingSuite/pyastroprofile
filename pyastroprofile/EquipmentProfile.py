#
# store equipment profiles
#
from dataclasses import dataclass

from pyastroprofile.ProfileDict import Profile, ProfileSection

class EquipmentProfile(Profile):
    # where this should go under astroprofile directory hierarchy
    _conf_rel_dir = 'equipment'

    @dataclass
    class Focuser(ProfileSection):
        # set some hopefully safe defaults
        _sectionname : str = 'focuser'
        driver : str = 'Not Set'
        minpos : int = 0
        maxpos : int = 0

    @dataclass
    class Camera(ProfileSection):
        _sectionname : str = 'camera'
        driver : str = 'Not Set'

    @dataclass
    class Mount(ProfileSection):
        _sectionname : str = 'mount'
        driver : str = 'Not Set'

    @dataclass
    class FilterWheel(ProfileSection):
        _sectionname : str = 'filterwheel'
        driver : str = 'Not Set'

    @dataclass
    class Telescope(ProfileSection):
        _sectionname : str = 'telescope'
        focal_length : int = 0
        aperture : int = 0

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)
#        self.focuser = self.Focuser()
#        self.camera = self.Camera()
#        self.mount = self.Mount()
#        self.filterwheel = self.FilterWheel()
#        self.telescope = self.Telescope()

        self.add_section(self.Focuser)
        self.add_section(self.Camera)
        self.add_section(self.Mount)
        self.add_section(self.FilterWheel)
        self.add_section(self.Telescope)


#    def __repr__(self):
#        return f'{self .__class__.__name__}(' \
#               f'Focuser={self.focuser}),' \
#               f'Focuser={self.camera}),' \
#               f'Mount={self.mount}),' \
#               f'FilterWheel={self.filterwheel},' \
#               f'Telescope={self.telescope})'
#
#    def to_dict(self):
#        d = {}
#        d['Focuser'] = self.focuser._to_dict()
#        d['Camera'] = self.camera._to_dict()
#        d['Mount'] = self.mount._to_dict()
#        d['FilterWheel'] = self.filterwheel._to_dict()
#        d['Telescope'] = self.telescope._to_dict()
#        logging.debug(f'{self.__class__.__name__}.to_dict(): {d}')
#        return d
#
#    def from_dict(self, d):
#        self.focuser = self.Focuser()
#        self.focuser._from_dict(d['Focuser'])
#        self.camera = self.Camera()
#        self.camera._from_dict(d['Camera'])
#        self.mount = self.Mount()
#        self.mount._from_dict(d['Mount'])
#        self.filterwheel = self.FilterWheel
#        self.filterwheel._from_dict(d['FilterWheel'])
#        self.telescope = self.Telescope()
#        self.telescope._from_dict(d['Telescope'])
