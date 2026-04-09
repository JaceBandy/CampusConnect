import requests
import sqlite3

class APIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        """
        Sends a GET request to the API and returns JSON data.
        Example API: Open-Meteo weather API
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print("API request failed:", e)
            return None

    def save_to_db(self, data):
        """
        Stores API data into the api_data table.
        Expects data dictionary with keys: current_weather -> temperature, windspeed, time
        """

        if data is None:
            print("No data to save to DB")
            return

        conn = sqlite3.connect("db/campusconnect.db")
        cursor = conn.cursor()

        # Clear old data to prevent duplicates
        cursor.execute("DELETE FROM api_data")

        try:
            weather = data.get("current_weather")
            if weather:
                cursor.execute("""
                    INSERT INTO api_data (date, temperature, windspeed)
                    VALUES (?, ?, ?)
                """, (weather.get("time"), weather.get("temperature"), weather.get("windspeed")))
        except Exception as e:
            print("Failed to insert API data:", e)

        conn.commit()
        conn.close()