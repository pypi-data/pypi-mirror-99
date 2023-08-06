##############################################################################
#
#   __main__.py for pynndb-cli
#
#   Copyright (c) 2021 Gareth Bult
#
##############################################################################

import sys
import readline
from cmd2 import Cmd, with_argparser, with_default_category  # , Settable
from termcolor import colored
from pynndb2cli.parsers import Parsers
from pynndb2cli.completers import Completers
from pynndb2cli.commands import Commands
from importlib.metadata import version, PackageNotFoundError


@with_default_category('Database Commands')
class Main(Cmd):

    completers = Completers()
    parsers = Parsers(completers)

    def __init__(self):
        super().__init__()

        try:
            self.__version__ = version("pynndb2cli")
        except PackageNotFoundError:
            raise Exception('package "pynndb2cli" not found!')

        self._commands = Commands(self)
        self.completers._commands = self._commands
        self._history = self._commands.home / '.readline_history'
        self.setPrompt()

    def setPrompt(self):
        if not self._commands.db:
            self.prompt = colored('none', 'cyan') + colored('>', 'blue') + ' '
        else:
            self.prompt = colored(self._commands.dbname, 'green') + colored('>', 'blue') + ' '

    def preloop(self):
        print()
        print(
            colored('PyNNDB2 Command Line Interface ', 'green'),
            colored(f'(v{self.__version__})', 'cyan'))
        print(colored('[', 'white'), colored('type "help" or use TAB to autocomplete', 'grey'), colored(']', 'white'))

        try:
            readline.read_history_file(str(self._history))
        except FileNotFoundError:
            pass

    def postloop(self):
        readline.set_history_length(5000)
        readline.write_history_file(str(self._history))
        print()

    def ppfeedback(self, method, level, msg):
        self.pfeedback(colored(method, 'cyan') + ': ' + colored(level, 'yellow') + ': ' + colored(msg, 'red'))
        return False

    @with_argparser(parsers.register)
    def do_register(self, opts):
        """Register a new database with this tool\n"""
        self._commands.register(opts)

    @with_argparser(parsers.use)
    def do_use(self, opts):
        """Select the database you want to work with\n"""
        self._commands.use(opts)
        self.setPrompt()

    @with_argparser(parsers.explain)
    def do_explain(self, opts):
        """Sample the fields and field types in use in this table\n"""
        self._commands.explain(opts)

    @with_argparser(parsers.analyse)
    def do_analyse(self, opts):
        """Analyse a table to see how record sizes are broken down\n"""
        self._commands.analyse(opts)

    @with_argparser(parsers.select)
    def do_select(self, opts):
        """Select records from a table

        find --by=(index) -k field=value table field:format [field:format..]
        """
        self._commands.select(opts)

    @with_argparser(parsers.unique)
    def do_unique(self, opts):
        """Display a list of unique values for a chosen field

        unique find --by=(index) table field
        """
        self._commands.unique(opts)

    @with_argparser(parsers.show)
    def do_show(self, opts):
        """Show various settings\n"""
        self._commands.show(opts)

    def run(self):
        return self.cmdloop()


print(colored("""
 ____        _   _ _   _ ____  ____         ____ _     ___
|  _ \ _   _| \ | | \ | |  _ \| __ )       / ___| |   |_ _|
| |_) | | | |  \| |  \| | | | |  _ \ _____| |   | |    | |
|  __/| |_| | |\  | |\  | |_| | |_) |_____| |___| |___ | |
|_|    \__, |_| \_|_| \_|____/|____/       \____|_____|___|
       |___/""", 'magenta'))

sys.exit(Main().run())
