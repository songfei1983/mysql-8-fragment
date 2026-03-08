"""Perform repeated deletions and insertions to increase table fragmentation."""

import mysql.connector
import random

config = {
    'user': 'user',
    'password': 'password',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'test_db',
}

LOOPS = 20
BATCH_SIZE = 50000


def do_cycle(cnx):
    """Perform one delete/insert cycle using mostly server-side work for speed."""
    cur = cnx.cursor()

    # delete rows in one statement using RAND() to avoid Python-side selection
    cur.execute("DELETE FROM composite_key_table ORDER BY RAND() LIMIT %s", (BATCH_SIZE,))
    cnx.commit()

    # insert new random rows using a single INSERT..SELECT; generate numbers on the server
    insert_sql = f"""
    INSERT INTO composite_key_table
    (time_col, number_col, string_col, num_val1, num_val2, num_val3,
     string_val1, string_val2, string_val3, num_val4)
    SELECT
      NOW() + INTERVAL FLOOR(RAND()*1000) HOUR,
      FLOOR(RAND()*1000000),
      CONCAT('SKU_', FLOOR(RAND()*1000000)),
      FLOOR(RAND()*1000),
      ROUND(RAND()*1000,2),
      FLOOR(RAND()*1000000)+1000000,
      CONCAT('Product_', FLOOR(RAND()*1000000)),
      CONCAT('Category_', FLOOR(RAND()*1000000)),
      ELT(FLOOR(RAND()*4)+1,'Active','Inactive','Pending','Archived'),
      ROUND(RAND()*10,2)
    FROM (SELECT 1 FROM information_schema.COLUMNS LIMIT {BATCH_SIZE}) AS x;
    """
    cur.execute(insert_sql)
    cnx.commit()

    cur.close()


def main():
    cnx = mysql.connector.connect(**config)
    for i in range(LOOPS):
        print(f"Cycle {i+1}/{LOOPS}")
        do_cycle(cnx)
    cnx.close()

if __name__ == '__main__':
    main()
