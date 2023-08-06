"""
Ease unit conversion operations
Uses a JSON file 'unitconversions.json' with the actual unit conversions

2020, September 4

"""

import json
import pkgutil

from conversion import indexmatch

# Filename of unit conversions configuration file
filepath = 'resources/unitconversions.json'

# Load JSON file
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
s = pkgutil.get_data('fonsim', filepath)
unitconversions = json.loads(s)


# The read function
def get_unit_multiplier(label, space):
    """
    Get unit multiplier for a particular unit.
    Conversions are defined in file 'unitconversions.json'.

    :param label: unit label, e.g. "mbar" or "cm^3"
    :param space: unit space, e.g. "pressure" or "volume"
    :return: multiplication factor
    """
    # Get best space
    candidates = list(unitconversions.keys())
    i = indexmatch.get_index_of_best_match(space, candidates)
    space_best = candidates[i]

    # Get best unit
    candidates = list(unitconversions[space_best])
    i = indexmatch.get_index_of_best_match(label, candidates)
    k = candidates[i]

    return unitconversions[space_best][k]
