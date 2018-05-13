from DB_connection import DbConnect

with DbConnect() as cur:
    sql = 'select * from `User` limit 101'
    cur.execute(sql)
    print(cur.rowcount)
