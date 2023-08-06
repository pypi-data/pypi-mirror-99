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

import contextlib
import importlib
import io

import marcel.argsparser
import marcel.core
import marcel.exception
import marcel.helpformatter
import marcel.util


def help(env):
    return Help(env)


class HelpArgsParser(marcel.argsparser.ArgsParser):

    def __init__(self, env):
        super().__init__('help', env)
        self.add_anon('topic', convert=self.check_str, default='marcel')
        self.validate()


class Help(marcel.core.Op):

    def __init__(self, env):
        super().__init__(env)
        self.topic = None
        self.module = None

    def __repr__(self):
        return f'help({self.topic})'

    # AbstractOp
    
    def setup(self):
        self.topic = self.topic.lower()

    def run(self):
        op_module = self.env().op_modules.get(self.topic, None)
        help_text = self.op_help(op_module) if op_module else self.topic_help()
        self.send(help_text)
        self.send('')

    # Op

    def must_be_first_in_pipeline(self):
        return True

    def run_in_main_process(self):
        return True

    # For use by this class

    def op_help(self, op_module):
        help_text = op_module.help()
        formatter = marcel.helpformatter.HelpFormatter(self.env().color_scheme())
        return formatter.format(help_text)

    def topic_help(self):
        try:
            self.module = importlib.import_module(f'marcel.doc.help_{self.topic}')
        except ModuleNotFoundError:
            raise marcel.exception.KillCommandException(f'Help not available for {self.topic}')
        formatter = marcel.helpformatter.HelpFormatter(self.env().color_scheme())
        help_text = getattr(self.module, 'HELP')
        return formatter.format(help_text)
