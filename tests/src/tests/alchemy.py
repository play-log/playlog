import sqlalchemy as sa
import yaml


class Alchemy:
    def __init__(self, url, meta):
        # common
        self._url = url
        self._meta = meta
        self._pk_map = {
            k: [i for i in v.columns.values() if i.primary_key]
            for k, v in self._meta.tables.items()
        }

        # setup/teardown
        self._engine = None
        self._conn = None

        # load
        self.data = None

    def setup(self):
        self._engine = sa.create_engine(self._url)
        self._meta.create_all(self._engine)
        self._conn = self._engine.connect()

    def teardown(self):
        self._conn.close()
        self._meta.drop_all(self._engine)
        self._engine = None
        self._conn = None

    def load(self, filepath):
        with open(filepath) as f:
            data = yaml.load(f)
        self.data = {}
        self._fill_data(data)

    def clean(self):
        self.data = {}
        with self._conn.begin():
            tables = ','.join(self._meta.tables)
            stmt = 'TRUNCATE TABLE {} RESTART IDENTITY'.format(tables)
            self._conn.execute(stmt)

    def fetchall(self, table_name):
        stmt = self._meta.tables[table_name].select()
        return self._conn.execute(stmt).fetchall()

    def count(self, table_name):
        return self._conn.scalar(self._meta.tables[table_name].count())

    def _fill_data(self, data):
        with self._conn.begin():
            for entry in data:
                table_name, fields = next(iter(entry.items()))
                table = self._meta.tables[table_name]
                pks = self._pk_map[table.name]
                pk = self._conn.execute(table.insert().values(**fields).returning(*pks)).fetchone()
                if len(pk) > 1:
                    pk = tuple(pk)
                else:
                    pk = pk[0]
                if table_name not in self.data:
                    self.data[table_name] = {}
                self.data[table_name][pk] = fields
