#
# Store equipment profiles
#
# Copyright 2020 Michael Fulbright
#
#
#    pyastroprofile is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from dataclasses import dataclass, field

from pyastroprofile.ProfileDict import Profile, ProfileSection

class EquipmentProfile(Profile):
    """
    This class represents the equipment profile.

    :param reldir: Path relative to the system configuration directory
                   to store the yaml settings file.
    :param name: The name of the settings file **WITHOUT** the '.yaml' extension.

    Currently the settings stored are:
        * backend
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
    class Backend(ProfileSection):
        _sectionname: str = 'backend'
        #: Camera driver
        name: str = 'Not Set'

    @dataclass
    class Focuser(ProfileSection):
        # set some hopefully safe defaults
        _sectionname: str = 'focuser'
        # Backend (overrides backend specified in Backend section)
        backend: str = 'Not Set'
        #: Focuser driver
        driver: str = 'Not Set'
        #: Minimum allowed position for focuser
        minpos: int = 0
        #: Maximum allowed position for focuser
        maxpos: int = 0

    @dataclass
    class Camera(ProfileSection):
        _sectionname: str = 'camera'
        # Backend (overrides backend specified in Backend section)
        backend: str = 'Not Set'
        #: Camera driver
        driver: str = 'Not Set'

    @dataclass
    class Mount(ProfileSection):
        _sectionname: str = 'mount'
        # Backend (overrides backend specified in Backend section)
        backend: str = 'Not Set'
        #: Mount driver
        driver: str = 'Not Set'
        #: pier side reporting hint
        pierside_reporting: str = 'Not set'

    @dataclass
    class FilterWheel(ProfileSection):
        _sectionname: str = 'filterwheel'
        # Backend (overrides backend specified in Backend section)
        backend: str = 'Not Set'
        #: Filter wheel driver
        driver: str = 'Not Set'
        names: list = field(default_factory=list)

        @property
        def num_filters(self):
            return len(self.names)

    @dataclass
    class Telescope(ProfileSection):
        _sectionname: str = 'telescope'
        #: Focal length of telescope
        focal_length: int = 0
        #: Aperture of telescope
        aperture: int = 0
        #: Obstruction of telescope
        obstruction: int = 0

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)
        self.add_section(self.Backend)
        self.add_section(self.Focuser)
        self.add_section(self.Camera)
        self.add_section(self.Mount)
        self.add_section(self.FilterWheel)
        self.add_section(self.Telescope)
