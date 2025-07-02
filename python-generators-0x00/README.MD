# Python Generators Project - Task 1: Streaming Data from SQL with Generators

This project explores advanced Python generators by applying them in real-world scenarios involving large data processing, live updates, and memory-efficient computations.

## Task 1: SQL Row Streaming with Python

This task sets up a **MySQL database** and populates it with sample user data from a CSV file. The goal is to simulate real-world, large-scale data processing which will later be streamed using generators.

### 🔧 File: `seed.py`

#### Purpose:
- Connects to a local MySQL server
- Creates a database called `ALX_prodev` (if not already present)
- Creates a table `user_data` with proper schema and indexing
- Loads data from `user_data.csv` into the table
- Ensures data is not duplicated on repeated runs

---

### 🧪 Database Schema: `user_data`

| Field Name | Type     | Description                       |
|------------|----------|-----------------------------------|
| user_id    | UUID     | Primary key, indexed, auto-gen.   |
| name       | VARCHAR  | User full name (required)         |
| email      | VARCHAR  | Email address (required)          |
| age        | DECIMAL  | Age (required)                    |

---

### 📁 File Structure

python-generators-0x00/
├── 0-main.py
├── seed.py
├── user_data.csv
└── README.md


---

### 🚀 Usage Instructions

1. **Ensure MySQL is installed and running** on your machine.
2. **Modify credentials** in `seed.py`:
   ```python
   user="your_mysql_user",
   password="your_mysql_password",
