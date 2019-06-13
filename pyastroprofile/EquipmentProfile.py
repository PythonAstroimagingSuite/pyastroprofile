#
# store equipment profiles
#
from dataclasses import dataclass

from pyastroprofile.ProfileDict import Profile, ProfileSection

class EquipmentProfile(Profile):
    """
    This class represents the equipment profile.

    :param reldir: Path relative to the system configuration directory
                   to store the yaml settings file.
    :param name: The name of the settings file **WITHOUT** the '.yaml' extension.

    Currently the settings stored are:
        * focuser
        * filterwheel
        * camera
        * mount
        * telescope

    Access is done as follows::

        from pyastroprofile.EquipmentProfile import EquipmentProfile
        ep = EquipmentProfile(reldir='equipment', name='myequipment')
        ep.read()
        print('camera driver is ', ep.camera.driver)
        ep.telscope.focal_length = 1000.0
        ep.write()

    This example will create the file '<system config dir>/equipment/myequipment.yaml'

    **NOTE**: It is recommended to use the :class:`AstroProfile` class for
    accessing these settings as it includes the :class:`ObservatoryProfile` class.

    """

    # where this should go under astroprofile directory hierarchy
    _conf_rel_dir = 'equipment'

    @dataclass
    class Focuser(ProfileSection):
        # set some hopefully safe defaults
        _sectionname : str = 'focuser'
        #: Focuser driver
        driver : str = 'Not Set'
        #: Minimum allowed position for focuser
        minpos : int = 0
        #: Maximum allowed position for focuser
        maxpos : int = 0

    @dataclass
    class Camera(ProfileSection):
        _sectionname : str = 'camera'
        #: Camera driver
        driver : str = 'Not Set'

    @dataclass
    class Mount(ProfileSection):
        _sectionname : str = 'mount'
        #: Mount driver
        driver : str = 'Not Set'

    @dataclass
    class FilterWheel(ProfileSection):
        _sectionname : str = 'filterwheel'
        #: Filter wheel driver
        driver : str = 'Not Set'

    @dataclass
    class Telescope(ProfileSection):
        _sectionname : str = 'telescope'
        #: Focal length of telescope
        focal_length : int = 0
        #: Aperture of telescope
        aperture : int = 0
        #: Obstruction of telescope
        obstruction : int = 0

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)
        self.add_section(self.Focuser)
        self.add_section(self.Camera)
        self.add_section(self.Mount)
        self.add_section(self.FilterWheel)
        self.add_section(self.Telescope)
