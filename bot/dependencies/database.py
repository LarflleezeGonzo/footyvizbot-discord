import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, parameters=None):
        if parameters is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, parameters)
        self.connection.commit()

    def fetch_query(self, query, parameters=None):
        if parameters is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
