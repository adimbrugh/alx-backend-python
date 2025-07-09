

import asyncio
import aiosqlite

DB_NAME = "users.db"  # SQLite database file

# Create sample table and data (optional for demo)
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
            print("\nAll Users:")
            for row in rows:
                print(row)

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)

# Run both queries concurrently
async def fetch_concurrently():
    await setup_database()  # comment this if DB is already set up
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
# This script uses asyncio and aiosqlite to fetch data from an SQLite database concurrently.
# It creates a sample table and data, then fetches all users and users older than