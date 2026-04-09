from flask import Blueprint, render_template
from utils.api_client import APIClient
import sqlite3
import os

api_bp = Blueprint("api", __name__)

# Absolute path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "campusconnect.db")
DB_PATH = os.path.abspath(DB_PATH)

@api_bp.route("/api")
def api():
    """
    Fetches weather data from Open-Meteo API, saves it to the database,
    and passes it to the api.html template.
    """

    # ---------------------------
    # Fetch API data
    # ---------------------------
    client = APIClient(
        "https://api.open-meteo.com/v1/forecast?latitude=36.75&longitude=-95.98&current_weather=true"
    )
    data = client.fetch_data()
    client.save_to_db(data)

    # ---------------------------
    # Query api_data table from DB
    # ---------------------------
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT date, temperature, windspeed FROM api_data")
    api_data = cursor.fetchall()

    conn.close()

    # ---------------------------
    # Pass data to template
    # ---------------------------
    return render_template("api.html", api_data=api_data)