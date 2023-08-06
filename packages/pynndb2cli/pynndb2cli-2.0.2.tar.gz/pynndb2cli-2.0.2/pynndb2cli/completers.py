##############################################################################
#
#   completers.py for pynndb-cli
#
#   Copyright (c) 2021 Gareth Bult
#
##############################################################################
from cmd2 import Cmd


class Completers(Cmd):

    def __init__(self):
        self._cmd = Cmd()

    def path_complete(self, text, line, begidx, endidx):
        return Cmd.path_complete(self._cmd, text, line, begidx, endidx)

    def db_complete(self, text, line, begidx, endidx):
        return [f for f in self._commands._dbs if f.startswith(text)]

    def table_complete(self, text, line, begidx, endidx):
        return [f for f in self._commands._db.tables() if f.startswith(text)]

    def field_complete(self, text, line, begidx, endidx):
        table_name = line.split(' ')[1]
        table = self._commands._db.table(table_name)
        first = table.first()
        fields = [f for f in first.keys()]
        return ['*'] + [f for f in fields if f.startswith(text)]
