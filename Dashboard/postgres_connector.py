import psycopg2


class PostgresDB:
    def __init__(self, host, port, db, user, pw):
        try:
            self.conn = psycopg2.connect(
                host=host, port=port, database=db, user=user, password=pw
            )
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def write(self, table: str, data: list):
        template = ",".join(["%s"] * len(data))
        insert_query = f"INSERT INTO {table} VALUES({template})"
        try:
            self.cur.execute(insert_query, data)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error writing to DB: {e}")

    def writemany(self, table: str, data: list[tuple]):
        records_list_template = ",".join(["%s"] * len(data[0]))
        insert_query = f"INSERT INTO {table} VALUES({records_list_template})"
        try:
            self.cur.executemany(insert_query, data)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error writing to DB: {e}")

    def read_one(self, query: str):
        try:
            self.cur.execute(query)
            result = self.cur.fetchone()
        except psycopg2.Error as e:
            print(f"Error reading from DB: {e}")
        return result

    def read_all(self, query: str):
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error reading from DB: {e}")
        return result

    def close(self):
        self.cur.close()
        self.conn.close()

    def __del__(self):
        self.close()
