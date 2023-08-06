"""
Class to load and hold tabular data from CSV file

Numerical data is stored in numpy arrays as floats.
Labels and units are stored in Python lists

2020, September 1

"""

import numpy as np
import csv


class DataSeries:
    def __init__(self, filename, bytestring=None):
        """
        DataSeries class
        To load and hold tabular data from CSV file

        :param filename: path to file to read or, if bytestring given, filetype
        :param bytestring: bytestring with file data
        """
        self.labels = []
        self.units = []
        self.array = np.array(0)

        # Load data from file into labels, units and data
        self.load_data(filename, bytestring)

    def load_data(self, filename, bytestring=None):
        """
        Load in data. Provide a filename or byte string.
        If providing a byte string, provide the filetype extension (e.g. .csv)
        to the filename argument such that the formatting of the bytestring can be determined.

        :param filename: path to file to read or, if bytestring given, filetype
        :param bytestring: bytestring with file data
        :return: None
        """
        # Check whether CSV file (.csv)
        if '.csv' in filename:
            # CSV files cannot store numbers directly:
            # they can only store strings of characters,
            # typically representing numbers in decimal format.
            # Thus, we'll first load in the strings in a 2D Python list structure
            # and then convert those strings to floats.

            # Get file contents
            if bytestring is not None:
                csvfile = bytestring.decode('utf-8')
            else:
                f = open(filename, 'r', newline='')
                csvfile = f.read()
                f.close()
            csvfile = csvfile.splitlines()

            # CSV file contents to Python lists
            data = []
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            i_all_floats = -1
            i = 0
            for row in reader:
                data.append(row)
                if i_all_floats == -1:
                    try:
                        [float(x) for x in row]
                        i_all_floats = i
                    except ValueError:
                        pass
                    i += 1

            # Data shape
            width = len(data[i_all_floats])

            # Labels and units
            # No top labels -> this can get difficult!
            if i_all_floats == 0:
                print("Note: No labels detected! Applied automatic labeling")
                self.labels = [str(x) for x in range(width)]
            elif i_all_floats == 1:
                self.labels = data[0]
            else:
                self.labels = data[i_all_floats-2]
                self.units = data[i_all_floats-1]

            # Convert to Numpy array floats
            self.array = np.array(data[i_all_floats:], dtype=np.float32)

        else:
            print("ERROR: The given filename '", filename, "' is not recognized as a readable file.")
            print("       Only .csv files are currently supported.")
