"""Perform repeated deletions and insertions to increase table fragmentation."""

import mysql.connector
import random
from datetime import datetime, timedelta

config = {
    'user': 'user',
    'password': 'password',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'test_db',
}

LOOPS = 20
BATCH_SIZE = 100000

def do_cycle(cnx):
    cur = cnx.cursor()
    # optimized deletion: randomly pick IDs in known range 1000..40001000
    # instead of ORDER BY RAND()
    # We'll generate BATCH_SIZE random numbers
    min_id = 1000
    max_id = 40000000 + 1000
    keys = [random.randint(min_id, max_id) for _ in range(BATCH_SIZE)]
    
    if keys:
        # batch deletes to avoid huge SQL statements
        chunk_size = 5000
        total_deleted = 0
        for i in range(0, len(keys), chunk_size):
            chunk = keys[i:i + chunk_size]
            placeholder = ','.join(['%s'] * len(chunk))
            delete_sql = f"DELETE FROM composite_key_table WHERE number_col IN ({placeholder})"
            cur.execute(delete_sql, chunk)
            total_deleted += cur.rowcount
            cnx.commit()
        print(f"Deleted {total_deleted} rows")
        
    # insert same number of new rows
    base_time = datetime.now()
    data = []
    for i in range(BATCH_SIZE):
        offset = random.randint(0, 1000)
        tcol = base_time + timedelta(hours=offset)
        num = random.randint(1000, 40000000) # Updated range to match dataset
        s_col = f"SKU_{random.randint(1,1000000)}"
        n1 = random.randint(0, 999)
        n2 = round(random.random()*1000, 2)
        n3 = random.randint(1000000, 2000000)
        sv1 = f"Product_{random.randint(1,1000000)}"
        sv2 = f"Category_{random.randint(1,1000000)}"
        sv3 = random.choice(["Active","Inactive","Pending","Archived"])
        n4 = round(random.random()*10,2)
        data.append((tcol, num, s_col, n1, n2, n3, sv1, sv2, sv3, n4))
    sql = ("INSERT INTO composite_key_table (time_col, number_col, string_col, num_val1, num_val2, num_val3, "
           "string_val1, string_val2, string_val3, num_val4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    # chunk inserts
    chunk_size = 5000
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        cur.executemany(sql, chunk)
        cnx.commit()
    print(f"Inserted {len(data)} rows")
    cur.close()


def main():
    cnx = mysql.connector.connect(**config)
    try:
        for i in range(LOOPS):
            print(f"Cycle {i+1}/{LOOPS}")
            do_cycle(cnx)
    finally:
        cnx.close()

if __name__ == '__main__':
    main()
