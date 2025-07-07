

import sqlite3
import functools

# Decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# Decorator to manage transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            # Commit the transaction if the function executes successfully
            # This ensures that all changes made during the function execution are saved to the database
            conn.commit()  # Commit on success
            return result
        except Exception as e:
            # If an error occurs, rollback the transaction to maintain database integrity
            # This ensures that no partial changes are saved to the database, preserving its state
            conn.rollback()  # Rollback on error
            print(f"[ERROR] Transaction failed: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
# This function will update the user's email and handle the transaction automatically.
# If an error occurs, it will rollback the transaction and print an error message.