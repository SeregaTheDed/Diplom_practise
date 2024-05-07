import sqlite3

db_file = 'database.db'

def init_database():

    schema_file = 'schema.sql'
    print('')

    with open(schema_file, 'r') as rf:
        schema = rf.read()

    with sqlite3.connect(db_file) as conn:
        conn.executescript(schema)
