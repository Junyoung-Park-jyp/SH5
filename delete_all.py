import pymysql

def delete_all_data(host, user, password, database):
    # MySQL 데이터베이스에 연결
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 외래 키 제약 조건 비활성화
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # 데이터베이스 내 모든 테이블 이름 가져오기
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_type = 'BASE TABLE';", (database,))
            tables = cursor.fetchall()

            # 각 테이블의 데이터를 삭제
            for table in tables:
                table_name = table['table_name']
                cursor.execute(f"TRUNCATE TABLE `{table_name}`;")
                print(f"Truncated table {table_name}")

            # 외래 키 제약 조건 다시 활성화
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        # 변경사항을 커밋
        connection.commit()

    finally:
        connection.close()

# 함수 호출
delete_all_data(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database_name'
)
