from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Konfigurasi MongoDB
client = MongoClient('mongodb+srv://dwipayogi:X27wFWT5UMgfm_M@cluster0.tcyfwz4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['samsung']
collection = db['sensor']

@app.route('/')
def home():
    return "Welcome to Flask-MongoDB API"

@app.route('/data', methods=['GET'])
def get_data():
    data = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        data.append(item)
    return jsonify(data)

@app.route('/data/temperature', methods=['GET'])
def get_temperature():
    data = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        data.append({
            'temperature': item['temperature'],
            'timestamp': item['timestamp']
        })
    return jsonify(data)

@app.route('/data/humidity', methods=['GET'])
def get_humidity():
    data = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        data.append({
            'humidity': item['humidity'],
            'timestamp': item['timestamp']
        })
    return jsonify(data)

@app.route('/data/motion', methods=['GET'])
def get_motion():
    data = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        data.append({
            'motion': item['motion'],
            'timestamp': item['timestamp']
        })
    return jsonify(data)

@app.route('/data/post', methods=['POST'])
def post_data():
    request_data = request.get_json()

    temp = request_data.get('temperature')
    hum = request_data.get('humidity')
    motion = request_data.get('motion')
    
    data = {
        'temperature': temp,
        'humidity': hum,
        'motion': motion,
        'timestamp': datetime.now()
    }
    
    # Masukkan data ke MongoDB
    collection.insert_one(data)
    return jsonify({'message': 'Data berhasil disimpan'})

if __name__ == '__main__':
    app.run(debug=True)
