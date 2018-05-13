import pymysql
from sshtunnel import SSHTunnelForwarder, create_logger


class DbConnect(object):
    """docstring for DbConnect"""
    def __init__(self, host='', port=20, ):
        super(DbConnect, self).__init__()
        self.host = host
        self.port = port

    def __enter__(self):
        self.server = SSHTunnelForwarder(
            ('mm-ts-next.chinaeast.cloudapp.chinacloudapi.cn', 1021),  # 远端ssh server ip 和 ssh端口
            logger=create_logger(loglevel=1),  # sshtunnel debug log 打印输出
            ssh_username="ubuntu",
            ssh_pkey="loadtesters_rsa-2.pem",
            remote_bind_address=('127.0.0.1', 3306),  # 远端db server ip 和 db 端口
            # local_bind_address=('127.0.0.1', 3306)  # 本地连接db的端口
            )
        self.server.start()
        print(self.server.local_bind_address)
        print(self.server.local_bind_port)
        self.connection = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                          port=self.server.local_bind_port,
                                          user='root',
                                          password='3nations',
                                          database='mm')
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        self.server.stop()

    def run_sql(self, sql):
        self.cursor.execute(sql)


def connect_db():
    with SSHTunnelForwarder(
            ('mm-ts-next.chinaeast.cloudapp.chinacloudapi.cn', 1021),  # 远端ssh server ip 和 ssh端口
            logger=create_logger(loglevel=1),  # sshtunnel debug log 打印输出
            ssh_username="ubuntu",
            ssh_pkey="loadtesters_rsa-2.pem",
            remote_bind_address=('127.0.0.1', 3306),  # 远端db server ip 和 db 端口
            # local_bind_address=('127.0.0.1', 3306)  # 本地连接db的端口
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
        # server.stop()

if __name__ == '__main__':
    connect_db()
