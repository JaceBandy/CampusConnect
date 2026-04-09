import os
from flask import Blueprint, render_template
import sqlite3
from utils.event_scraper import CampusEventScraper  # Import the scraper class

event_bp = Blueprint('event', __name__)

# Absolute path to your database
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'campusconnect.db')
DB_PATH = os.path.abspath(DB_PATH)

@event_bp.route("/events")
def events():
    # ---------------------------
    # Fetch internal events
    # ---------------------------
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT title, location, date FROM events")
    internal_events = cursor.fetchall()
    print("Internal events:", internal_events)  # Debugging

    # ---------------------------
    # Fetch external events via scraper
    # ---------------------------
    scraper = CampusEventScraper("https://okwueagles.com/coverage")
    
    try:
        scraped_events = scraper.scrape_events()
        scraper.save_to_db(scraped_events)
    except Exception as e:
        print("Scraping failed:", e)

    # Query database to get external_events
    cursor.execute("SELECT title, location, date, description FROM external_events")
    external_events = cursor.fetchall()
    print("External events:", external_events)  # Debugging

    conn.close()

    # Pass both internal and external events to template
    return render_template("events.html", internal_events=internal_events, external_events=external_events)