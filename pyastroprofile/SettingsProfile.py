#
# store observatory profiles
#
from dataclasses import dataclass, InitVar
from pyastroprofile.ProfileDict import Profile, ProfileSection

class SettingsProfile(Profile):
    """
    This class represents the program settings for the various
    programs involved in the imaging tool chain.  Anything settings
    specific to a particular hardware profile will be stored here.
    Settings which are not specific to a hardware profile but are
    instead global to all profile (like the path to an executable)
    will be stored in a settings file specific to the particular
    program.

    :param reldir: Path relative to the system configuration directory
                   to store the yaml settings file.
    :param name: The name of the settings file **WITHOUT** the '.yaml' extension.

    Currently the settings stored are:
        * platesolve
        * autofocus

    Access is done as follows::

        from pyastroprofile.SettingsProfile import SettingsProfile
        sp = SettingsProfile(reldir='settings', name='mysettings')
        sp.read()
        print('pixelscale is ', sp.platesolve.pixelscale)
        print('focus direction is ', sp.autofocus.focus_dir)
        sp.platesolve.pixelscale = 3.0
        sp.write()

    This example will create the file '<system config dir>/settings/mysettings.yaml'

    **NOTE**: It is recommended to use the :class:`AstroProfile` class for
    accessing these settings as it includes the :class:`SettingsProfile` class.

    """

    # where this should go under astroprofile directory hierarchy
    _conf_rel_dir = 'settings'

    @dataclass
    class PlateSolveSettings(ProfileSection):
        """This class stores settings related to plate solving
        for a particular hardware setting.

        :var pixelscale: pixel scale in arcseconds/pixel
        :var prefer_filter: preferred filter for solving
        """
        pixelscale : float = 5.7
        prefer_filter : str = None

        # name of section in YAML output and attribute name
        _sectionname : str = 'platesolve'

    @dataclass
    class GuiderSettings(ProfileSection):
        """This class stores settings related to guiding
        for a particular hardware setting.

        :var pixelscale: pixel scale in arcseconds/pixel
        """
        dither_size_pixels : float = 3.0
        dither_settle_pixels : float = 0.5
        dither_settle_time : float = 10.0
        dither_settle_timeout : float = 60.0
        dither_operation_timeout : float = 90.0

        guide_settle_pixels : float = 0.5
        guide_settle_time : float = 10.0
        guide_settle_timeout : float = 60.0
        guide_operation_timeout : float = 90.0

        # name of section in YAML output and attribute name
        _sectionname : str = 'guider'

    @dataclass
    class AutoFocusSettings(ProfileSection):
        """This class stores settings related to autofocus
        for a particular hardware setting.
        """

#        :var start_hfr: Desired HFR which focus run starts at
#        :var near_hfr: HFR used for determining final focus
#        :var focus_delay: Delay (seconds) after a focus move
#        :var focus_dir: Direction ('IN' or 'OUT') of focus run
#        :var exposure_start: Starting exposure time (seconds)
#        :var exposure_max: Maximum exposure time (seconds) allowed
#        :var exposure_min: Minimum exposure time (seconds) allowed
        start_hfr : float = 25.0
        near_hfr : float = 12.0
        focus_delay : float = 0.0
        focus_dir : str = 'IN'
        exposure_start : float = 1.0
        exposure_max : float = 8.0
        exposure_min : float = 0.5
        star_mag_for_filter : dict = {}

        # name of section in YAML output and attribute name
        _sectionname : str = 'autofocus'

        def preferred_star_mag(self, filter_name):
            mag = self.star_mag_for_filter.get(filter_name, None)
            return mag

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        # create sections for settings
        self.add_section(self.PlateSolveSettings)
        self.add_section(self.AutoFocusSettings)
        self.add_section(self.GuiderSettings)
