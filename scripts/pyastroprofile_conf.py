#
# Test code
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
import os
import sys
import argparse
import logging

from pyastroprofile.AstroProfile import get_astroprofile_base_dir
from pyastroprofile.AstroProfile import AstroProfile
from pyastroprofile.EquipmentProfile import EquipmentProfile
from pyastroprofile.ObservatoryProfile import ObservatoryProfile
from pyastroprofile.SettingsProfile import SettingsProfile

# FIXME this should be something globally configured!
#ASTROPROFILE_ROOT_RELDIR = 'astroprofiles'

# FIXME probably better to not have to reference '_' attr to get rel dir!
class_map = {
              EquipmentProfile._conf_rel_dir : EquipmentProfile,
              ObservatoryProfile._conf_rel_dir : ObservatoryProfile,
              SettingsProfile._conf_rel_dir : SettingsProfile
            }

def get_reldir(subpath):
    return os.path.join(get_astroprofile_base_dir(), subpath)

def parse_class():
    logging.debug('parse_class()')
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd_class', type=str, help='Profile class for command')
    if len(sys.argv) < 2:
        parser.print_help()
    args = parser.parse_args(sys.argv[1:2])

    return args.cmd_class

def parse_command():
    logging.debug('parse_command()')
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, help='Profile class for command')
    args, unknown = parser.parse_known_args(sys.argv[2:3])
    return args.command

def write_template(cmd_class):
    logging.debug('write_template()')
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Filename for template file')
    args, unknown = parser.parse_known_args(sys.argv[3:4])

    # create profile object for requested class
    obj = class_map[cmd_class](reldir=None, name=args.filename)
    logging.info(f'obj = {obj}')
    logging.info(f'obj.sections = {obj.sections}')
    obj.write()

    return True

def show_profile(cmd_class):
    logging.debug('show_profile()')
    parser = argparse.ArgumentParser()
    parser.add_argument('profile', type=str, help='Profile to show')
    args, unknown = parser.parse_known_args(sys.argv[3:4])

    # create profile object for requested class
    # FIXME should have method to construct filename without knowing
    #       path subcomponents and extension!
    reldir = get_reldir(cmd_class)
    obj = class_map[cmd_class](reldir=reldir, name=args.profile+'.yaml')
    obj.read()
    logging.info(f'Profile = {obj}')

    return True

def show_astroprofile():
    logging.debug('show_astroprofile()')
    parser = argparse.ArgumentParser()
    parser.add_argument('profile', type=str, help='Profile to show')
    args, unknown = parser.parse_known_args(sys.argv[3:4])
    ap = AstroProfile()
    ap.read(args.profile)
    logging.info(f'AstroProfile = {ap}')

    return True

#    parser.add_argument('list_profiles', type=str, help='List profiles for class')
#    parser.add_argument('write_template', type=str, help='Write template for class')
#    parser.add_argument('show_profile', type=str, help='Show a profile for class')
#    parser.add_argument('set_default', type=str, help='Set default profile for class')
#    parser.add_argument('reset_default', type=str, help='Reset default profile for class')

if __name__ == '__main__':
    logging.basicConfig(filename='pyastroprofile_conf.log',
                        filemode='w',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # add to screen as well
    LOG = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    CH = logging.StreamHandler()
    CH.setLevel(logging.DEBUG)
    CH.setFormatter(formatter)
    LOG.addHandler(CH)

    logging.info(f'pyastroprofile_conf starting')

    # several commands
    #
    # pyastroprofile_conf <profile class> <command>
    #
    # where:
    #   <profile class>  can be 'equipment', 'observatories', 'settings, astroprofile'
    #
    # For all profile classes EXCEPT 'astroprofile' command can be:
    #
    # write_template  <fname>    writes out a template file to profile class
    # show_profile <name>        dumps profile <name> from standard location with name
    # set_default <name>         sets profile <name> as default
    # list_profiles              list all profiles
    # reset_default              removes default for profile class
    #
    # For 'astroprofile' the commands are:
    #
    # show_profile <name>        show astroprofile <name>

    cmd_class = parse_class()

    rc = None

    if cmd_class != 'astroprofile':
        cmd = parse_command()

        if cmd == 'write_template':
            rc = write_template(cmd_class)
        elif cmd == 'show_profile':
            rc = show_profile(cmd_class)
    else:
        cmd = parse_command()
        if cmd == 'show_profile':
            rc = show_astroprofile()

    if rc:
        logging.info('Operation sucessful')
        sys.exit(0)
    else:
        logging.info('Operation failed')
        sys.exit(1)




