#
# Local horizon
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
import numpy as np

class Horizon:

    def __init__(self):

        self.horizon_file = None
        self.horizon_table = None

    def readfile(self, horizon_file):
        with open(horizon_file, 'r') as f:
            alt_values = []
            az_values = []
            for line in f.readlines():
                az, alt = line.strip().split()
                az_values.append(float(az))
                alt_values.append(float(alt))

            self.horizon_table = (np.array(az_values), np.array(alt_values))
            self.horizon_file = horizon_file
            return True

        # failed
        return None

    # makes a 360 x 90 array with a value of 1 below horizon
    # first index is az and second is alt
    def create_horizon_map(self):
        alt_arr = np.empty((360, 90)).astype(bool)
        alt_arr.fill(False)
        for az in range(0, 360):
            # round up to make sure we dont give false positives
            # that an object has cleared horizon
            h_alt = min(90, self.get_alt(az) + 1)
            alt_arr[az, 0:int(h_alt)] = True

        return alt_arr

    def get_alt(self, az):
        # interpolate alt
        if self.horizon_table is None or len(self.horizon_table) < 1:
            return None
        return np.interp(az, self.horizon_table[0], self.horizon_table[1])
