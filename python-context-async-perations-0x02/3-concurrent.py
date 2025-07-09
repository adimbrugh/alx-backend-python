

import asyncio
import aiosqlite

DB_NAME = "users.db"  # SQLite database file

# Optional: Create sample table and seed data
async def setup_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
        """)
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 25),
            ("Bob", 42),
            ("Charlie", 38),
            ("Diana", 45),
        ])
        await db.commit()

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows

# Run both queries concurrently and return the data
async def fetch_concurrently():
    await setup_database()  # Comment this out if DB already exists

    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\nAll Users:")
    for user in all_users:
        print(user)

    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
# This script uses asyncio and aiosqlite to fetch data from an SQLite database concurrently.
# It creates a sample table and seeds it with data, then fetches all users and those