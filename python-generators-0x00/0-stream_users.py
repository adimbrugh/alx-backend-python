import mysql.connector

def stream_users():
    """Generator that streams user data from the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_user",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
