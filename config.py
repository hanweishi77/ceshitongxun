# 连接mysql数据库的配置
HOSTNAME = "127.0.0.1"                                    # 本机
PORT = 3306                                               # 端口
USERNAME = "root"                                         # 连接用户
PASSWORD = "123456"                                       # 用户密码
DATABASE = "testBrowser"                                 # 数据库
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI                          # SQLALCHEMY_DATABASE_URI为系统变量名
SQLALCHEMY_TRACK_MODIFICATIONS = False                    # 设置是否跟踪数据库的修改情况，一般不跟踪
SQLALCHEMY_ECHO = True                                    # 数据库操作时后台显示原始SQL语句
