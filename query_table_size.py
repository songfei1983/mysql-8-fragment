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
query = """
SELECT table_name AS TableName,
       round((data_length+index_length)/1024/1024,2) AS Size_MB,
       round(data_length/1024/1024,2) AS Data_MB,
       round(index_length/1024/1024,2) AS Index_MB,
       round(data_free/1024/1024,2) AS Free_MB
FROM information_schema.TABLES
WHERE table_schema='test_db' AND table_name='composite_key_table';
"""
cur.execute(query)
rows = cur.fetchall()

# nicely format the output
if rows:
    # print headers
    headers = [i[0] for i in cur.description]
    # compute column widths
    col_widths = [max(len(str(val)) for val in [hdr] + [row[idx] for row in rows]) for idx, hdr in enumerate(headers)]
    # header line
    header_line = " | ".join(hdr.ljust(col_widths[idx]) for idx, hdr in enumerate(headers))
    sep_line = "-+-".join("".ljust(col_widths[idx], "-") for idx in range(len(headers)))
    print(header_line)
    print(sep_line)
    for row in rows:
        print(" | ".join(str(val).ljust(col_widths[idx]) for idx, val in enumerate(row)))
else:
    print("No results returned.")

cur.close()
cnx.close()
