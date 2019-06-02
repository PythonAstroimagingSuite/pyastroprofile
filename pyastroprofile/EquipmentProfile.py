#
# store equipment profiles
#
from pyastroprofile.ProfileDict import Profile

class EquipmentProfile(Profile):

    class Focuser:
        driver = 'Focus Simulator'
        minpos = 5000
        maxpos = 10000

        def __repr__(self):
            return f'Focuser(driver={self.driver}, minpos={self.minpos}, maxpos={self.maxpos})'

    class Camera:
        driver = 'CCD Simulator'

        def __repr__(self):
            return f'Camera(driver={self.driver})'

    class Mount:
        driver = 'Telescope Simulator'

        def __repr__(self):
            return f'Mount(driver={self.driver})'

    class FilterWheel:
        driver = 'FilterWheel Simulator'

        def __repr__(self):
            return f'FilterWheel(driver={self.driver})'

    class Telescope:
        focal_length = 800
        aperture = 200

        def __repr__(self):
            return f'Telescope(focal_length={self.focal_length}, '\
                   f'aperture={self.aperture})'

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
        d['Focuser'] = { 'driver' : self.focuser.driver,
                         'minpos' : self.focuser.minpos,
                         'maxpos' : self.focuser.maxpos }
        d['Camera'] = { 'driver' : self.camera.driver}
        d['Mount'] = { 'driver' : self.mount.driver}
        d['FilterWheel'] = { 'driver' : self.filterwheel.driver}
        d['Telescope'] = { 'focal_length' : self.focal_length,
                           'aperture' : self.aperture }
        return d

    def from_dict(self, d):
        self.focuser = self.Focuser()
        self.focuser.driver = d['Focuser']['driver']
        self.focuser.minpos = d['Focuser']['minpos']
        self.focuser.maxpos = d['Focuser']['maxpos']
        self.camera = self.Camera()
        self.camera.driver = d['Camera']['driver']
        self.mount = self.Mount()
        self.mount.driver = d['Mount']['driver']
        self.filterwheel = self.FilterWheel
        self.filterwheel.driver = d['FilterWheel']['driver']
        self.telescope = self.Telescope()
        self.telescope.focal_length = d['Telescope']['focal_length']
        self.telescpoe.aperture = d['Telescope']['aperture']