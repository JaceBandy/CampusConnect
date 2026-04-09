import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

class CampusEventScraper:    
    def __init__(self, url):
        self.url = url

    def scrape_events(self):
        """
        Sends a GET request to the OKWU athletics coverage page
        and extracts event data from table rows.
        """

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        events = []

        # Find all table rows
        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            # Skip rows that don't have enough data
            if len(cols) >= 3:
                try:
                    time = cols[0].text.strip()
                    sport = cols[1].text.strip()
                    opponent = cols[2].text.strip()

                    # Format into database fields
                    title = f"{sport} vs {opponent}"
                    date = time
                    location = "OKWU Athletics"
                    description = "Live sports event from OKWU coverage page"

                    events.append((title, date, location, description))

                except Exception as e:
                    print("Error parsing row:", e)

        return events

    def save_to_db(self, events):
        """
        Saves scraped events into the external_events table.
        """

        conn = sqlite3.connect("db/campusconnect.db")
        cursor = conn.cursor()

        # Clear old data to avoid duplicates
        cursor.execute("DELETE FROM external_events")

        for event in events:
            cursor.execute("""
                INSERT INTO external_events (title, date, location, description)
                VALUES (?, ?, ?, ?)
            """, event)

        conn.commit()
        conn.close()