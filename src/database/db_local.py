import sqlite3

class LocalDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            print("Connected to the local database successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the local database.")

    def execute_query(self, query, params=None):
        if not self.connection:
            print("No database connection. Please connect first.")
            return None
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
