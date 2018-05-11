import pymysql
from sshtunnel import SSHTunnelForwarder, create_logger


class DbConnect(object):
    """docstring for DbConnect"""
    def __init__(self, host='', port=20, ):
        super(DbConnect, self).__init__()
        self.host = host
        self.port = port


def connect_db():
    with SSHTunnelForwarder(
            ('mm-ts-next.chinaeast.cloudapp.chinacloudapi.cn', 1021),  # 远端server ssh ip 和端口
            # logger=create_logger(loglevel=1),  # sshtunnel debug log 打印输出
            ssh_username="ubuntu",
            ssh_pkey="loadtesters_rsa-2.pem",
            remote_bind_address=('127.0.0.1', 3306),  # 远端server ip 和 db 端口
            local_bind_address=('127.0.0.1', 3306)  # 本地连接db的端口
            ) as server:

        print(server.local_bind_address)
        print(server.local_bind_port)
        db = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                             port=server.local_bind_port,
                             user='root',
                             password='3nations',
                             database='mm')
        cursor = db.cursor()
        cursor.execute("show tables")
        sql = 'select * from `User` limit 101'
        cursor.execute(sql)
        print(cursor.rowcount)
        # print(len(cursor.fetchall()))
        server.stop()

if __name__ == '__main__':
    connect_db()
