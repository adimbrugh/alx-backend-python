import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields batches of rows from user_data table."""
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
            yield batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass




def batch_processing(batch_size):
    """Generator that processes batches and yields users over age 25."""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered_batch = (user for user in batch if float(user[3]) > 25)  # generator expression
        for user in filtered_batch:  # loop 2
            yield user
