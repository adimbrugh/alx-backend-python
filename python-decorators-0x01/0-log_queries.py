

import sqlite3
import functools
from datetime import datetime

# This script demonstrates how to log SQL queries with timestamps using a decorator.
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #print(f"[{timestamp}] Executing SQL query...")
        if query:
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print("[LOG] No query found to log.")
        return func(*args, **kwargs)
    return wrapper



@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
