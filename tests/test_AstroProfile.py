import os
import sys
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from pyastroprofile.ProfileDict import find_profiles, set_default_profile, get_default_profile
from pyastroprofile.AstroProfile import get_astroprofile_base_dir, AstroProfile
from pyastroprofile.EquipmentProfile import EquipmentProfile
from pyastroprofile.ObservatoryProfile import ObservatoryProfile
from pyastroprofile.SettingsProfile import SettingsProfile

FNAME='test_profile.yaml'
RELDIR = get_astroprofile_base_dir()

def create_section(section, name):
    return section(reldir=os.path.join(get_astroprofile_base_dir(), section._conf_rel_dir),
                   name=name)


if sys.argv[1] in ['write', 'defaultwrite']:
    if sys.argv[1] == 'write':
        fname = FNAME
    else:
        fname = None

    # create individual profiles
    eq = create_section(EquipmentProfile, fname)
    obs = create_section(ObservatoryProfile, fname)
    settings = create_section(SettingsProfile, fname)

    # populate
    eq.camera.driver = 'CCD Simulator'
    eq.mount.driver = 'Telescope Simulator'
    eq.focuser.driver = 'Focuser Simulator'
    eq.focuser.minpos = 5000
    eq.focuser.maxpos = 12000
    eq.filterwheel.driver = 'FilterWheel Simulator'
    eq.telescope.aperture = 100
    eq.telescope.focal_length = 600
    rc = eq.write()
    if not rc:
        logging.error('Failed to write equipment profile!')
        sys.exit(1)

    obs.location.obsname = 'Test Location'
    obs.location.latitude = 40.0
    obs.location.longitude = -80.0
    obs.location.altitude = 100.0
    obs.location.timezone = "US/Eastern"
    rc = obs.write()
    if not rc:
        logging.error('Failed to write observatory profile!')
        sys.exit(1)
    settings.platesolve.pixelscale = 1.0
    rc = settings.write()
    if not rc:
        logging.error('Failed to write settings profile!')
        sys.exit(1)

    ap = AstroProfile()
    ap.create_reference('test_astroprofile', fname, fname, fname)
    rc = ap.read('test_astroprofile')
    if not rc:
        logging.error('Failed to write reference file!')
        sys.exit(1)

    logging.info('ASTROPROFILE WRITTEN!')
    logging.info(f'ap = {ap}')

    rc = True

elif sys.argv[1] in ['read', 'defaultread']:
    if sys.argv[1] == 'read':
        fname = FNAME
    else:
        fname = None

    eq = EquipmentProfile(RELDIR, fname)

    rc = eq.read()
    logging.info(f'rc for read is {rc}')

    logging.info('read core info')
    logging.info(f'eq.camera.driver = {eq.camera.driver}')
    logging.info(f'eq.mount.driver = {eq.mount.driver}')
    logging.info(f'eq.focuser.driver = {eq.focuser.driver}')
    logging.info(f'eq.filterwheel.driver = {eq.filterwheel.driver}')

    logging.info(f'eq.camera = {eq.camera}')
    logging.info(f'eq.mount = {eq.mount}')
    logging.info(f'eq.focuser = {eq.focuser}')
    logging.info(f'eq.filterwheel = {eq.filterwheel}')
elif sys.argv[1] == 'setdefault':
    set_default_profile(RELDIR, FNAME)
elif sys.argv[1] == 'getdefault':
    d = get_default_profile(RELDIR)
    logging.info(f'default profile = {d}')
elif sys.argv[1] == 'resetdefault':
    set_default_profile(RELDIR, '')
elif sys.argv[1] == 'listprofiles':
    plist = find_profiles(RELDIR)
    logging.info(f'Found profiles for {RELDIR}')
    for p in plist:
        logging.info(f'   {p}')
