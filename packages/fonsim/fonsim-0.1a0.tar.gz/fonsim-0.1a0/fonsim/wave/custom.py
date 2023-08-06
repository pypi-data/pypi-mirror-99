"""
Class CustomWave

2020, September 5

"""

import numpy as np

import scipy.interpolate


class Custom:
    def __init__(self, wave_array, time_notation='absolute', kind='previous'):
        """
        Custom wave

        Interpolation kinds: limited to those supported by scipy package.
        See https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html.
        From above site (copied 2020, September 5):
          Specifies the kind of interpolation as a string
          (‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’,
          where ‘zero’, ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline interpolation
          of zeroth, first, second or third order;
          ‘previous’ and ‘next’ simply return the previous or next value of the point)
          or as an integer specifying the order of the spline interpolator to use.

        :param wave_array: indexable object, size 2 x N
        :param time_notation: "absolute" (default) or "relative"
        :param kind: interpolation kind, default "previous" (left neighbour)
        """
        # Convert to numpy array if it isn't yet one
        if not isinstance(wave_array, np.ndarray):
            wave_array = np.array(wave_array)

        # Take transpose by default
        wave_array = wave_array.T

        # Look at shape of given wave series and transpose as necessary
        shape = np.shape(wave_array)
        if shape[0] != 2:
            wave_array = wave_array.T
        if shape[0] != 2:
            print("Error: wave_series shape does not seem to be compatible:\
            at least one dimension should have length two.")

        # Put in separate variable to ease handling
        times = wave_array[0, :]
        values = wave_array[1, :]

        # Convert given time series to absolute if relative
        if time_notation == 'relative':
            np.cumsum(times, out=times)

        # Preprocessing finished
        self.times = times
        self.values = values
        self.kind = kind

        # Interpolation function
        self.f = None
        self._update_interpolation_function()

    def _update_interpolation_function(self):
        """
        Update interpolation function
        :return: None
        """
        self.f = scipy.interpolate.interp1d(self.times, self.values, kind=self.kind, fill_value='extrapolate')

    def __call__(self, time):
        """
        Overload call operator to allow calling the object (using ())
        to read out the value.

        :param time: elapsed time, in s
        :return: interpolated value
        """
        return self.f(time)

    def __add__(self, other):
        """
        Add offset on y-values.
        :param other: y offset, float
        :return: modified object
        """
        # Update values
        self.values += other
        # Update interpolation function
        self._update_interpolation_function()
        return self

    def __mul__(self, other):
        """
        Multiply y-values
        :param other: y multiplier, float
        :return: modified object
        """
        # Update values
        self.values *= other
        # Update interpolation function
        self._update_interpolation_function()
        return self
