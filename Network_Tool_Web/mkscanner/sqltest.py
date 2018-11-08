import mysql.connector


identity_fixed = 'Test'
host = '172.31.16.17'


sql_connector = mysql.connector.connect(user='python',
                                                    password='yzh8RB0Bcw1VivO3',
                                                    host='localhost',
                                                    database='test')

cursor = sql_connector.cursor()

check_query = "SELECT ip FROM devices" "WHERE" "ip='172.31.16.17' "

cursor.execute(check_query)
sql_connector.commit()
cursor.close()
sql_connector.close()