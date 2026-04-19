import os
import duckdb

class OnlineDatabase:
    def __init__(self, db_path):
        self.conn = duckdb.connect(db_path)
        self.initialize_database()

    def initialize_database(self):
        # Initialize the database with any required tables or schema
        pass

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        return cursor.fetchall()
