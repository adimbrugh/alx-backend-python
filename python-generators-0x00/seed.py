import mysql.connector
import uuid
import csv
import os




def connect_db():  
    """Connects to MySQL server (without a specific DB)"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="your_mysql_user",
            password="your_mysql_password"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None




def create_database(connection): 
    """Creates the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")




def connect_to_prodev():
    """Connects to the ALX_prodev database"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="your_mysql_user",
            password="your_mysql_password",
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None




def create_table(connection):
    """Creates the user_data table in the ALX_prodev database"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")




def insert_data(connection, csv_file):
    """Inserts data from a CSV file into the user_data table"""
    try:
        if not os.path.exists(csv_file):
            print(f"{csv_file} not found.")
            return

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_data")
        if cursor.fetchone()[0] > 0:
            print("Data already exists. Skipping insert.")
            return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                uid = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (uid, row['name'], row['email'], row['age']))

        connection.commit()
        print("Data inserted successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
