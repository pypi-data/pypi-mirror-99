from collections import defaultdict, namedtuple
from datetime import datetime
import os

import attr
import sqlalchemy as sa

# permit use in both a package and standalone for testing purposes.
# See https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time/14132912#14132912
if __package__:
    from . import constants
else:
    import constants

TABLES = {
    "registree": ("md410_2021_conv", "online_registree"),
}


@attr.s
class Registree(object):
    reg_num = attr.ib()
    first_names = attr.ib()
    last_name = attr.ib()
    cell = attr.ib()
    email = attr.ib()
    club = attr.ib()
    district = attr.ib()
    first_mdc = attr.ib()
    attending_district_convention = attr.ib()
    attending_md_convention = attr.ib()
    voter = attr.ib()
    timestamp = attr.ib()

    def __attrs_post_init__(self):
        self.name = f"{self.first_names} {self.last_name}"


@attr.s
class DB(object):
    """Handle postgres database interaction"""

    host = attr.ib(default=os.getenv("PGHOST", "localhost"))
    port = attr.ib(default=os.getenv("PGPORT", 5432))
    user = attr.ib(default=os.getenv("PGUSER", "postgres"))
    password = attr.ib(default=os.getenv("PGPASSWORD"))
    dbname = attr.ib(default="postgres")
    debug = attr.ib(default=False)

    def __attrs_post_init__(self):
        self.engine = sa.create_engine(
            f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}",
            echo=self.debug,
        )
        md = sa.MetaData()
        md.bind = self.engine
        self.engine.autocommit = True
        self.tables = {}
        for (k, (schema, name)) in TABLES.items():
            self.tables[k] = sa.Table(name, md, autoload=True, schema=schema)
        self.reg_nums = []

    def get_registree(self, reg_num):
        tr = self.tables["registree"]
        res = self.engine.execute(
            sa.select(
                [
                    tr.c.reg_num,
                    tr.c.first_names,
                    tr.c.last_name,
                    tr.c.cell,
                    tr.c.email,
                    tr.c.club,
                    tr.c.district,
                    tr.c.first_mdc,
                    tr.c.attending_district_convention,
                    tr.c.attending_md_convention,
                    tr.c.voter,
                    tr.c.timestamp,
                ],
                whereclause=sa.and_(
                    tr.c.reg_num == reg_num, tr.c.cancellation_timestamp == None
                ),
            )
        ).fetchone()
        return Registree(*res)

    def __delete_registrees(self, reg_nums):
        tr = self.tables["registree"]
        for t in (tr,):
            self.engine.execute(t.delete(t.c.reg_num.in_(reg_nums)))

    def _clear(self):
        tr = self.tables["registree"]
        res = self.engine.execute(sa.select([tr.c.reg_num])).fetchall()
        self.__delete_registrees([r.reg_num for r in res])

    def save_registree(self, registree):
        tr = self.tables["registree"]

        self.__delete_registrees([registree.reg_num])

        d = {
            "reg_num": registree.reg_num,
            "first_names": registree.first_names,
            "last_name": registree.last_name,
            "cell": registree.cell,
            "email": registree.email,
            "club": registree.club,
            "district": registree.district,
            "first_mdc": registree.first_mdc,
            "attending_district_convention": registree.attending_district_convention,
            "attending_md_convention": registree.attending_md_convention,
            "voter": registree.voter,
            "timestamp": registree.timestamp,
        }
        self.engine.execute(tr.insert(d))

    def get_registrees(self, reg_nums=None):
        tr = self.tables["registree"]

        query = sa.select(
            [
                tr.c.reg_num,
                tr.c.first_names,
                tr.c.last_name,
                tr.c.cell,
                tr.c.email,
                tr.c.club,
                tr.c.district,
                tr.c.first_mdc,
                tr.c.attending_district_convention,
                tr.c.attending_md_convention,
                tr.c.voter,
                tr.c.timestamp,
            ]
        )

        if reg_nums:
            query = query.where(
                sa.and_(tr.c.reg_num.in_(reg_nums), tr.c.cancellation_timestamp == None)
            )
        else:
            query = query.where(tr.c.cancellation_timestamp == None)
        res = self.engine.execute(query).fetchall()
        registrees = []
        for r in res:
            registrees.append(Registree(*r))
        return registrees

    def cancel_registration(self, reg_nums):
        tr = self.tables["registree"]
        dt = datetime.now()
        self.engine.execute(
            tr.update(tr.c.reg_num.in_(reg_nums), {"cancellation_timestamp": dt})
        )
