#
# Test case
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
#
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

    logging.info(f'DICT = {s.__dict__}')

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
