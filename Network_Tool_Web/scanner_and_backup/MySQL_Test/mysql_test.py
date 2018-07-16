import mysql.connector
import mysql


sql_connector = mysql.connector.connect(user='python',
                                        password='yzh8RB0Bcw1VivO3',
                                        host='localhost',
                                        database='MikrotikDB')

cursor = sql_connector.cursor()

add_mikrotik = ("INSERT INTO devices "
                "(host, name, mac)"
                "VALUES (%s, %s, %s)", 'Host', 'Name', 'MAC')

cursor.execute(add_mikrotik)
sql_connector.commit()

cursor.close()
sql_connector.close()
