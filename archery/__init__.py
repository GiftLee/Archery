version = (1, 7, 1)
display_version = '.'.join(str(i) for i in version)
import pymysql
pymysql.install_as_MySQLdb()