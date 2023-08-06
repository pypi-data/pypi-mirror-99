# -*- coding: utf-8 -*-

import numpy as np

from brainpy import backend

__all__ = [
    'constant_current',
    'spike_current',
    'ramp_current',
]


def constant_current(Iext, dt=None):
    """Format constant input in durations.

    For example:

    If you want to get an input where the size is 0 bwteen 0-100 ms,
    and the size is 1. between 100-200 ms.
    >>> constant_current([(0, 100), (1, 100)])
    >>> constant_current([(np.zeros(100), 100), (np.random.rand(100), 100)])

    Parameters
    ----------
    Iext : list
        This parameter receives the current size and the current
        duration pairs, like `[(size1, duration1), (size2, duration2)]`.
    dt : float
        Default is None.

    Returns
    -------
    current_and_duration : tuple
        (The formatted current, total duration)
    """
    dt = backend.get_dt() if dt is None else dt

    # get input current dimension, shape, and duration
    I_duration = 0.
    I_dim = 0
    I_shape = ()
    for I in Iext:
        I_duration += I[1]
        dim = np.ndim(I[0])
        if dim > I_dim:
            I_dim = dim
            I_shape = np.shape(I[0])

    # get the current
    I_current = np.zeros((int(np.ceil(I_duration / dt)),) + I_shape)
    start = 0
    for c_size, duration in Iext:
        length = int(duration / dt)
        I_current[start: start + length] = c_size
        start += length
    return I_current, I_duration


def spike_current(points, lengths, sizes, duration, dt=None):
    """Format current input like a series of short-time spikes.

    For example:

    If you want to generate a spike train at 10 ms, 20 ms, 30 ms, 200 ms, 300 ms,
    and each spike lasts 1 ms and the spike current is 0.5, then you can use the
    following funtions:

    >>> spike_current(points=[10, 20, 30, 200, 300],
    >>>               lengths=1.,  # can be a list to specify the spike length at each point
    >>>               sizes=0.5,  # can be a list to specify the current size at each point
    >>>               duration=400.)

    Parameters
    ----------
    points : list, tuple
        The spike time-points. Must be an iterable object.
    lengths : int, float, list, tuple
        The length of each point-current, mimicking the spike durations.
    sizes : int, float, list, tuple
        The current sizes.
    duration : int, float
        The total current duration.
    dt : float
        The default is None.

    Returns
    -------
    current_and_duration : tuple
        (The formatted current, total duration)
    """
    dt = backend.get_dt() if dt is None else dt
    assert isinstance(points, (list, tuple))
    if isinstance(lengths, (float, int)):
        lengths = [lengths] * len(points)
    if isinstance(sizes, (float, int)):
        sizes = [sizes] * len(points)

    current = np.zeros(int(np.ceil(duration / dt)))
    for time, dur, size in zip(points, lengths, sizes):
        pp = int(time / dt)
        p_len = int(dur / dt)
        current[pp: pp + p_len] = size
    return current


def ramp_current(c_start, c_end, duration, t_start=0, t_end=None, dt=None):
    """Get the gradually changed input current.

    Parameters
    ----------
    c_start : float
        The minimum (or maximum) current size.
    c_end : float
        The maximum (or minimum) current size.
    duration : int, float
        The total duration.
    t_start : float
        The ramped current start time-point.
    t_end : float
        The ramped current end time-point. Default is the None.
    dt

    Returns
    -------
    current_and_duration : tuple
        (The formatted current, total duration)
    """
    dt = backend.get_dt() if dt is None else dt
    t_end = duration if t_end is None else t_end

    current = np.zeros(int(np.ceil(duration / dt)))
    p1 = int(np.ceil(t_start / dt))
    p2 = int(np.ceil(t_end / dt))
    current[p1: p2] = np.linspace(c_start, c_end, p2 - p1)
    return current
