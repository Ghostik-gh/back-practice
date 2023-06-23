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

engine = create_engine(f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@db/db01", echo=True)
# engine = create_engine(f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.HOST}/db01", echo=True)

meta.create_all(engine)

# try except ?
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
    print('start changing')
    with engine.connect() as conn:
        print('connection started')
        conn.execute(test.update().where(test.c.uuid == uuid).values(state=state))
        print('before commit')
        conn.commit()
        print('closing')
        conn.close()
    print("end connection from postgre")

def get_exts(uuid:str) -> int:
    with engine.connect() as conn:
        res = conn.execute(test.select().where(test.c.uuid == uuid))
        return res.fetchone()[-3:-1]

# change_status("2f3ff4a6-c1fd-41c4-af6d-e911ca9dddb8", 3)
# add_file("file_id", str(random.randint(0, 1000)), '.start', '.abc')
# check_state_db('file_id')