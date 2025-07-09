

import mysql.connector


# This module provides a context manager for managing database connections using MySQL Connector/Python.
class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Establish a database connection and return a cursor."""
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self.cursor   # Return the cursor to use in the block

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"Exception occurred: {exc_value}")
        return False  # Don't suppress exceptions



# --- Usage Example ---

if __name__ == "__main__":
    # Example usage of the DatabaseConnection context manager
    # Make sure to replace the database credentials with your actual values.
    db_params = {
        "host": "localhost",
        "user": "your_user",
        "password": "your_password",
        "database": "your_database"
    }

    # Using the DatabaseConnection context manager
    with DatabaseConnection(**db_params) as cursor:
        # Example query to fetch data from a table named 'users'
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            # Process each row as needed
            print(row)
