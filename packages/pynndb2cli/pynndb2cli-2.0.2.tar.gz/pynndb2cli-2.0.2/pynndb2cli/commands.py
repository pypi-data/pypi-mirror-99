##############################################################################
#
#   commands.py for pynndb-cli
#
#   Copyright (c) 2021 Gareth Bult
#
##############################################################################
from pathlib import PosixPath, Path
from json import dumps, loads
from datetime import datetime
from termcolor import colored
from ascii_graph import Pyasciigraph
from ascii_graph.colors import Gre
from pynndb import Manager, Doc
from pynndb2cli.prettyprint import PrettyPrint


class Commands:

    LIMIT = 10

    def __init__(self, cmd):
        self._cmd = cmd
        self._manager = Manager()
        self._db = None
        self._dbname = ''
        self._home = PosixPath('~/.pynndb').expanduser()
        self._regfile = self._home / '.registered_dbs'
        self._dbs = {}
        Path.mkdir(self._home, exist_ok=True)
        self.load_dbs()

    @property
    def home(self):
        return self._home

    @property
    def db(self):
        return self._db

    @property
    def dbname(self):
        return self._dbname

    def ppfeedback(self, method, level, msg):
        self._cmd.pfeedback(colored(method, 'cyan') + ': ' + colored(level, 'yellow') + ': ' + colored(msg, 'red'))
        return False

    def register(self, opts):
        db = opts.database[0]
        alias = opts.alias[0]

        if alias in self._dbs:
            self._cmd.pwarning(f'alias name "{alias}" is already registered')
            return

        if db[0] == '/':
            path = Path(db)
        else:
            path = PosixPath(db).expanduser()

        if not path.exists():
            self._cmd.pwarning(f'database "{db}" does not exist')
            return
        if not path.is_dir():
            self._cmd.pwarning(f'database "{db}" appears to be a file')
            return
        self._cmd.poutput(f'Registering "{db}" as "{alias}"')
        self._dbs[alias] = path.absolute().as_posix()
        self.save_dbs()

    def save_dbs(self):
        with open(self._regfile.as_posix(), 'w') as io:
            io.write(dumps(self.__dbs))

    def load_dbs(self):
        if self._regfile.exists():
            with open(self._regfile.as_posix(), 'r') as io:
                self._dbs = loads(io.read())

    def show_databases(self):
        """Show available databases"""
        dbpp = PrettyPrint()
        for name, path in self._dbs.items():
            mdb = Path(path) / 'data.mdb'
            stat = mdb.stat()
            mapped = stat.st_size
            divisor = 1024
            units = 'K'
            if mapped > 1024 * 1024 * 1024:
                divisor = 1024 * 1024 * 1024
                units = 'G'
            elif mapped > 1024 * 1024:
                divisor = 1024 * 1024
                units = 'M'
            dbpp.append({
                'Database name': name,
                '  Mapped': '{:7.2f}{}'.format(stat.st_size / divisor, units),
                '   Used': '{:6.2f}{}'.format(stat.st_blocks * 512 / divisor, units),
                '(%)': int((stat.st_blocks * 512 * 100) / stat.st_size)
            })
        dbpp.reformat()
        for line in dbpp:
            print(line)

    def show_tables(self):
        """Display a list of tables available within this database\n"""
        dbpp = PrettyPrint()
        for name in self._db.tables():
            table = self._db.table(name)
            db = self._db.env.open_db(name.encode())
            with self._db.env.begin() as txn:
                stat = txn.stat(db)
            leaf = int(stat['leaf_pages'])
            dbpp.append({
                'Table name': name,
                '# Recs': stat['entries'],
                'Depth': stat['depth'],
                'Oflow%': int(int(stat['overflow_pages']) * 100 / (leaf if leaf else 1)),
                'Index names': ', '.join(table.indexes())
            })
        dbpp.reformat()
        for line in dbpp:
            print(line)

    def show_indexes(self, table_name):
        """Display a list of indexes for the specified table\n"""
        table = self._db.table(table_name)
        dbpp = PrettyPrint()

        with table.read_transaction as txn:
            for index in table.indexes(txn=txn):
                d = self._db.meta.fetch_index(table_name, index, txn)
                conf = d['conf']
                if not d or 'conf' not in d:
                    self._cmd.pwarning(f'unable to locate metadata for table "{table_name}"')
                    continue
                dbpp.append({
                    'Table name': table_name if table_name else 'None',
                    'Index name': index if index else 'None',
                    'Entries': table[index].records(),
                    'Key': conf.get('func', 'None'),
                    'Dups': 'True' if conf.get('dupsort') else 'False'
                })
        dbpp.reformat()
        for line in dbpp:
            print(line)

    def show(self, opts):
        if opts.option == 'settings':
            return super.do_show('')
        if opts.option == 'databases':
            return self.show_databases()
        if not self._db:
            return self._cmd.pwarning('no database selected (try "use" first)')
        if opts.option == 'tables':
            return self.show_tables()
        if opts.option == 'indexes':
            if opts.table not in list(self._db.tables()):
                return self._cmd.pwarning(f'no such tables "{opts.table}"')
            return self.show_indexes(opts.table)
        self._cmd.perror('NOT IMPLEMENTED!')

    def use(self, opts):
        if self._db:
            self._db.close()
            self._db = None

        self._dbname = opts.database
        if not opts.database:
            return

        if opts.database not in self._dbs:
            self._cmd.pwarning(f'unknown database name "{opts.database}" - is it registered?')
            return

        name = opts.database
        path = self._dbs[name]
        self._db = self._manager.database(name, path)

    def explain(self, opts):
        """Sample the fields and field types in use in this table\n"""
        if not self._db:
            return self.ppfeedback('explain', 'error', 'no database selected')

        table_name = opts.table[0]
        if table_name not in list(self._db.tables()):
            return self.ppfeedback('register', 'error', 'table does not exist "{}"'.format(table_name))

        table = self._db.table(table_name)
        keys = {}
        samples = {}
        for result in table.filter(page_size=10):
            for key in result.doc.keys():
                ktype = type(result.doc[key]).__name__
                if ktype in ['str', 'int', 'bool', 'bytes', 'float']:
                    sample = result.doc[key]
                    if sample:
                        if ktype == 'bytes':
                            sample = sample.decode()
                        samples[key] = sample
                else:
                    sample = str(result.doc[key])
                    if len(sample) > 60:
                        sample = sample[:60] + '...'
                    samples[key] = sample

                if key not in keys:
                    keys[key] = [ktype]
                else:
                    if ktype not in keys[key]:
                        keys[key].append(ktype)

        dbpp = PrettyPrint()
        [dbpp.append({'Field name': key, 'Field Types': keys[key], 'Sample': samples.get(key, '')}) for key in keys]
        dbpp.reformat()
        for line in dbpp:
            print(line)

    def select(self, opts):
        if not self._db:
            return self.ppfeedback('find', 'error', 'no database selected')

        table_name = opts.table[0]
        if table_name not in list(self._db.tables()):
            return self.ppfeedback('find', 'error', 'table does not exist "{}"'.format(table_name))

        table = self._db.table(table_name)
        if opts.by and opts.by not in table.indexes():
            return self.ppfeedback('find', 'error', 'index does not exist "{}"'.format(opts.by))

        limit = int(opts.limit[0]) if opts.limit else self.LIMIT

        params = {'page_size': limit}
        if opts.by:
            params['index_name'] = opts.by
        if opts.key:
            try:
                key, val = opts.key.split('=')
                params['lower'] = Doc({key: val})
            except Exception as e:
                self._cmd.pfeedback(f'key error: {opts.key} , needs to be in form <key>=<value>')
                raise Exception(e)
        if opts.expr:
            try:
                params['expression'] = eval(opts.expr)
            except Exception as e:
                self._cmd.pfeedback(f'error evaluating expression')
                raise Exception(e)

        def docval(doc, k):
            if k == '_id':
                return doc.key
            if '.' not in k:
                return doc[k] or 'null'
            parts = k.split('.')
            while len(parts):
                k = parts.pop(0)
                doc = doc[k] or {}
            return doc

        dbpp = PrettyPrint()

        if '*' in opts.fields:
            opts.fields.remove('*')
            fields = []
            for result in table.filter(**params):
                for key in result.doc.keys():
                    if key not in fields:
                        fields.append(key)
            opts.fields += fields

        beg = datetime.now()
        for result in table.filter(**params):
            if opts.key:
                if not result.doc[key].startswith(val):
                    break
            dbpp.append({k: docval(result.doc, k) for k in opts.fields})
        end = datetime.now()
        dbpp.reformat()
        for line in dbpp:
            print(line)

        tspan = colored('{:0.4f}'.format((end - beg).total_seconds()), 'yellow')
        limit = '' if dbpp.len < self.LIMIT else colored('(Limited view)', 'red')
        persc = colored('{}/sec'.format(int(1 / (end - beg).total_seconds() * dbpp.len)), 'cyan')
        displayed = colored('Displayed {}'.format(colored(str(dbpp.len), 'yellow')), 'green')
        displayed += colored(' records', 'green')
        self._cmd.pfeedback(colored('{} in {}s {} {}'.format(displayed, tspan, limit, persc), 'green'))

    def unique(self, opts):
        if not self._db:
            return self.ppfeedback('unique', 'error', 'no database selected')

        table_name = opts.table[0]
        if table_name not in list(self._db.tables()):
            return self.ppfeedback('unique', 'error', 'table does not exist "{}"'.format(table_name))

        field_name = opts.field[0]
        table = self._db.table(table_name)
        dbpp = PrettyPrint()

        if opts.by:
            params = {'suppress_duplicates': True}
            if opts.by not in table.indexes():
                return self.ppfeedback('unique', 'error', 'index does not exist "{}"'.format(opts.by))
            params['index_name'] = opts.by
            for result in table.filter(**params):
                dbpp.append(
                    {field_name: result.doc[field_name], 'count': result.count})
        else:
            values = {}
            for result in table.filter():
                value = result.doc[field_name]
                if not isinstance(value, (str, int, float, bool)):
                    value = str(value)
                if value in values:
                    values[value] += 1
                else:
                    values[value] = 1
            for value in values:
                dbpp.append(
                    {field_name: value, 'count': values[value]})

        dbpp.reformat()
        for line in dbpp:
            print(line)

    def analyse(self, opts):
        """Analyse a table to see how record sizes are broken down\n"""
        if not self._db:
            return self.ppfeedback('explain', 'error', 'no database selected')

        table_name = opts.table[0]
        if table_name not in list(self._db.tables()):
            return self.ppfeedback('register', 'error', 'table does not exist "{}"'.format(table_name))

        count = 0
        rtot = 0
        rmax = 0
        vals = []
        for result in self._db.table(table_name).filter():
            rlen = len(result.raw)
            rtot += rlen
            vals.append(rlen)
            if rlen > rmax:
                rmax = rlen
            count += 1

        max = 20
        div = rmax / max
        arr = [0 for i in range(max + 1)]
        for item in vals:
            idx = int(item / div)
            arr[idx] += 1

        test = []
        n = div
        for item in arr:
            label = int(n)
            if n > 1024:
                label = str(int(n / 1024)) + 'K' if n > 1024 else str(label)
            else:
                label = str(label)

            test.append((label, item, Gre))
            n += div

        graph = Pyasciigraph(human_readable='cs')
        print()
        for line in graph.graph(colored('Breakdown of record size distribution', 'cyan'), test):
            print(line)
