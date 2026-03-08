"""Script to concurrently insert 1,000,000 rows into `composite_key_table`.

Usage:
    python insert_composite_key_table.py

Adjust the connection parameters as needed for your environment.
"""

import threading
import mysql.connector
from mysql.connector import errorcode
import datetime

# database connection configuration
# values mirror docker-compose.yml environment
config = {
    'user': 'user',
    'password': 'password',  # from MYSQL_PASSWORD
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'test_db',   # from MYSQL_DATABASE
    'raise_on_warnings': True,
}

ROWS_PER_THREAD = 100000
THREAD_COUNT = 10  # will insert 1_000_000 rows


def insert_rows(start_id, count):
    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        # match init.sql schema:
        # time_col, number_col, string_col, num_val1, num_val2, num_val3,
        # string_val1, string_val2, string_val3, num_val4
        sql = """
            INSERT INTO composite_key_table \
            (time_col, number_col, string_col, num_val1, num_val2, num_val3, \
             string_val1, string_val2, string_val3, num_val4) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = []
        base_time = datetime.datetime.now()
        for i in range(count):
            offset_hours = (start_id + i) % 24
            tcol = base_time + datetime.timedelta(hours=offset_hours)
            num = 1000 + (start_id + i)  # arbitrary
            s_col = f"SKU_{start_id+i}"
            n1 = (start_id + i) % 1000
            n2 = round(((start_id + i) % 10000) * 0.01, 2)
            n3 = 1000000 + (start_id + i)
            sv1 = f"Product_{start_id+i}"
            sv2 = f"Category_{start_id+i}"
            sv3 = "Active"
            n4 = float(((start_id + i) % 100) * 0.1)
            data.append((tcol, num, s_col, n1, n2, n3, sv1, sv2, sv3, n4))

        cursor.executemany(sql, data)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if cnx is not None and cnx.is_connected():
            cnx.close()


def main():
    threads = []
    for t in range(THREAD_COUNT):
        start = t * ROWS_PER_THREAD
        thread = threading.Thread(target=insert_rows, args=(start, ROWS_PER_THREAD))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # note: errors may have occurred; check logs or exceptions for details
    print("Finished attempted insert of 1,000,000 rows into composite_key_table.")


if __name__ == '__main__':
    main()
