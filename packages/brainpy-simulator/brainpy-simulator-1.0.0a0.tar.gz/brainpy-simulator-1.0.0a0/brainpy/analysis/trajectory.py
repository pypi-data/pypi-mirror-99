# -*- coding: utf-8 -*-

from brainpy import backend
from brainpy.simulation.utils import run_model
from brainpy.tools import DictPlus

__all__ = [
    'Trajectory',
]


class Trajectory(object):
    def __init__(self, size, integrals, target_vars, fixed_vars,
                 pars_update, scope, show_code=False):
        """Trajectory Class.

        Parameters
        ----------
        size : int, tuple, list
            The network size.
        integrals : list of functions, function
            The integral functions.
        target_vars : dict
            The target variables, with the format of "{key: initial_v}".
        fixed_vars : dict
            The fixed variables, with the format of "{key: fixed_v}".
        pars_update : dict
            The parameters to update.
        scope :
        """
        if callable(integrals):
            integrals = (integrals,)
        elif isinstance(integrals, (list, tuple)) and callable(integrals[0]):
            integrals = tuple(integrals)
        else:
            raise ValueError
        self.integrals = integrals
        self.target_vars = target_vars
        self.fixed_vars = fixed_vars
        self.pars_update = pars_update
        self.scope = {key: val for key, val in scope.items()}
        self.show_code = show_code

        # check network size
        if isinstance(size, int):
            size = (size,)
        elif isinstance(size, (tuple, list)):
            assert isinstance(size[0], int)
            size = tuple(size)
        else:
            raise ValueError

        # monitors, variables, parameters
        self.mon = DictPlus()
        self.vars_and_pars = DictPlus()
        for key, val in target_vars.items():
            self.vars_and_pars[key] = backend.ones(size) * val
            self.mon[key] = backend.zeros((1,) + size)
        for key, val in fixed_vars.items():
            self.vars_and_pars[key] = backend.ones(size) * val
        for key, val in pars_update.items():
            self.vars_and_pars[key] = val
        self.scope['VP'] = self.vars_and_pars
        self.scope['MON'] = self.mon
        self.scope['_fixed_vars'] = fixed_vars

        code_lines = ['def run_func(_t, _i, _dt):']
        for integral in integrals:
            func_name = integral.__name__
            self.scope[func_name] = integral
            # update the step function
            assigns = [f'VP["{var}"]' for var in integral.variables]
            calls = [f'VP["{var}"]' for var in integral.variables]
            calls.append('_t')
            calls.extend([f'VP["{var}"]' for var in integral.parameters[1:]])
            code_lines.append(f'  {", ".join(assigns)} = {func_name}({", ".join(calls)})')
            # reassign the fixed variables
            for key, val in fixed_vars.items():
                code_lines.append(f'  VP["{key}"][:] = _fixed_vars["{key}"]')
        # monitor the target variables
        for key in target_vars.keys():
            code_lines.append(f'  MON["{key}"][_i] = VP["{key}"]')
        # compile
        code = '\n'.join(code_lines)
        if show_code:
            print(code)
            print(self.scope)
            print()

        # recompile
        exec(compile(code, '', 'exec'), self.scope)
        self.run_func = self.scope['run_func']

    def run(self, duration, report=False, report_percent=0.1):
        if isinstance(duration, (int, float)):
            duration = [0, duration]
        elif isinstance(duration, (tuple, list)):
            assert len(duration) == 2
            duration = tuple(duration)
        else:
            raise ValueError

        # get the times
        times = backend.arange(duration[0], duration[1], backend.get_dt())
        # reshape the monitor
        for key in self.mon.keys():
            self.mon[key] = backend.zeros((len(times),) + backend.shape(self.mon[key])[1:])
        # run the model
        run_model(run_func=self.run_func, times=times, report=report, report_percent=report_percent)
