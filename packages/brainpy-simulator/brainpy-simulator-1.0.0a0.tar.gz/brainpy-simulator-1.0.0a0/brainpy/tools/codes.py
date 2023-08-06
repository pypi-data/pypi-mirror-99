# -*- coding: utf-8 -*-

import inspect
import re
from types import LambdaType

__all__ = [
    # tools for code string
    'get_identifiers',
    'indent',
    'deindent',
    'word_replace',

    # other tools
    'is_lambda_function',
    'get_main_code',
    'get_func_source',
]


######################################
# String tools
######################################


def get_identifiers(expr, include_numbers=False):
    """
    Return all the identifiers in a given string ``expr``, that is everything
    that matches a programming language variable like expression, which is
    here implemented as the regexp ``\\b[A-Za-z_][A-Za-z0-9_]*\\b``.

    Parameters
    ----------
    expr : str
        The string to analyze
    include_numbers : bool, optional
        Whether to include number literals in the output. Defaults to ``False``.

    Returns
    -------
    identifiers : set
        A set of all the identifiers (and, optionally, numbers) in `expr`.

    Examples
    --------
    >>> expr = '3-a*_b+c5+8+f(A - .3e-10, tau_2)*17'
    >>> ids = get_identifiers(expr)
    >>> print(sorted(list(ids)))
    ['A', '_b', 'a', 'c5', 'f', 'tau_2']
    >>> ids = get_identifiers(expr, include_numbers=True)
    >>> print(sorted(list(ids)))
    ['.3e-10', '17', '3', '8', 'A', '_b', 'a', 'c5', 'f', 'tau_2']
    """

    _ID_KEYWORDS = {'and', 'or', 'not', 'True', 'False'}
    identifiers = set(re.findall(r'\b[A-Za-z_][A-Za-z0-9_.]*\b', expr))
    # identifiers = set(re.findall(r'\b[A-Za-z_][.?[A-Za-z0-9_]*]*\b', expr))
    if include_numbers:
        # only the number, not a + or -
        pattern = r'(?<=[^A-Za-z_])[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?|^[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
        numbers = set(re.findall(pattern, expr))
    else:
        numbers = set()
    return (identifiers - _ID_KEYWORDS) | numbers


def indent(text, num_tabs=1, spaces_per_tab=4, tab=None):
    if tab is None:
        tab = ' ' * spaces_per_tab
    indent_ = tab * num_tabs
    indented_string = indent_ + text.replace('\n', '\n' + indent_)
    return indented_string


def deindent(text, num_tabs=None, spaces_per_tab=4, docstring=False):
    text = text.replace('\t', ' ' * spaces_per_tab)
    lines = text.split('\n')
    # if it's a docstring, we search for the common tabulation starting from
    # line 1, otherwise we use all lines
    if docstring:
        start = 1
    else:
        start = 0
    if docstring and len(lines) < 2:  # nothing to do
        return text
    # Find the minimum indentation level
    if num_tabs is not None:
        indent_level = num_tabs * spaces_per_tab
    else:
        line_seq = [len(line) - len(line.lstrip()) for line in lines[start:] if len(line.strip())]
        if len(line_seq) == 0:
            indent_level = 0
        else:
            indent_level = min(line_seq)
    # remove the common indentation
    lines[start:] = [line[indent_level:] for line in lines[start:]]
    return '\n'.join(lines)


def word_replace(expr, substitutions):
    """Applies a dict of word substitutions.

    The dict ``substitutions`` consists of pairs ``(word, rep)`` where each
    word ``word`` appearing in ``expr`` is replaced by ``rep``. Here a 'word'
    means anything matching the regexp ``\\bword\\b``.

    Examples
    --------

    >>> expr = 'a*_b+c5+8+f(A)'
    >>> print(word_replace(expr, {'a':'banana', 'f':'func'}))
    banana*_b+c5+8+func(A)
    """
    for var, replace_var in substitutions.items():
        # expr = re.sub(r'\b' + var + r'\b', str(replace_var), expr)
        expr = re.sub(r'\b(?<!\.)' + var + r'\b(?!\.)', str(replace_var), expr)
    return expr


######################################
# Other tools
######################################


def is_lambda_function(func):
    """Check whether the function is a ``lambda`` function. Comes from
    https://stackoverflow.com/questions/23852423/how-to-check-that-variable-is-a-lambda-function

    Parameters
    ----------
    func : callable function
        The function.

    Returns
    -------
    bool
        True of False.
    """
    return isinstance(func, LambdaType) and func.__name__ == "<lambda>"


def get_func_source(func):
    code = inspect.getsource(func)
    # remove @
    try:
        start = code.index('def ')
        code = code[start:]
    except ValueError:
        pass
    return code


def get_main_code(func):
    """Get the main function _code string.

    For lambda function, return the

    Parameters
    ----------
    func : callable, Optional, int, float

    Returns
    -------

    """
    if func is None:
        return ''
    elif callable(func):
        if is_lambda_function(func):
            func_code = get_func_source(func)
            splits = func_code.split(':')
            if len(splits) != 2:
                raise ValueError(f'Can not parse function: \n{func_code}')
            return f'return {splits[1]}'

        else:
            func_codes = inspect.getsourcelines(func)[0]
            idx = 0
            for i, line in enumerate(func_codes):
                idx += 1
                line = line.replace(' ', '')
                if '):' in line:
                    break
            else:
                code = "\n".join(func_codes)
                raise ValueError(f'Can not parse function: \n{code}')
            return ''.join(func_codes[idx:])
    else:
        raise ValueError(f'Unknown function type: {type(func)}.')

