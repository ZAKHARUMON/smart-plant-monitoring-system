from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the SQLite Database
def init_db():
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        humidity REAL,
                        temperature REAL,
                        soil_moisture INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Route to handle sensor data (HTTP POST)
@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    humidity = data['humidity']
    temperature = data['temperature']
    soil_moisture = data['soil_moisture']

    # Save to database
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO sensor_data (humidity, temperature, soil_moisture)
                      VALUES (?, ?, ?)''', (humidity, temperature, soil_moisture))
    conn.commit()
    conn.close()

    return "Data received successfully!"

# Route to fetch the latest data (for displaying on the webpage)
@app.route('/fetch_data')
def fetch_data():
    conn = sqlite3.connect('plant_monitoring.db')
    cursor = conn.cursor()
    cursor.execute('SELECT humidity, temperature, soil_moisture, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()

    if row:
        data = {
            'humidity': row[0],
            'temperature': row[1],
            'soil_moisture': row[2],
            'timestamp': row[3]
        }
    else:
        data = {
            'humidity': '--',
            'temperature': '--',
            'soil_moisture': '--',
            'timestamp': '--'
        }
    
    return jsonify(data)

# Route to serve the webpage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
