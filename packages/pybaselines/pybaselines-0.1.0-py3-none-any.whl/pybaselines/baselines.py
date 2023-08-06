# -*- coding: utf-8 -*-
"""High level functions for .


Created on March 3, 2021
@author: Donald Erb

"""

import warnings

import numpy as np

from .morphological import mpls
from .penalized_least_squares import iarpls, airpls, arpls, asls, aspls, drpls, iasls
from .polynomial import imodpoly, modpoly, poly
from .utils import gaussian, _setup_polynomial


def manual_baseline(x_data, baseline_points=()):
    """
    Creates a linear baseline constructed from points.

    Parameters
    ----------
    x_data : array-like, shape (N,)
        The x-values of the measured data.
    baseline_points : Iterable(Container(float, float))
        An iterable of ((x_1, y_1), (x_2, y_2), ..., (x_n, y_n)) values for
        each point representing the baseline. Must be at least two points
        to have a non-zero baseline.

    Returns
    -------
    z : numpy.ndarray, shape (N,)
        The baseline array constructed from connecting line segments between
        each background point.
    dict
        An empty dictionary, just to match the output of all other algorithms.

    Warns
    -----
    UserWarning
        Raised if there are less than two points in baseline_points.

    Notes
    -----
    Assumes the background is represented by lines connecting each of the
    specified background points.

    """
    x = np.asarray(x_data)
    z = np.zeros(x.shape[0])
    if len(baseline_points) < 2:
        warnings.warn('there must be at least 2 background points to create a baseline')
    else:
        points = sorted(baseline_points, key=lambda p: p[0])
        for i in range(len(points) - 1):
            x_points, y_points = zip(*points[i:i + 2])
            segment = (x >= x_points[0]) & (x <= x_points[1])
            z[segment] = np.linspace(*y_points, x[segment].shape[0])

    return z, {}


def collab_pls(data, average_dataset=True, method='asls', **method_kwargs):
    """
    Collaborative Penalized Least Squares (collab-PLS).

    Averages the data or the fit weights for an entire dataset to get more
    optimal results.

    Parameters
    ----------
    data : array-like, shape (M, N)
        An array with shape (M, N) where M is the number of entries in
        the dataset and N is the number of data points in each entry.
    average_dataset : bool
        If True (default) will average the dataset before fitting to get the
        weighting. If False, will fit each individual entry in the dataset and
        then average the weights to get the weighting for the dataset.
    method : {}
        [description], by default 'asls'
    full : bool
        If True, will return the weights along with the baselines.
    **method_kwargs

    Returns
    -------
    np.ndarray, shape (M, N)
        An array of all of the baselines.

    References
    ----------
    Chen, L. et al. Collaborative Penalized Least Squares for Background
    Correction of Multiple Raman Spectra. Journal of Analytical Methods
    in Chemistry, 2018, 2018, DOI:https://doi.org/10.1155/2018/9031356.

    """
    fit_func = {
        'arpls': arpls,
        'aspls': aspls,
        'iarpls': iarpls,
        'airpls': airpls,
        'mpls': mpls,
        'asls': asls,
        'iasls': iasls,
        'drpls': drpls
    }[method.lower()]
    dataset = np.asarray(data)
    if average_dataset:
        _, fit_params = fit_func(np.mean(dataset.T, 1), **method_kwargs)
        method_kwargs['weights'] = fit_params['weights']
    else:
        weights = []
        for entry in dataset:
            _, fit_params = fit_func(entry, **method_kwargs)
            weights.append(fit_params['weights'])
        method_kwargs['weights'] = np.mean(np.transpose(weights), 1)

    method_kwargs['tol'] = np.inf
    baselines = []
    for entry in dataset:
        baselines.append(fit_func(entry, **method_kwargs))

    return np.vstack(baselines), {'weights': method_kwargs['weights']}


def _iter_solve(func, fit_data, known_background, lower_bound, upper_bound, variable,
                min_value, max_value, step=1, allowed_misses=1, **func_kwargs):
    """Iterates through possible values to find the one with lowest root-mean-square-error."""
    min_rmse = np.inf
    misses = 0
    for var in np.arange(min_value, max_value, step):
        if variable == 'lam':
            func_kwargs[variable] = 10**var
        else:
            func_kwargs[variable] = var
        baseline = func(fit_data, **func_kwargs)[0]
        #TODO change the known baseline so that np.roll does not have to be
        # calculated each time, since it requires additional time
        rmse = np.sqrt(np.mean(
            (known_background - np.roll(baseline, upper_bound)[:upper_bound + lower_bound])**2
        ))
        if rmse < min_rmse:
            z = baseline[lower_bound:baseline.shape[0] - upper_bound]
            min_var = var
            misses = 0
            min_rmse = rmse
        else:
            misses += 1
            if misses > allowed_misses:
                break

    return z, min_var


def optimize_parameter(data, x_data=None, method='aspls', side='left', **method_kwargs):
    """
    Finds the best parameter value for the given baseline method.

    Useful for calculating the optimum `lam` or `poly_degree` value required
    to optimize other algorithms.

    Notes
    -----
    Based on the extended range penalized least squares (erPLS) method from [1]_.
    The method proposed by [1]_ was for optimizing lambda only for the aspls
    method by extending only the right side of the spectrum. The method was
    modified by allowing extending either side following [2]_, and for optimizing
    lambda or the polynomial degree for all of the affected algorithms in
    pybaselines.

    References
    ----------
    .. [1] Zhang, F., et al. An Automatic Baseline Correction Method Based on
           the Penalized Least Squares Method. Sensors, 2020, 20(7), 2015.
    .. [2] Krishna, H, et al. Range-independent background subtraction algorithm
           for recovery of Raman spectra of biological tissue. Journal of Raman
           Spectroscopy. 2012, 43(12), 1884-1894.

    """
    if side.lower() not in ('left', 'right', 'both'):
        raise ValueError('side must be "left", "right", or "both"')
    fit_func = {
        'arpls': arpls,
        'aspls': aspls,
        'iarpls': iarpls,
        'airpls': airpls,
        'mpls': mpls,
        'asls': asls,
        'iasls': iasls,
        'drpls': drpls,
        'modpoly': modpoly,
        'imodpoly': imodpoly,
        'poly': poly
    }[method.lower()]

    y, x, *_ = _setup_polynomial(data, x_data)
    sort_order = tuple(enumerate(np.argsort(x)))  # to ensure x is increasing
    x = x[[val[1] for val in sort_order]]
    y = y[[val[1] for val in sort_order]]
    max_x = np.nanmax(x)
    min_x = np.nanmin(x)
    x_range = max_x - min_x
    known_background = np.array([])
    fit_x_data = x
    fit_data = y
    lower_bound = upper_bound = 0

    W = x.shape[0] // 10

    if side.lower() in ('right', 'both'):
        added_x = np.linspace(max_x, max_x + x_range / 5, W)
        line = np.polynomial.Polynomial.fit(
            x[x > max_x - x_range / 20], y[x > max_x - x_range / 20], 1
        )(added_x)
        gaus = gaussian(added_x, np.nanmax(y), np.median(added_x), x_range / 50)
        fit_x_data = np.hstack((fit_x_data, added_x))
        fit_data = np.hstack((fit_data, gaus + line))
        known_background = line
        upper_bound += W
    if side.lower() in ('left', 'both'):
        added_x = np.linspace(min_x - x_range / 5, min_x, W)
        line = np.polynomial.Polynomial.fit(
            x[x < min_x + x_range / 20], y[x < min_x + x_range / 20], 1
        )(added_x)
        gaus = gaussian(added_x, np.nanmax(y), np.median(added_x), x_range / 50)
        fit_x_data = np.hstack((added_x, fit_x_data))
        fit_data = np.hstack((gaus + line, fit_data))
        known_background = np.hstack((known_background, line))
        lower_bound += W

    if method.lower() in ('iasls', 'modpoly', 'imodpoly', 'poly'):
        method_kwargs['x_data'] = fit_x_data

    if method.lower() in ('modpoly', 'imodpoly', 'poly'):
        z, best_val = _iter_solve(
            fit_func, fit_data, known_background, lower_bound, upper_bound, 'poly_order',
            0, 20, 1, 4, **method_kwargs
        )
    else:
        _, best_val = _iter_solve(
            fit_func, fit_data, known_background, lower_bound, upper_bound, 'lam',
            1, 50, 1, 2, **method_kwargs
        )
        z, best_val = _iter_solve(
            fit_func, fit_data, known_background, lower_bound, upper_bound, 'lam',
            best_val - 0.9, best_val + 1.1, 0.1, 2, **method_kwargs
        )

    return (
        z[[val[0] for val in sorted(sort_order, key=lambda v: v[1])]],
        {'optimal_parameter': best_val}
    )
