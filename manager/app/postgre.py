from config import settings
from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine

meta = MetaData()

"""
states:
0: uploading
1: waiting queue
2: converting
3: ready
4: deleted
"""
test = Table('test', meta,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(36), nullable=False),
    Column('filename', String(250), nullable=False),
    Column('start_ext', String(30), nullable=False),
    Column('end_ext', String(30), nullable=False),
    Column('state', Integer, default=0),
)

dsn=settings.DSN_POSTGRE
engine = create_engine(dsn)# , echo=True)
meta.create_all(engine)

def add_file(uuid:str, filename:str, start_ext:str, end_ext:str):
    with engine.connect() as conn:
        insert_row = test.insert().values(uuid=uuid, filename=filename, start_ext=start_ext, end_ext=end_ext, state=0)
        conn.execute(insert_row)
        conn.commit()


def get_status(uuid:str) -> int:
    with engine.connect() as conn:
        res = conn.execute(test.select().where(test.c.uuid == uuid))
        return res.fetchone()[-1]


def change_status(uuid:str, state:int):
    with engine.connect() as conn:
        conn.execute(test.update().where(test.c.uuid == uuid).values(state=state))
        conn.commit()


def get_filename(uuid:str) -> int:
    with engine.connect() as conn:
        res = conn.execute(test.select().where(test.c.uuid == uuid))
        result = res.fetchone()[2:]
        filename = f'{result[0]}.{result[2]}'
        return filename
