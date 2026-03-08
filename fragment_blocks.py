import mysql.connector
import time

config = {
    'user': 'user',
    'password': 'password',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'test_db',
}

def delete_blocks():
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    
    # Get range
    cur.execute("SELECT MIN(number_col), MAX(number_col) FROM composite_key_table")
    min_id, max_id = cur.fetchone()
    print(f"ID range: {min_id} to {max_id}")
    
    # Delete blocks of 3000 rows every 5000 rows (60% delete)
    block_size = 3000
    step = 5000
    
    total_deleted = 0
    start_time = time.time()
    
    for start in range(min_id, max_id + 1, step):
        end = start + block_size - 1
        # Delete range
        cur.execute(f"DELETE FROM composite_key_table WHERE number_col BETWEEN {start} AND {end}")
        deleted = cur.rowcount
        total_deleted += deleted
        cnx.commit()
        
        if total_deleted % 100000 < deleted: # rough progress check
             print(f"Deleted {total_deleted} rows so far...")
             
    print(f"Finished. Total deleted: {total_deleted}")
    print(f"Time taken: {time.time() - start_time:.2f}s")
    
    cur.close()
    cnx.close()

if __name__ == '__main__':
    delete_blocks()
