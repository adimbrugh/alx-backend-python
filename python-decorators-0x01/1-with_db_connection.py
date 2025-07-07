

import sqlite3
import functools


# This decorator opens a database connection before calling the function
# and ensures that the connection is closed after the function execution.
# It injects the connection as the first argument to the decorated function.
# This allows the function to execute SQL queries without needing to manage the connection lifecycle.
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Open a database connection and pass it to the function."""
        conn = sqlite3.connect('users.db')
        try:
            # Ensure the function receives the connection as its first argument
            # Inject connection as first argument
            return func(conn, *args, **kwargs)
        finally:
            # Close the connection after the function execution
            # This ensures that the connection is always closed, even if an error occurs
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
