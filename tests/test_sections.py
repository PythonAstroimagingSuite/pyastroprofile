#
# store equipment profiles
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




