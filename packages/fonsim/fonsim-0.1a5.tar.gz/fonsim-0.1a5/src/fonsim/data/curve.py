"""
Class to ease working with PV- and PN-curves

2020, September 1

"""

from . import dataseries


class Curve:
    def __init__(self, data):
        """
        Class to ease working with pv- and pn-curves

        :param data: filepath to CSV file or DataSeries-like object
        """
        # Allow passing filepaths
        if isinstance(data, str):
            self.data = dataseries.DataSeries(data)
        else:
            self.data = data
