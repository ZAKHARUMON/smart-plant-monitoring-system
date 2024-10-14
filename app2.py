from flask import Flask, jsonify, render_template
import serial

app = Flask(__name__)

# Set up serial communication with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to your port

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/data')
def get_data():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # Read line from Arduino
        data = {}
        
        if "SoilMoisture:" in line:
            data['soilMoisture'] = int(line.split(":")[1])
        
        elif "Temperature:" in line:
            data['temperature'] = float(line.split(":")[1])
        
        elif "Humidity:" in line:
            data['humidity'] = float(line.split(":")[1])
        
        return jsonify(data)
    
    return jsonify({"error": "No data available"})

if __name__ == '__main__':
    app.run(debug=True)
