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
from pyastroprofile.EquipmentProfile import EquipmentProfile

RELDIR = 'testprofiles/equipment'
FNAME = 'test-equipment.yaml'

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
    eq.filterwheel.names = ['L', 'R', 'G', 'B', 'Ha', 'OIII', 'SII', 'Dark']
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
    logging.info(f'n filters      = {eq.filterwheel.num_filters}')
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
