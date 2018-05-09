import MySQLdb
from sshtunnel import SSHTunnelForwarder


def connect_db():
    with SSHTunnelForwarder(
            ('sshhost.domain.com', 22),  # B机器的配置
            ssh_password="sshpasswd",
            ssh_username="sshusername",
            remote_bind_address=('mysqlhost.domain.com', 3306)) as server:  # A机器的配置

        conn = MySQLdb.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                               port=server.local_bind_port,
                               user='user',
                               passwd='password',
                               db='dbname')
        cursor = conn.cursor()
        cursor.execute("show tables")
        print(server.local_bind_address)
        print(len(cursor.fetchall()))
        server.stop()