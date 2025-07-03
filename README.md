# Python Generators – Memory-Efficient SQL Data Processing

This project demonstrates how to use Python generators to efficiently handle large datasets from a MySQL database. It simulates real-world tasks such as streaming user data, processing in batches, paginating lazily, and computing aggregate values — all without loading the entire dataset into memory.

---

## 🔧 Project Setup

Start by preparing the environment and database:

- `seed.py` connects to MySQL, creates the `ALX_prodev` database (if it doesn't exist), creates the `user_data` table with the following schema:

| Field    | Type     | Description                    |
|----------|----------|--------------------------------|
| user_id  | UUID     | Primary key, indexed           |
| name     | VARCHAR  | Required, user’s full name     |
| email    | VARCHAR  | Required, user’s email         |
| age      | DECIMAL  | Required, user’s age           |

- The script also loads sample data from a CSV file `user_data.csv` and avoids inserting duplicate data.

Run the setup:
```bash
./0-main.py

---

🧠 Generator-Based Data Processing
The remaining scripts use Python’s yield statement to implement memory-efficient operations on the user_data table.

---

##Streaming Rows One-by-One:
0-stream_users.py defines a generator function stream_users() that connects to the database and yields rows from the user_data table one at a time using a cursor iterator.

This method avoids using .fetchall() and is suitable for processing large tables efficiently.

for user in stream_users():
    print(user)

---

## Batch Processing with Filtering:
1-batch_stream.py implements two functions:

-stream_users_in_batches(batch_size) yields batches of rows using cursor.fetchmany().
-batch_processing(batch_size) filters and yields only users with age > 25.

The script uses a generator expression to avoid additional loops and keeps memory usage low.

python
for user in batch_processing(10):
    print(user)

---


## Lazy Pagination:
2-lazy_paginate.py simulates paginated access to the database by lazily fetching pages using SQL's LIMIT and OFFSET.

It includes:
-paginate_users(page_size, offset) – fetches a page of users.

-lazy_paginate(page_size) – a generator that yields the next page only when needed.

This is useful for API endpoints or infinite scroll UIs.

python
for page in lazy_paginate(5):
    print(page)

---

## Memory-Efficient Average Age Calculation:
3-average_age.py defines:

-stream_user_ages() – a generator that yields ages from the table one by one.

-compute_average_age() – computes the average age without using SQL AVG() or loading all rows.

It uses only 2 loops and prints the result:

Test:
python
compute_average_age()

---


## 📁 Directory Structure

python-generators-0x00/
├── seed.py                # Setup script: DB and table creation, CSV import
├── user_data.csv          # CSV file with sample user data
├── 0-main.py              # Main runner script to prepare the database
├── 0-stream_users.py      # Stream one row at a time
├── 1-batch_stream.py      # Batch stream and filter users over age 25
├── 2-lazy_paginate.py     # Lazily fetch paginated data
├── 3-average_age.py       # Compute average age using a generator
├── README.md              # Documentation (this file)

---


## ✅ Requirements:

-Python 3.8+
-MySQL server installed and running
-Update MySQL credentials in all scripts:

python
user="your_mysql_user",
password="your_mysql_password",

---

## 🎯 Key Concepts Demonstrated:

-Python generators and yield
-Lazy evaluation
-Cursor iteration and fetchmany()
-Filtering using generator expressions
-Aggregate computation without loading all data
-Avoidance of SQL aggregate functions (e.g., AVG())

---