# -*- coding: utf-8 -*-


import _thread as thread
import inspect
import threading

import numpy as np

from brainpy import errors
from brainpy import tools
from brainpy.integrators import ast_analysis
from brainpy.integrators import sympy_analysis

try:
    import numba
    from numba.core.dispatcher import Dispatcher
except ModuleNotFoundError:
    numba = None
    Dispatcher = None

__all__ = [
    'transform_integrals_to_model',
    'DynamicModel',
    'rescale',
    'timeout',
    'jit_compile',
    'add_arrow',
    'contain_unknown_symbol',
]


def transform_integrals_to_model(integrals):
    if callable(integrals):
        integrals = [integrals]

    all_scope = dict()
    all_variables = set()
    all_parameters = set()
    analyzers = []
    for integral in integrals:
        # integral function
        if Dispatcher is not None and isinstance(integral, Dispatcher):
            integral = integral.py_func
        else:
            integral = integral

        # original function
        f = integral.origin_f
        if Dispatcher is not None and isinstance(f, Dispatcher):
            f = f.py_func
        func_name = f.__name__

        # code scope
        closure_vars = inspect.getclosurevars(f)
        code_scope = dict(closure_vars.nonlocals)
        code_scope.update(dict(closure_vars.globals))

        # separate variables
        analysis = ast_analysis.separate_variables(f)
        variables_for_returns = analysis['variables_for_returns']
        expressions_for_returns = analysis['expressions_for_returns']
        for vi, (key, vars) in enumerate(variables_for_returns.items()):
            variables = []
            for v in vars:
                if len(v) > 1:
                    raise ValueError('Cannot analyze must assignment code line.')
                variables.append(v[0])
            expressions = expressions_for_returns[key]
            var_name = integral.variables[vi]
            DE = sympy_analysis.SingleDiffEq(var_name=var_name,
                                             variables=variables,
                                             expressions=expressions,
                                             derivative_expr=key,
                                             scope=code_scope,
                                             func_name=func_name)
            analyzers.append(DE)

        # others
        for var in integral.variables:
            if var in all_variables:
                raise errors.ModelDefError(f'Variable {var} has been defined before. Cannot group '
                                           f'this integral as a dynamic system.')
            all_variables.add(var)
        all_parameters.update(integral.parameters)
        all_scope.update(code_scope)

    return DynamicModel(integrals=integrals,
                        analyzers=analyzers,
                        variables=list(all_variables),
                        parameters=list(all_parameters),
                        scopes=all_scope)


class DynamicModel(object):
    def __init__(self, integrals, analyzers, variables, parameters, scopes):
        self.integrals = integrals
        self.analyzers = analyzers
        self.variables = variables
        self.parameters = parameters
        self.scopes = scopes


def rescale(min_max, scale=0.01):
    """Rescale lim."""
    min_, max_ = min_max
    length = max_ - min_
    min_ -= scale * length
    max_ += scale * length
    return min_, max_


def timeout(s):
    """Add a timeout parameter to a function and return it.

    Parameters
    ----------
    s : float
        Time limit in seconds.

    Returns
    -------
    func : callable
        Functional results. Or, raise an error of KeyboardInterrupt.
    """

    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, thread.interrupt_main)
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result

        return inner

    return outer


def _jit(func):
    if sympy_analysis.func_in_numpy_or_math(func):
        return func
    if isinstance(func, Dispatcher):
        return func
    vars = inspect.getclosurevars(func)
    code_scope = dict(vars.nonlocals)
    code_scope.update(vars.globals)

    modified = False
    # check scope variables
    for k, v in code_scope.items():
        # function
        if callable(v):
            if (not sympy_analysis.func_in_numpy_or_math(v)) and (not isinstance(v, Dispatcher)):
                code_scope[k] = _jit(v)
                modified = True

    if modified:
        func_code = tools.deindent(tools.get_func_source(func))
        exec(compile(func_code, '', "exec"), code_scope)
        func = code_scope[func.__name__]
        return numba.njit(func)
    else:
        return numba.njit(func)


def jit_compile(scope, func_code, func_name):
    if numba is None:
        return
        # get function scope
    func_scope = dict()
    for key, val in scope.items():
        if callable(val):
            if sympy_analysis.func_in_numpy_or_math(val):
                pass
            elif isinstance(val, Dispatcher):
                pass
            else:
                val = _jit(val)
        func_scope[key] = val

    # compile function
    exec(compile(func_code, '', 'exec'), func_scope)
    return numba.njit(func_scope[func_name])


def contain_unknown_symbol(expr, scope):
    """Examine where the given expression ``expr`` has the unknown symbol in ``scope``.

    Returns
    -------
    res : bool
        True or False.
    """
    ids = tools.get_identifiers(expr)
    for id_ in ids:
        if '.' in id_:
            prefix = id_.split('.')[0].strip()
            if prefix not in scope:
                return True
        if id_ not in scope:
            return True
    return False


def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate(text='',
                       xytext=(xdata[start_ind], ydata[start_ind]),
                       xy=(xdata[end_ind], ydata[end_ind]),
                       arrowprops=dict(arrowstyle="->", color=color),
                       size=size)


def f1(arr, grad, tol):
    condition = np.logical_and(grad[:-1] * grad[1:] <= 0, grad[:-1] >= 0)
    indexes = np.where(condition)[0]
    if len(indexes) >= 2:
        data = arr[indexes[-2]: indexes[-1]]
        length = np.max(data) - np.min(data)
        a = arr[indexes[-2]]
        b = arr[indexes[-1]]
        if np.abs(a - b) < tol * length:
            return indexes[-2:]
    return np.array([-1, -1])


if numba is not None:
    f1 = numba.njit(f1)


def f2(arr, grad, tol):
    condition = np.logical_and(grad[:-1] * grad[1:] <= 0, grad[:-1] <= 0)
    indexes = np.where(condition)[0]
    if len(indexes) >= 2:
        data = arr[indexes[-2]: indexes[-1]]
        length = np.max(data) - np.min(data)
        a = arr[indexes[-2]]
        b = arr[indexes[-1]]
        if np.abs(a - b) < tol * length:
            return indexes[-2:]
    return np.array([-1, -1])


if numba is not None:
    f2 = numba.njit(f2)


def find_indexes_of_limit_cycle_max(arr, tol=0.001):
    grad = np.gradient(arr)
    return f1(arr, grad, tol)


def find_indexes_of_limit_cycle_min(arr, tol=0.001):
    grad = np.gradient(arr)
    return f2(arr, grad, tol)


def _identity(a, b, tol=0.01):
    if np.abs(a - b) < tol:
        return True
    else:
        return False


if numba is not None:
    _identity = numba.njit(_identity)


def find_indexes_of_limit_cycle_max2(arr, tol=0.001):
    if np.ndim(arr) == 1:
        grad = np.gradient(arr)
        condition = np.logical_and(grad[:-1] * grad[1:] <= 0, grad[:-1] >= 0)
        indexes = np.where(condition)[0]
        if len(indexes) >= 2:
            data = arr[indexes[-2]: indexes[-1]]
            length = np.max(data) - np.min(data)
            if _identity(arr[indexes[-2]], arr[indexes[-1]], tol * length):
                return indexes[-2:]
        return np.array([-1, -1])

    elif np.ndim(arr) == 2:
        # The data with the shape of (axis_along_time, axis_along_neuron)
        grads = np.gradient(arr, axis=0)
        conditions = np.logical_and(grads[:-1] * grads[1:] <= 0, grads[:-1] >= 0)
        indexes = -np.ones((len(conditions), 2), dtype=int)
        for i, condition in enumerate(conditions):
            idx = np.where(condition)[0]
            if len(idx) >= 2:
                if _identity(arr[idx[-2]], arr[idx[-1]], tol):
                    indexes[i] = idx[-2:]
        return indexes

    else:
        raise ValueError


def find_indexes_of_limit_cycle_min2(arr, tol=0.01):
    if np.ndim(arr) == 1:
        grad = np.gradient(arr)
        condition = np.logical_and(grad[:-1] * grad[1:] <= 0, grad[:-1] <= 0)
        indexes = np.where(condition)[0]
        if len(indexes) >= 2:
            indexes += 1
            if _identity(arr[indexes[-2]], arr[indexes[-1]], tol):
                return indexes[-2:]
        return np.array([-1, -1])

    elif np.ndim(arr) == 2:
        # The data with the shape of (axis_along_time, axis_along_neuron)
        grads = np.gradient(arr, axis=0)
        conditions = np.logical_and(grads[:-1] * grads[1:] <= 0, grads[:-1] <= 0)
        indexes = -np.ones((len(conditions), 2), dtype=int)
        for i, condition in enumerate(conditions):
            idx = np.where(condition)[0]
            if len(idx) >= 2:
                idx += 1
                if _identity(arr[idx[-2]], arr[idx[-1]], tol):
                    indexes[i] = idx[-2:]
        return indexes

    else:
        raise ValueError
