import sys
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
from pyastroprofile.Profile import find_profiles, set_default_profile, get_default_profile
from pyastroprofile.SettingsProfile import SettingsProfile

if sys.argv[1] in ['write', 'defaultwrite']:
    if sys.argv[1] == 'write':
        fname = 'test-settings.ini'
    else:
        fname = None

    s = SettingsProfile('testprofiles', fname)

    s.write()
elif sys.argv[1] in ['read', 'defaultread']:
    if sys.argv[1] == 'read':
        fname = 'test-settings.ini'
    else:
        fname = None

    s = SettingsProfile('testprofiles', fname)
    rc = s.read()
    logging.info(f'rc for read is {rc}')
    logging.info('read core info')
    logging.info(f's = {s}')
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
