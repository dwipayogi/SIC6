from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Konfigurasi MongoDB
client = MongoClient('mongodb+srv://dwipayogi:X27wFWT5UMgfm_M@cluster0.tcyfwz4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['samsung']
collection_sensor = db['sensor']
collection_streamlit = db['streamlit']

@app.route('/')
def home():
    return "Welcome to Flask-MongoDB API"

@app.route('/data/latest', methods=['GET'])
def get_latest_data():
    latest_data = collection_sensor.find_one(sort=[("timestamp", -1)])
        
    if latest_data:
        latest_data['_id'] = str(latest_data['_id'])
        return jsonify(latest_data)
    else:
        return jsonify({"message": "No data found"}), 404

@app.route('/data/streamlit', methods=['GET'])
def get_streamlit_data():
    data = []
    for item in collection_streamlit.find():
        item['_id'] = str(item['_id'])
        data.append(item)
    return jsonify(data)

@app.route('/data/sensor', methods=['GET'])
def get_data():
    data = []
    for item in collection_sensor.find():
        item['_id'] = str(item['_id'])
        data.append(item)
    return jsonify(data)

@app.route('/data/temperature', methods=['GET'])
def get_temperature():
    data = []
    for item in collection_sensor.find():
        item['_id'] = str(item['_id'])
        data.append({
            'temperature': item['temperature'],
            'timestamp': item['timestamp']
        })
    return jsonify(data)

@app.route('/data/humidity', methods=['GET'])
def get_humidity():
    data = []
    for item in collection_sensor.find():
        item['_id'] = str(item['_id'])
        data.append({
            'humidity': item['humidity'],
            'timestamp': item['timestamp']
        })
    return jsonify(data)

@app.route('/data/motion', methods=['GET'])
def get_motion():
    data = []
    for item in collection_sensor.find():
        item['_id'] = str(item['_id'])
        data.append({
            'motion': item['motion'],
            'timestamp': item['timestamp']
        })
    return jsonify(data)

@app.route('/data/post/sensor', methods=['POST'])
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
    
    collection_sensor.insert_one(data)
    return jsonify({'message': 'Data berhasil disimpan'})

@app.route('/data/post/streamlit', methods=['POST'])
def post_streamlit_data():
    request_data = request.get_json()

    attentive_count = request_data.get('attentive_count')
    inattentive_count = request_data.get('inattentive_count')
    
    data = {
        'attentive_count': attentive_count,
        'inattentive_count': inattentive_count,
        'total_count': attentive_count + inattentive_count,
        'timestamp': datetime.now()
    }
    
    collection_streamlit.insert_one(data)
    return jsonify({'message': 'Data berhasil disimpan'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
