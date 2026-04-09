import sqlite3
import os

DB_PATH = "db/campusconnect.db"

# Remove existing DB for a clean seed (optional in dev environment)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create tables manually or run schema.sql separately if preferred
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
)''')

# Create Users Seed Data
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Alice", "Aly"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Bob", "art, Bobby"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Charlie", "Chaz"))

# Internal Events Seed Data
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Music Night", "Student Center", "2025-04-05"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Hackathon", "Library", "2025-04-01"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Art Exhibition", "Gallery", "2025-04-10"))
c.execute("SELECT title, location, date FROM events")

# -----------------------------
# External Events Table + Seed
# -----------------------------
c.execute('''CREATE TABLE IF NOT EXISTS external_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    location TEXT,
    description TEXT
)''')

# Clear existing data (optional for clean reseed)
c.execute("DELETE FROM external_events")

# Insert sample external events
c.execute("""
INSERT INTO external_events (title, date, location, description)
VALUES (?, ?, ?, ?)
""", ("Guest Speaker Event", "2026-04-12", "Auditorium", "A guest speaker discusses career growth"))

c.execute("""
INSERT INTO external_events (title, date, location, description)
VALUES (?, ?, ?, ?)
""", ("Spring Festival", "2026-04-15", "Campus Lawn", "Annual spring celebration with food and games"))


# -----------------------------
# API Data Table + Seed
# -----------------------------
c.execute('''CREATE TABLE IF NOT EXISTS api_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    temperature REAL,
    windspeed REAL
)''')

# Clear existing data
c.execute("DELETE FROM api_data")

# Insert sample API data
c.execute("""
INSERT INTO api_data (date, temperature, windspeed)
VALUES (?, ?, ?)
""", ("2026-04-09", 70.5, 8.2))

c.execute("""
INSERT INTO api_data (date, temperature, windspeed)
VALUES (?, ?, ?)
""", ("2026-04-10", 68.0, 12.5))

conn.commit()
conn.close()