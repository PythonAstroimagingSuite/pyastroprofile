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

    eq.camera.driver = 'CCD Simulator'
    eq.mount.driver = 'Telescope Simulator'
    eq.focuser.driver = 'Focuser Simulator'
    eq.filterwheel.driver = 'FilterWheel Simulator'
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
