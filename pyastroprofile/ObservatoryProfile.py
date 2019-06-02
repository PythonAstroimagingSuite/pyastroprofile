#
# store observatory profiles
#

import astropy.units as u
from pyastroprofile.ProfileDict import Profile

from astroplan import Observer

class ObservatoryProfile(Profile):
    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        # define attributes for this profile
        # NOTE altitude is in meters
        self.obsname = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.timezone = None

    def to_dict(self):
        d ={}
        d['obsname'] = self.obsname
        d['latitude'] = self.latitude
        d['longitude'] = self.longitude
        d['altitude'] = self.altitude
        d['timezone'] = self.timezone
        return d

    def from_dict(self, d):
        self.obsname = d['obsname']
        self.latitude = d['latitude']
        self.longitude = d['longitude']
        self.altitude = d['altitude']
        self.timezone = d['timezone']

    def _data_complete(self):
        l = [self.obsname, self.latitude, self.longitude, self.altitude,
             self.timezone]
        return not (l.count(None) == 0)

    def __getattr__(self, attr):
        #logging.info(f'{self.__dict__}')
        # see if they are asking for observer which
        # we construct on the fly from 'real' config items
        if attr == 'observer':
            if self._data_complete():
                return Observer(longitude=self.longitude*u.deg,
                                latitude=self.latitude*u.deg,
                                elevation=self.altitude*u.m,
                                timezone=self.timezone,
                                name=self.obsname)
            else:
                return None
        else:
            return super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        #logging.info(f'setattr: {attr} {value}')
        # see if they are setting for observer which
        # we break into actual config items
        if attr == 'observer':
            self.obsname = value.name
            self.longitude = value.location.lat.degree
            self.latitude = value.location.lon.degree
            self.altitude = value.location.height.m
            self.timezone = value.timezone
        else:
            super().__setattr__(attr, value)
