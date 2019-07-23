#
# store observatory profiles
#
import os
import logging
from dataclasses import dataclass
import astropy.units as u
from astroplan import Observer

from pyastroprofile.ProfileDict import Profile, ProfileSection

from pyastroprofile.Horizon import Horizon

class ObservatoryProfile(Profile):
    """
    This class represents the observing location including
    geographical and time relating settings.

    :param reldir: Path relative to the system configuration directory
                   to store the yaml settings file.
    :param name: The name of the settings file **WITHOUT** the '.yaml' extension.

    Currently the parameter stored is:
        * location

    Access is done as follows::

        from pyastroprofile.ObservatoryProfile import ObservatoryProfile
        op = ObservatoryProfile(reldir='observatories', name='myobservatory')
        op.read()
        print('latitude is ', op.location.latitude)
        op.location.altitude = 300.0
        sp.write()

    This example will create the file '<system config dir>/observatories/myobservatory.yaml'

    **NOTE**: It is recommended to use the :class:`AstroProfile` class for
    accessing these settings as it includes the :class:`ObservatoryProfile` class.

    """

    # where this should go under astroprofile directory hierarchy
    _conf_rel_dir = 'observatories'

    @dataclass
    class Location(ProfileSection):
        _sectionname : str = 'location'
        #: Name of observing location
        obsname : str = None
        #: Latitude in degrees
        latitude : float = None
        #: Longitude in degrees
        longitude : float = None
        #: Altitude in meters
        altitude : float = None
        #: Timezone string
        timezone : str = None
        #: Horizon definition
        horizon_file : str = None

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        self.add_section(self.Location)

        # load horizon file and store so it is not saved in dict
        self._horizon = Horizon()

    def read(self):
        # load in profile
        super().read()

        # now try to load horizon file
        if self.location.horizon_file is not None:
            logging.debug(f'ObservatoryProfile: horizon file = {self.location.horizon_file}')

            # if horizon file specification does not have a leading
            # directory specification assume it is in the 'astroprofiles/observatories'
            # directory
            if os.path.dirname(self.location.horizon_file) == '':
                hzn_dir =  self._get_config_dir()
            else:
                hzn_dir = ''
            hzn_file = os.path.join(hzn_dir, self.location.horizon_file)
            logging.debug(f'loading horizon file {hzn_file}')
            rc = self._horizon.readfile(hzn_file)
            if not rc:
                logging.error('ObservatoryProfile: Unable to load horizon!')
            return rc

    def _data_complete(self):
        l = [self.location.obsname,
             self.location.latitude,
             self.location.longitude,
             self.location.altitude,
             self.location.timezone]
        return (l.count(None) == 0)

    def __getattr__(self, attr):
        #logging.info(f'{self.__dict__}')
        # see if they are asking for observer which
        # we construct on the fly from 'real' config items
        if attr == 'observer':
            if self._data_complete():
                return Observer(longitude=self.location.longitude*u.deg,
                                latitude=self.location.latitude*u.deg,
                                elevation=self.location.altitude*u.m,
                                timezone=self.location.timezone,
                                name=self.location.obsname)
            else:
                return None
        elif attr == 'horizon':
            return self._horizon
        else:
            return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        #logging.info(f'setattr: {attr} {value}')
        # see if they are setting for observer which
        # we break into actual config items
        if attr == 'observer':
            self.location.obsname = value.name
            self.location.longitude = value.location.lat.degree
            self.location.latitude = value.location.lon.degree
            self.location.altitude = value.location.height.m
            self.location.timezone = value.timezone
        else:
            super().__setattr__(attr, value)
