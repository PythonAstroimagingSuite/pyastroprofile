#
# store observatory profiles
#
from dataclasses import dataclass
import astropy.units as u
from pyastroprofile.ProfileDict import Profile, ProfileSection
from astroplan import Observer

class ObservatoryProfile(Profile):
    # where this should go under astroprofile directory hierarchy
    _conf_rel_dir = 'observatories'

    @dataclass
    class Location(ProfileSection):
        _sectionname : str = 'location'
        # NOTE altitude is in meters
        obsname : str = None
        latitude : float = None
        longitude : float = None
        altitude : float = None
        timezone : float = None

    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        self.add_section(self.Location)

    def _data_complete(self):
        l = [self.location.obsname,
             self.location.latitude,
             self.location.longitude,
             self.location.altitude,
             self.location.timezone]
        return not (l.count(None) == 0)

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

#    def to_dict(self):
#        d ={}
#        d['obsname'] = self.obsname
#        d['latitude'] = self.latitude
#        d['longitude'] = self.longitude
#        d['altitude'] = self.altitude
#        d['timezone'] = self.timezone
#        return d
#
#    def from_dict(self, d):
#        self.obsname = d['obsname']
#        self.latitude = d['latitude']
#        self.longitude = d['longitude']
#        self.altitude = d['altitude']
#        self.timezone = d['timezone']
