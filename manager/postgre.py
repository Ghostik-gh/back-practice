from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine

meta = MetaData()

test = Table('test', meta,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(36), nullable=False),
    Column('filename', String(250), nullable=False),
    Column('from', String(10), nullable=False),
    Column('to', String(10), nullable=False),
    Column('state', Integer, default=0),
)

engine = create_engine("postgresql+psycopg2://admin:root@localhost", echo=True)
meta.create_all(engine)



# try:
# connection = psycopg2.connect("user=admin password=root")
# print("connection")
# with connection.cursor() as cursor:
#     print("cursor created")
#     cursor.execute(
#         "SELECT version();"
#     )
#     print(f"Server version: {cursor.fetchone()}")
# except psycopg2.Error as err:
#     print("[ERROR]:", str(err))