import pymysql
from sshtunnel import SSHTunnelForwarder, create_logger

default_host = 'mm-ts-next.chinaeast.cloudapp.chinacloudapi.cn'
default_ssh_port = 1021
default_ssh_username = 'ubuntu'
default_ssh_pkey = 'loadtesters_rsa-2.pem'
default_remote_db_ip = '127.0.0.1'
default_remote_db_port = 3306


class DbConnect(object):
    """docstring for DbConnect"""
    def __init__(self,
                 host=default_host,
                 port=default_ssh_port,
                 username=default_ssh_username,
                 sshkey=default_ssh_pkey,
                 db_ip=default_remote_db_ip,
                 db_port=default_remote_db_port,
                 debug_logger=True
                 ):

        super(DbConnect, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.sshkey = sshkey
        self.db_ip = db_ip
        self.db_port = db_port
        if debug_logger:
            self.ssh_logger = create_logger(loglevel=1)  # debug
        else:
            self.ssh_logger = create_logger(loglevel='ERROR')  # only report error or fatal

    def __enter__(self):
        self.server = SSHTunnelForwarder(
            (self.host, self.port),  # 远端ssh server ip 和 ssh端口
            logger=self.ssh_logger,  # sshtunnel debug log 打印输出
            ssh_username=self.username,
            ssh_pkey=self.sshkey,
            remote_bind_address=(self.db_ip, self.db_port),  # 远端db server ip 和 db 端口
            # local_bind_address=('127.0.0.1', 3306)  # 本地连接db的端口
            )
        self.server.start()
        # log 本地绑定地址
        self.ssh_logger.log(level=10,
                            msg='Bind address is ' + str(self.server.local_bind_address)
                            )
        self.connection = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                          port=self.server.local_bind_port,
                                          user='root',
                                          password='3nations',
                                          database='mm')
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
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
