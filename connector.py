import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="car_data"
    )

connection = get_connection()
if connection.is_connected():
    print("MySQL에 성공적으로 연결 되었습니다.")
else:
    print("실패")

connection.close()