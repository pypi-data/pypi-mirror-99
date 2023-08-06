# -*- coding: utf-8 -*-

from brainpy import backend
from brainpy.integrators import constants
from . import common

__all__ = [
    'euler',
    'milstein',
]


def _df_and_dg(code_lines, variables, parameters):
    # 1. df
    # df = f(x, t, *args)
    all_df = [f'{var}_df' for var in variables]
    code_lines.append(f'  {", ".join(all_df)} = f({", ".join(variables + parameters)})')

    # 2. dg
    # dg = g(x, t, *args)
    all_dg = [f'{var}_dg' for var in variables]
    code_lines.append(f'  {", ".join(all_dg)} = g({", ".join(variables + parameters)})')
    code_lines.append('  ')


def _dfdt(code_lines, variables, vdt):
    for var in variables:
        code_lines.append(f'  {var}_dfdt = {var}_df * {vdt}')
    code_lines.append('  ')


def _noise_terms(code_lines, variables):
    num_vars = len(variables)
    if num_vars > 1:
        code_lines.append(f'  all_dW = backend.normal(0.0, dt_sqrt, ({num_vars},)+backend.shape({variables[0]}_dg))')
        for i, var in enumerate(variables):
            code_lines.append(f'  {var}_dW = all_dW[{i}]')
    else:
        var = variables[0]
        code_lines.append(f'  {var}_dW = backend.normal(0.0, dt_sqrt, backend.shape({var}))')
    code_lines.append('  ')


# ----------
# Wrapper
# ----------


def _wrap(wrapper, f, g, dt, sde_type, var_type, wiener_type, show_code):
    """The base function to format a SRK method.

    Parameters
    ----------
    f : callable
        The drift function of the SDE.
    g : callable
        The diffusion function of the SDE.
    dt : float
        The numerical precision.
    sde_type : str
        "utils.ITO_SDE" : Ito's Stochastic Calculus.
        "utils.STRA_SDE" : Stratonovich's Stochastic Calculus.
    wiener_type : str
    var_type : str
        "scalar" : with the shape of ().
        "population" : with the shape of (N,) or (N1, N2) or (N1, N2, ...).
        "system": with the shape of (d, ), (d, N), or (d, N1, N2).
    show_code : bool
        Whether show the formatted code.

    Returns
    -------
    numerical_func : callable
        The numerical function.
    """

    sde_type = constants.ITO_SDE if sde_type is None else sde_type
    assert sde_type in constants.SUPPORTED_SDE_TYPE, f'Currently, BrainPy only support SDE types: ' \
                                                     f'{constants.SUPPORTED_SDE_TYPE}. But we got {sde_type}.'

    var_type = constants.POPU_VAR if var_type is None else var_type
    assert var_type in constants.SUPPORTED_VAR_TYPE, f'Currently, BrainPy only supports variable types: ' \
                                                     f'{constants.SUPPORTED_VAR_TYPE}. But we got {var_type}.'

    wiener_type = constants.SCALAR_WIENER if wiener_type is None else wiener_type
    assert wiener_type in constants.SUPPORTED_WIENER_TYPE, f'Currently, BrainPy only supports Wiener ' \
                                                           f'Process types: {constants.SUPPORTED_WIENER_TYPE}. ' \
                                                           f'But we got {wiener_type}.'

    show_code = False if show_code is None else show_code
    dt = backend.get_dt() if dt is None else dt

    if f is not None and g is not None:
        return wrapper(f=f, g=g, dt=dt, show_code=show_code, sde_type=sde_type,
                       var_type=var_type, wiener_type=wiener_type)

    elif f is not None:
        return lambda g: wrapper(f=f, g=g, dt=dt, show_code=show_code, sde_type=sde_type,
                                 var_type=var_type, wiener_type=wiener_type)

    elif g is not None:
        return lambda f: wrapper(f=f, g=g, dt=dt, show_code=show_code, sde_type=sde_type,
                                 var_type=var_type, wiener_type=wiener_type)

    else:
        raise ValueError('Must provide "f" or "g".')


def _euler_wrapper(f, g, dt, sde_type, var_type, wiener_type, show_code):
    vdt, variables, parameters, arguments, func_name = common.basic_info(f=f, g=g)

    # 1. code scope
    code_scope = {'f': f, 'g': g, vdt: dt, f'{vdt}_sqrt': dt ** 0.5, 'backend': backend}

    # 2. code lines
    code_lines = [f'def {func_name}({", ".join(arguments)}):']

    # 2.1 df, dg
    _df_and_dg(code_lines, variables, parameters)

    # 2.2 dfdt
    _dfdt(code_lines, variables, vdt)

    # 2.3 dW
    _noise_terms(code_lines, variables)

    # 2.3 dgdW
    # ----
    # SCALAR_WIENER : dg * dW
    # VECTOR_WIENER : backend.sum(dg * dW, axis=-1)

    if wiener_type == constants.SCALAR_WIENER:
        for var in variables:
            code_lines.append(f'  {var}_dgdW = {var}_dg * {var}_dW')
    else:
        for var in variables:
            code_lines.append(f'  {var}_dgdW = backend.sum({var}_dg * {var}_dW, axis=-1)')
    code_lines.append('  ')

    if sde_type == constants.ITO_SDE:
        # 2.4 new var
        # ----
        # y = x + dfdt + dgdW
        for var in variables:
            code_lines.append(f'  {var}_new = {var} + {var}_dfdt + {var}_dgdW')
        code_lines.append('  ')

    elif sde_type == constants.STRA_SDE:
        # 2.4  y_bar = x + backend.sum(dgdW, axis=-1)
        all_bar = [f'{var}_bar' for var in variables]
        for var in variables:
            code_lines.append(f'  {var}_bar = {var} + {var}_dgdW')
        code_lines.append('  ')

        # 2.5  dg_bar = g(y_bar, t, *args)
        all_dg_bar = [f'{var}_dg_bar' for var in variables]
        code_lines.append(f'  {", ".join(all_dg_bar)} = g({", ".join(all_bar + parameters)})')

        # 2.6 dgdW2
        # ----
        # SCALAR_WIENER : dgdW2 = dg_bar * dW
        # VECTOR_WIENER : dgdW2 = backend.sum(dg_bar * dW, axis=-1)
        if wiener_type == constants.SCALAR_WIENER:
            for var in variables:
                code_lines.append(f'  {var}_dgdW2 = {var}_dg_bar * {var}_dW')
        else:
            for var in variables:
                code_lines.append(f'  {var}_dgdW2 = backend.sum({var}_dg_bar * {var}_dW, axis=-1)')
        code_lines.append('  ')

        # 2.7 new var
        # ----
        # y = x + dfdt + 0.5 * (dgdW + dgdW2)
        for var in variables:
            code_lines.append(f'  {var}_new = {var} + {var}_dfdt + 0.5 * ({var}_dgdW + {var}_dgdW2)')
        code_lines.append('  ')
    else:
        raise ValueError(f'Unknown SDE type: {sde_type}. We only '
                         f'supports {constants.SUPPORTED_SDE_TYPE}.')

    # return and compile
    return common.return_compile_and_assign_attrs(
        code_lines=code_lines, code_scope=code_scope, show_code=show_code,
        variables=variables, parameters=parameters, func_name=func_name,
        sde_type=sde_type, var_type=var_type, wiener_type=wiener_type, dt=dt)


def _milstein_wrapper(f, g, dt, sde_type, var_type, wiener_type, show_code):
    vdt, variables, parameters, arguments, func_name = common.basic_info(f=f, g=g)

    # 1. code scope
    code_scope = {'f': f, 'g': g, vdt: dt, f'{vdt}_sqrt': dt ** 0.5, 'backend': backend}

    # 2. code lines
    code_lines = [f'def {func_name}({", ".join(arguments)}):']

    # 2.1 df, dg
    _df_and_dg(code_lines, variables, parameters)

    # 2.2 dfdt
    _dfdt(code_lines, variables, vdt)

    # 2.3 dW
    _noise_terms(code_lines, variables)

    # 2.3 dgdW
    # ----
    # dg * dW
    for var in variables:
        code_lines.append(f'  {var}_dgdW = {var}_dg * {var}_dW')
    code_lines.append('  ')

    # 2.4  df_bar = x + dfdt + backend.sum(dg * dt_sqrt, axis=-1)
    all_df_bar = [f'{var}_df_bar' for var in variables]
    if wiener_type == constants.SCALAR_WIENER:
        for var in variables:
            code_lines.append(f'  {var}_df_bar = {var} + {var}_dfdt + {var}_dg * {vdt}_sqrt')
    else:
        for var in variables:
            code_lines.append(f'  {var}_df_bar = {var} + {var}_dfdt + backend.sum('
                              f'{var}_dg * {vdt}_sqrt, axis=-1)')

    # 2.5  dg_bar = g(y_bar, t, *args)
    all_dg_bar = [f'{var}_dg_bar' for var in variables]
    code_lines.append(f'  {", ".join(all_dg_bar)} = g({", ".join(all_df_bar + parameters)})')
    code_lines.append('  ')

    # 2.6 dgdW2
    # ----
    # dgdW2 = 0.5 * (dg_bar - dg) * (dW * dW / dt_sqrt - dt_sqrt)
    if sde_type == constants.ITO_SDE:
        for var in variables:
            code_lines.append(f'  {var}_dgdW2 = 0.5 * ({var}_dg_bar - {var}_dg) * '
                              f'({var}_dW * {var}_dW / {vdt}_sqrt - {vdt}_sqrt)')
    elif sde_type == constants.STRA_SDE:
        for var in variables:
            code_lines.append(f'  {var}_dgdW2 = 0.5 * ({var}_dg_bar - {var}_dg) * '
                              f'{var}_dW * {var}_dW / {vdt}_sqrt')
    else:
        raise ValueError(f'Unknown SDE type: {sde_type}')
    code_lines.append('  ')

    # 2.7 new var
    # ----
    # SCALAR_WIENER : y = x + dfdt + dgdW + dgdW2
    # VECTOR_WIENER : y = x + dfdt + backend.sum(dgdW + dgdW2, axis=-1)
    if wiener_type == constants.SCALAR_WIENER:
        for var in variables:
            code_lines.append(f'  {var}_new = {var} + {var}_dfdt + {var}_dgdW + {var}_dgdW2')
    elif wiener_type == constants.VECTOR_WIENER:
        for var in variables:
            code_lines.append(f'  {var}_new = {var} + {var}_dfdt +backend.sum({var}_dgdW + {var}_dgdW2, axis=-1)')
    else:
        raise ValueError(f'Unknown Wiener Process : {wiener_type}')
    code_lines.append('  ')

    # return and compile
    return common.return_compile_and_assign_attrs(
        code_lines=code_lines, code_scope=code_scope, show_code=show_code,
        variables=variables, parameters=parameters, func_name=func_name,
        sde_type=sde_type, var_type=var_type, wiener_type=wiener_type, dt=dt)


# ------------------
# Numerical methods
# ------------------


def euler(f=None, g=None, dt=None, sde_type=None, var_type=None, wiener_type=None, show_code=None):
    return _wrap(_euler_wrapper, f=f, g=g, dt=dt, sde_type=sde_type, var_type=var_type,
                 wiener_type=wiener_type, show_code=show_code)


def milstein(f=None, g=None, dt=None, sde_type=None, var_type=None, wiener_type=None, show_code=None):
    return _wrap(_milstein_wrapper, f=f, g=g, dt=dt, sde_type=sde_type, var_type=var_type,
                 wiener_type=wiener_type, show_code=show_code)
