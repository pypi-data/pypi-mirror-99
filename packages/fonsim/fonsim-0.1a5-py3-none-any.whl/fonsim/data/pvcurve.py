"""
Class to ease working with pv-curves

2020, September 4

"""

import numpy as np

from . import curve
from . import interpolate
from fonsim.conversion import indexmatch
from fonsim.conversion import unitconversion as uc
import fonsim.constants.norm as cnorm


class PVCurve(curve.Curve):
    def __init__(self, data, pressure_reference="relative", autocorrect=False,
                 **interpolation_opts):
        """
        Class to ease working with pv-curves

        Warning: original data in DataSeries object may be modified by this function.
        Take a deepcopy if modification undesirable.

        :param data: filepath to CSV file or DataSeries-like object
        :param pressure_reference: "relative" or "absolute"
        :param autocorrect: True or False
        :param interpolation_opts: kwargs for interpolation function
        """
        curve.Curve.__init__(self, data)
        self.interpolation_opts = interpolation_opts

        # Look which labels match best with those in dataseries object
        i_v = indexmatch.get_index_of_best_match("volume", self.data.labels)
        i_p = indexmatch.get_index_of_best_match("pressure", self.data.labels)

        # Load data
        self.v = self.data.array[:, i_v]
        self.p = self.data.array[:, i_p]

        # Unit conversions to SI
        self.v *= uc.get_unit_multiplier(self.data.units[i_v], "volume")
        self.p *= uc.get_unit_multiplier(self.data.units[i_p], "pressure")

        # To absolute pressure
        if pressure_reference == "relative":
            self.p += cnorm.pressure_atmospheric
        elif pressure_reference == "absolute":
            pass
        else:
            print("Error: pressure reference not recognized.")

        # Autocorrect
        if autocorrect:
            # Volume offset to zero
            self.v -= np.min(self.v)
            # Pressure offset to zero
            self.p -= (np.min(self.p) - cnorm.pressure_atmospheric)

        # Add dataseries for compressible fluid, aka normalvolume or nv
        # Use ideal gas gaw for conversion.
        self.nv = np.multiply(self.v, self.p/cnorm.pressure_atmospheric)

    def get_initial_volume(self, p0):
        """
        Get the volume of the first datapoint on the curve that
        approaches the provided pressure value the closest

        :param p0: pressure at which to find the first matching volume
        :return: first closest matching volume
        """
        i0 = 0
        for i in range(len(self.p)-1):
            # check if p0 is crossed
            if self.p[i] <= p0 <= self.p[i+1] or \
               self.p[i] >= p0 >= self.p[i+1]:
                # linear interpolation
                slope = (self.v[i+1]-self.v[i]) / (self.p[i+1]-self.p[i])
                return self.v[i] + slope*(p0-self.p[i])
            # keep a record of the index that approaced p0 the closest in
            # case no crossing with p0 is found
            if abs(p0-self.p[i]) < abs(p0-self.p[i0]):
                i0 = i
        return self.v[i0]

    def fdf_volume(self, volume):
        """
        Readout for incompressible fluids

        :param volume: volume in [m3]
        :return: f, df
        """
        return interpolate.interpolate_fdf(volume, self.v, self.p,
                                           **self.interpolation_opts)

    def fdf_normalvolume(self, normalvolume):
        """
        Readout for compressible fluids
        Relation to normalvolume via ideal gas law

        :param normalvolume: normal volume ("free volume") in [m3]
        :return: f, df
        """
        return interpolate.interpolate_fdf(normalvolume, self.nv, self.p,
                                           **self.interpolation_opts)

    def __str__(self):
        #txt = "PCurve object"
        txt = self.__repr__()
        txt += "\n  Number of datapoints:             " + str(len(self.v))
        txt += "\n  Maximum relative pressure [bar]:  " + str((max(self.p)-cnorm.pressure_atmospheric)/uc.get_unit_multiplier("bar", "pressure"))
        txt += "\n  Maximum volume [ml]:              " + str(max(self.v)/uc.get_unit_multiplier("ml", "volume"))
        txt += "\n  Maximum normalvolume [ml]:        " + str(max(self.nv)/uc.get_unit_multiplier("ml", "volume"))
        txt += "\n  Minimum relative pressure [bar]:  " + str((min(self.p)-cnorm.pressure_atmospheric)/uc.get_unit_multiplier("bar", "pressure"))
        txt += "\n  Minimum volume [ml]:              " + str(min(self.v)/uc.get_unit_multiplier("ml", "volume"))
        txt += "\n  Minimum normalvolume [ml]:        " + str(min(self.nv)/uc.get_unit_multiplier("ml", "volume"))
        return txt
