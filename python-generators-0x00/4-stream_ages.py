import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one from user_data table."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_user",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:  # ✅ loop 1
            yield float(age)

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")




def compute_average_age():
    """Computes average age using the generator without loading all data into memory."""
    total = 0
    count = 0
    for age in stream_user_ages():  # ✅ loop 2
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
