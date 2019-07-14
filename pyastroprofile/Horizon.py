# read horizon file
import numpy as np

class Horizon:

    def __init__(self):

        self.horizon_file = None
        self.horizon_table = None

    def readfile(self, horizon_file):
        with open(horizon_file, 'r') as f:
            alt_values = []
            az_values = []
            for l in f.readlines():
                az, alt = l.strip().split()
                az_values.append(float(az))
                alt_values.append(float(alt))

            self.horizon_table=(np.array(az_values), np.array(alt_values))
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
            h_alt = max(90, self.get_alt(az)+1)
            alt_arr[az, 0:int(h_alt)] = True

        return alt_arr

    def get_alt(self, az):
        # interpolate alt
        if self.horizon_table is None or len(self.horizon_table) < 1:
            return None
        return np.interp(az, self.horizon_table[0], self.horizon_table[1])