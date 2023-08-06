# This file is part of Marcel.
# 
# Marcel is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your
# option) any later version.
# 
# Marcel is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Marcel.  If not, see <https://www.gnu.org/licenses/>.

import dill.source

import marcel.exception
import marcel.reduction


SYMBOLS = {
    '+': marcel.reduction.r_plus,
    '*': marcel.reduction.r_times,
    '^': marcel.reduction.r_xor,
    '&': marcel.reduction.r_bit_and,
    '|': marcel.reduction.r_bit_or,
    'and': marcel.reduction.r_and,
    'or': marcel.reduction.r_or,
    'max': marcel.reduction.r_max,
    'min': marcel.reduction.r_min,
    'count': marcel.reduction.r_count,
    '.': marcel.reduction.r_group
}


class FunctionWrapper:

    # For creating a Function from source, we need source and globals. If the function itself (i.e., lambda)
    # is provided, then the globals aren't needed, since we don't need to use eval.
    def __init__(self, function=None, source=None):
        self._op = None
        if function and source:
            self._function = function
            self._source = source
            self._display = source
        elif function:
            assert type(function) is not FunctionWrapper, function
            self._function = function
            self._source = None
            try:
                self._display = dill.source.getsource(function)
            except:
                pass
        else:  # source is not None
            self._source = source
            self._display = source
            self._function = SYMBOLS[source]
        self._globals = self._function.__globals__
        assert self._function

    def __repr__(self):
        return str(self._function) if self._display is None else self._display

    def __getstate__(self):
        if self._source:
            map = self.__dict__.copy()
            map['_function'] = None
            # TODO: Clear _globals too. Rely on ops providing the applicable one
        else:
            map = self.__dict__
        return map

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __call__(self, *args, **kwargs):
        try:
            return self.function()(*args, **kwargs)
        except Exception as e:
            self.handle_error(e, self.function_input_description(args, kwargs))

    def check_validity(self):
        if not callable(self.function()):
            raise marcel.exception.KillCommandException('Not a valid function')

    def source(self):
        return self._source if self._source else None

    def snippet(self):
        return self._source.split('\n')[0].strip() if self._source else self._function

    def is_grouping(self):
        return self.function() == marcel.reduction.r_group

    def set_op(self, op):
        self._op = op

    def handle_error(self, e, function_input_string):
        if self._op:
            self._op.fatal_error(function_input_string, str(e))
        else:
            raise marcel.exception.KillCommandException(f'Error evaluating {self} on {function_input_string}: {e}')

    def function(self):
        if self._function is None or (self._function.__globals__ is not self._op.env().vars()):
            try:
                self._function = SYMBOLS[self._source]
            except KeyError:
                self._function = eval(self._source, self._globals)
        return self._function

    def set_globals(self, globals):
        if self._globals is not globals:
            self._globals = globals
            if self._source is None:
                self._function.__globals__.update(globals)
            else:
                self._function = None

    @staticmethod
    def function_input_description(args, kwargs):
        function_input = []
        if args and len(args) > 0:
            function_input.append(str(args))
        if kwargs and len(kwargs) > 0:
            function_input.append(str(kwargs))
        return None if len(function_input) == 0 else ', '.join(function_input)

