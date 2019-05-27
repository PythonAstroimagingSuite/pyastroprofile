import sys
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
from pyastroprofile.Profile import find_profiles, set_default_profile, get_default_profile
from pyastroprofile.EquipmentProfile import EquipmentProfile

RELDIR = 'testprofiles/equipment'
FNAME = 'test-equipment.ini'

if sys.argv[1] in ['write', 'defaultwrite']:
    if sys.argv[1] == 'write':
        fname = FNAME
    else:
        fname = None

    eq = EquipmentProfile(RELDIR, fname)

    eq.camera_driver = 'CCD Simulator'
    eq.telescope_driver = 'Telescope Simulator'
    eq.focuser_driver = 'Focuser Simulator'
    eq.filterwheel_driver = 'FilterWheel Simulator'
    eq.write()
elif sys.argv[1] in ['read', 'defaultread']:
    if sys.argv[1] == 'read':
        fname = FNAME
    else:
        fname = None

    eq = EquipmentProfile(RELDIR, fname)

    rc = eq.read()
    logging.info(f'rc for read is {rc}')

    logging.info('read core info')
    logging.info(f'eq.camera_driver = {eq.camera_driver}')
    logging.info(f'eq.telescope_driver = {eq.telescope_driver}')
    logging.info(f'eq.focuser_driver = {eq.focuser_driver}')
    logging.info(f'eq.filterwheel_driver = {eq.filterwheel_driver}')

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
