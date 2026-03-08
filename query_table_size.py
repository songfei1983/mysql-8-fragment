import mysql.connector

config = {
    'user': 'user',
    'password': 'password',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'test_db',
}

cnx = mysql.connector.connect(**config)
cur = cnx.cursor()
cur.execute("""
SELECT table_name AS TableName,
       round((data_length+index_length)/1024/1024,2) AS Size_MB,
       round(data_length/1024/1024,2) AS Data_MB,
       round(index_length/1024/1024,2) AS Index_MB,
       round(data_free/1024/1024,2) AS Free_MB
FROM information_schema.TABLES
WHERE table_schema='test_db' AND table_name='composite_key_table';
"""
)
print(cur.fetchall())
cur.close()
cnx.close()
