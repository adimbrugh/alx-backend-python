

import time
import sqlite3
import functools



# Global in-memory cache
query_cache = {}

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



# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get query from kwargs or positional arguments
        query = kwargs.get("query") if "query" in kwargs else (args[1] if len(args) > 1 else None)

        if query in query_cache:
            # Return cached result if available
            print(f"[CACHE] Returning cached result for: {query}")
            return query_cache[query]
        
        # If not cached, execute the query and cache the result
        print(f"[CACHE] No cache found for: {query}. Executing query...")
        result = func(conn, *args, **kwargs) # Call the original function
        # Store the result in the cache
        query_cache[query] = result
        return result
    return wrapper



@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

# Print the results
print(users_again)
