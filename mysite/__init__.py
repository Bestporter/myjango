"""
其实python解释器在运行django程序时，django的orm底层操作数据库的python模块
默认是mysqldb而非pymysql，然而对于解释器而言，python2.x解释器支持的操作数据库的模块是mysqldb，
而python3.x解释器支持的操作数据库的模块则是pymysql，，毫无疑问，
目前我们的django程序都是运行于python3.x解释器下，
于是我们需要修改django的orm默认操作数据库的模块为pymysql，具体做法如下
在项目目录下的__init__文件中添加下面两行
"""


import pymysql
pymysql.intall_as_MySQLdb()
