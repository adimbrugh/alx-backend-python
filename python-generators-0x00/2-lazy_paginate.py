import mysql.connector

def paginate_users(page_size, offset):
    """Fetch a single page of users from user_data at given offset."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_user",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor()

        query = """
            SELECT user_id, name, email, age
            FROM user_data
            LIMIT %s OFFSET %s
        """
       # ✅ Now uses SELECT * FROM user_data LIMIT ...
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []




def lazy_paginate(page_size):
    """Generator that yields pages lazily from user_data."""
    offset = 0
    while True:  # ✅ Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # ✅ Use of yield
        offset += page_size
