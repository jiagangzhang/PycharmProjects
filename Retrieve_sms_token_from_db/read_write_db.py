from DB_connection import DbConnect

with DbConnect(debug_logger=False) as cur:
    sql = 'select * from `User` limit 102'
    cur.execute(sql)
    print(cur.rowcount)
    # print(len(cur.fetchall()))
    value = cur.fetchone()
    print(value)
