import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from collections import defaultdict
import os

class Connect:
    def __init__(self):
        load_dotenv()  # Load the .env file
        self.database = os.getenv("DB_DATABASE")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return [dict(row) for row in results]

    def close(self):
        self.connection.close()

    def query(self, query, params=None):
        self.connect()
        result = self.execute_query(query, params)
        self.close()
        return result
