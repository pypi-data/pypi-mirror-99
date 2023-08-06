##############################################################################
#
#   parsers.py for pynndb-cli
#
#   Copyright (c) 2021 Gareth Bult
#
##############################################################################
from cmd2 import Cmd2ArgumentParser as ArgumentParser


class Parsers:

    def __init__(self, completers):
        self._completers = completers

    @property
    def register(self):
        parser = ArgumentParser(description="Register a new database")
        parser.add_argument(
            'database',
            nargs=1,
            help='path name of database to register',
            completer_function=self._completers.path_complete)
        parser.add_argument('alias', nargs=1, help='the local alias for the database')
        return parser

    @property
    def use(self):
        parser = ArgumentParser()
        parser.add_argument(
            'database',
            nargs='?',
            help='name of database to use',
            completer_function=self._completers.db_complete)
        return parser

    @property
    def explain(self):
        parser = ArgumentParser()
        parser.add_argument(
            'table',
            nargs=1,
            help='the name of the table',
            completer_function=self._completers.table_complete)
        return parser

    @property
    def analyse(self):
        parser = ArgumentParser()
        parser.add_argument(
            'table',
            nargs=1,
            help='the name of the table',
            completer_function=self._completers.table_complete)
        return parser

    @property
    def select(self):
        parser = ArgumentParser()
        parser.add_argument(
            'table',
            nargs=1,
            help='the table you want records from',
            completer_function=self._completers.table_complete)
        parser.add_argument(
            'fields',
            nargs='*',
            help='the fields to display: field:format [field:format..]',
            completer_function=self._completers.field_complete)
        parser.add_argument('-b', '--by', type=str, help='index to search and sort by')
        parser.add_argument('-k', '--key', type=str, help='key expression to search by')
        parser.add_argument('-e', '--expr', type=str, help='expression to filter by')
        parser.add_argument('-l', '--limit', nargs=1, help='limit output to (n) records')
        return parser

    @property
    def unique(self):
        parser = ArgumentParser()
        parser.add_argument(
            'table',
            nargs=1,
            help='the table you want records from',
            completer_function=self._completers.table_complete)
        parser.add_argument(
            'field',
            nargs=1,
            help='the name of the field you are interested in',
            completer_function=self._completers.field_complete)
        parser.add_argument('-b', '--by', type=str, help='index to search and sort by')
        return parser

    @property
    def show(self):
        parser = ArgumentParser()
        parser.add_argument(
            'option',
            choices=['settings', 'databases', 'tables', 'indexes'],
            help='what it is we want to show'
        )
        parser.add_argument(
            'table',
            nargs='?',
            help='',
            completer_function=self._completers.table_complete)
        return parser

