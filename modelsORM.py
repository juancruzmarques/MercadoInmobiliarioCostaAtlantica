import psycopg2

conn = psycopg2.connect(
        database = 'zp_db',
        host = '0.0.0.0',
        user = 'postgres',
        password = '0223',
        port = '5432'
        )

cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXIST Publicaciones( id INTEGER, VARCHAR(255), )
            ''')
