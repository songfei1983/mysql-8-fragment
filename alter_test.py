import mysql.connector, threading, time

config={'user':'user','password':'password','host':'127.0.0.1','port':3306,'database':'test_db'}

# function to print size

def print_size(label):
    cnx=mysql.connector.connect(**config)
    cur=cnx.cursor()
    cur.execute("SELECT round(data_free/1024/1024,2) FROM information_schema.TABLES WHERE table_schema='test_db' AND table_name='composite_key_table';")
    print(label, cur.fetchone()[0])
    cur.close();cnx.close()

print_size('before alter')

# start alter in separate thread

def do_alter():
    cnx=mysql.connector.connect(**config)
    cur=cnx.cursor()
    cur.execute('ALTER TABLE composite_key_table ALGORITHM=INPLACE, LOCK=NONE, ENGINE=InnoDB;')
    cnx.commit()
    cur.close()
    cnx.close()
    print('alter done')

alter_thread=threading.Thread(target=do_alter)
alter_thread.start()

# during alter, attempt selects and inserts
while alter_thread.is_alive():
    try:
        start_t = time.time()
        cnx=mysql.connector.connect(**config)
        cur=cnx.cursor()
        cur.execute('SELECT COUNT(*) FROM composite_key_table')
        count_res = cur.fetchone()[0]
        # attempt small insert
        cur.execute("INSERT INTO composite_key_table(time_col,number_col,string_col,num_val1,num_val2,num_val3,string_val1,string_val2,string_val3,num_val4) VALUES(NOW(),999999,'test',0,0.0,0,'test','test','Active',0.0)")
        cnx.commit()
        print(f"select count={count_res}, insert ok, time={time.time()-start_t:.2f}s")
        cur.close();cnx.close()
    except Exception as e:
        print('operation error', e)
    time.sleep(0.5)

alter_thread.join()
print_size('after alter')
