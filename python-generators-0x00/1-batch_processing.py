import mysql.connector

def stream_users_in_batches(batch_size):
    """Yields batches of users from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_user",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # ✅ Yielding a batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


def batch_processing(batch_size):
    """Yields users older than 25 from streamed batches."""
    for batch in stream_users_in_batches(batch_size):  # ✅ Loop 1
        for user in batch:  # ✅ Loop 2
            if float(user[3]) > 25:
                yield user  # ✅ Yielding each filtered user
