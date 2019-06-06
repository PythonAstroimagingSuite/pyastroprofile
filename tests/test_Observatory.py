import sys
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
from pyastroprofile.Profile import find_profiles, set_default_profile, get_default_profile
from pyastroprofile.ObservatoryProfile import ObservatoryProfile

if sys.argv[1] in ['write', 'defaultwrite']:
    if sys.argv[1] == 'write':
        fname = 'test-observatory.yaml'
    else:
        fname = None

    obs = ObservatoryProfile('testprofiles', fname)

    obs.location.latitude = 35.8
    obs.location.longitude = -78.8
    obs.location.altitude = 100.0
    obs.location.timezone = "US/Eastern"
    obs.write()
elif sys.argv[1] in ['read', 'defaultread']:
    if sys.argv[1] == 'read':
        fname = 'test-observatory'
    else:
        fname = None

    obs = ObservatoryProfile('testprofiles', fname)

    rc = obs.read()
    logging.info(f'rc for read is {rc}')

    logging.info('read core info')
    logging.info(f'obs.location.obsname = {obs.location.obsname}')
    logging.info(f'obs.location.longitude = {obs.location.longitude}')
    logging.info(f'obs.location.latitude = {obs.location.latitude}')
    logging.info(f'obs.location.altitude = {obs.location.altitude}')

    logging.info('Dervied quantities:')
    logging.info(f'obs.observer = {obs.observer}')
elif sys.argv[1] == 'setdefault':
    set_default_profile('testprofiles', 'test-observatory.ini')
elif sys.argv[1] == 'getdefault':
    d = get_default_profile('testprofiles')
    logging.info(f'default profile = {d}')
elif sys.argv[1] == 'resetdefault':
    set_default_profile('testprofiles', '')
elif sys.argv[1] == 'listprofiles':
    plist = find_profiles('testprofiles')
    logging.info(f'Found profiles for testprofiles')
    for p in plist:
        logging.info(f'   {p}')
