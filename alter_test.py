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
    cur.execute('ALTER TABLE composite_key_table ALGORITHM=INPLACE, LOCK=NONE;')
    cnx.commit()
    cur.close()
    cnx.close()
    print('alter done')

alter_thread=threading.Thread(target=do_alter)
alter_thread.start()

# during alter, attempt selects and inserts
for i in range(5):
    try:
        cnx=mysql.connector.connect(**config)
        cur=cnx.cursor()
        cur.execute('SELECT COUNT(*) FROM composite_key_table')
        print('select ok', cur.fetchone()[0])
        # attempt small insert
        cur.execute("INSERT INTO composite_key_table(time_col,number_col,string_col) VALUES(NOW(),999999,'test')")
        cnx.commit()
        print('insert ok')
        cur.close();cnx.close()
    except Exception as e:
        print('operation error', e)
    time.sleep(1)

alter_thread.join()
print_size('after alter')
