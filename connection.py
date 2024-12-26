from psycopg2 import connect as pscon

class Connection:
    @staticmethod
    def connect_to_db(username, password):
        try:
            conn = pscon(
                dbname="UP02.01",
                user=username,
                password=password,
                host="localhost",
                port="5432"
            )
            return conn
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return None