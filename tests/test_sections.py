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

from pyastroprofile.Profile import Profile#, Section

class SectionsProfile(Profile):
    def __init__(self, reldir, name=None):
        super().__init__(reldir, name)

        self.key1 = None
        self.key2 = None
        self.focuser = { 'key' : '1' }
        self.tree = {}
        self.tree.branch = 2

        print(self._config)
        print(dir(self._config['focuser']))
        print(self._config['focuser'])
        print(vars(self._config['focuser'].dict))
        #self.focuser.minpos = 1
        #self.focuser.maxpos = 10
        #self.focuser.prefdir = 'IN'
        #self.focuser.section = Section()
        #self.focuser.section.key = 4




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    s = SectionsProfile('test-profiles', 'test-sections.ini')
#    logging.info(f'{s.focuser.minpos}')
#    logging.info(f'{s.focuser.maxpos}')
#    logging.info(f'{s.focuser.prefdir}')
    logging.info(f'{s.focuser.key}')

    print(s.tree.branch.leaf)

    s.write()




