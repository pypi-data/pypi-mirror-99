"""
Function interpolate_fdf

Given that this function is used very often,
its is written with the eye on fast execution
rather than modularity and good looks.

2020, September 4

"""

from math import floor, ceil


def interpolate_fdf(x, xs, ys, extrapolate=False, method='linear'):
    """
    Quickly interpolate a dataseries
    and return both interpolated value
    and its derivative.

    Arrays xs, ys can be Numpy arrays,
    yet any object that allows indexing can be used,
    such as Python lists.

    Method: linear or quadratic
    Search: bisection

    :param x: x value to interpolate at
    :param xs: x dataseries
    :param ys: y dataseries
    :param extrapolate: True or False
    :param method: 'linear' or 'quadratic'
    :return: f and df/dx, both evaluated at x
    """
    # Determine whether increasing or decreasing series
    direction = "increasing" if xs[-1] > xs[0] else "decreasing"

    lower = 0
    upper = len(xs) - 1

    if direction == "increasing":
        # Trivial cases and extrapolation
        if x < xs[0]:
            df = (ys[-1] - ys[0]) / (xs[-1] - xs[0])
            f = ys[0] + (x - xs[0]) * df if extrapolate else ys[0]
            return f, df
        elif x > xs[-1]:
            df = (ys[-1] - ys[0]) / (xs[-1] - xs[0])
            f = ys[-1] + (x - xs[-1]) * df if extrapolate else ys[-1]
            return f, df
        # Find index (bisection method)
        else:
            while upper > lower+1:
                mid = int((upper + lower) / 2)
                if x > xs[mid]:
                    lower = mid
                else:
                    upper = mid

    else:
        # Trivial cases and extrapolation
        if x > xs[0]:
            df = (ys[-1] - ys[0]) / (xs[-1] - xs[0])
            f = ys[0] + (x - xs[0]) * df if extrapolate else ys[0]
            return f, df
        elif x < xs[-1]:
            df = (ys[-1] - ys[0]) / (xs[-1] - xs[0])
            f = ys[-1] + (x - xs[-1]) * df if extrapolate else ys[-1]
            return f, df
        # Find index (bisection method)
        else:
            while upper > lower + 1:
                mid = int((upper + lower) / 2)
                if x > xs[mid]:
                    upper = mid
                else:
                    lower = mid

    # Perform interpolation on the curve segment
    if method.lower() == 'pchip':
        # Cubic hermite spline interpolation
        # derivatives at the endpoints of the interpolated interval
        if lower <= 0:
            df_start = (ys[1] - ys[0]) / (xs[1] - xs[0])
        else:
            df_start = (ys[upper] - ys[lower-1]) / (xs[upper] - xs[lower-1])
        if upper >= len(xs) - 1:
            df_end = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
        else:
            df_end = (ys[upper+1] - ys[lower]) / (xs[upper+1] - xs[lower])
        # normalized location along the interval
        t = (x - xs[lower]) / (xs[upper] - xs[lower])
        tb = 1-t
        # spline interpolation
        f = ys[lower] + (3*t**2 - 2*t**3) * (ys[upper] - ys[lower]) + \
            (xs[lower] - xs[upper]) * t * tb * (t*df_end - tb*df_start)
        # its derivative
        df = 1 / (xs[upper] - xs[lower]) * 6*t*tb * (ys[upper] - ys[lower]) + \
             t**2 * df_end + tb**2 * df_start - 2*t*tb*(df_end+df_start)
    else:
        # Linear interpolation
        df = (ys[upper] - ys[lower]) / (xs[upper] - xs[lower])
        f = ys[lower] + (x - xs[lower]) * df

    return f, df