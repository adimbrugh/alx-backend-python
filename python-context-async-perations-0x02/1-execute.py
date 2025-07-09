

import mysql.connector


# This module provides a context manager for executing SQL queries using MySQL Connector/Python.
class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

        # Use your own MySQL connection info or load from env
        self.config = {
            'host': 'localhost',
            'user': 'your_user',
            'password': 'your_password',
            'database': 'your_database'
        }

    def __enter__(self):
        """Establish a database connection, execute the query, and return the result."""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.query, self.params)
            self.result = self.cursor.fetchall()
            return self.result  # Return the result directly
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return None
        
    def __exit__(self, exc_type, exc_value, traceback):
        """Close the cursor and connection, handle exceptions."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"Exception: {exc_value}")
        return False  # Don't suppress exceptions
    
    
    
# --- Usage Example --- 

# This part is not executed when the module is imported, but can be used for testing or demonstration purposes.
if __name__ == "__main__":
    # Example usage of the ExecuteQuery context manager
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)

    with ExecuteQuery(query, params) as results:
        if results is not None:
            for row in results:
                print(row)  # Process each row as needed
        else:
            print("No results found or an error occurred.")
# This code defines a context manager for executing SQL queries using MySQL Connector in Python.
# It handles connection management, error handling, and returns results directly.
# The context manager ensures that resources are cleaned up properly after use.
# The example at the end shows how to use the context manager to execute a query and process
