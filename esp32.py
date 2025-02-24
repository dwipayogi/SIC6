from umqtt.simple import MQTTClient
import network
import time
import json
import machine
import dht
import urequests

# Konfigurasi WiFi
SSID = "OMAHKU"
PASSWORD = "20192019"

# Konfigurasi HTTP Server (Flask API)
HTTP_URL = "http://krgv217k-5000.asse.devtunnels.ms/data/post"

# Konfigurasi MQTT
MQTT_CLIENT_ID = "67b82d7f661d433259fe955d"
MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_PORT = 1883
MQTT_USER = "BBUS-frJkaCpYUytxHEwMPNiqZWtxXoq7kc"
MQTT_PASSWORD = "BBUS-frJkaCpYUytxHEwMPNiqZWtxXoq7kc"
MQTT_TOPIC = "/v2.0/devices/samsung"

# Koneksi ke WiFi
print("Connecting to WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.1)
print("\nWiFi Connected!")

# Koneksi ke MQTT Server
print("Connecting to MQTT server...")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
client.connect()
print("MQTT Connected!")

# Inisialisasi Sensor
dht_pin = machine.Pin(23)
sensor = dht.DHT11(dht_pin)
pir = machine.Pin(34, machine.Pin.IN)


while True:
    sensor.measure()
    data_sensor = {
        "temperature": sensor.temperature(),
        "humidity": sensor.humidity(),
        "motion": pir.value()
    }
    message = json.dumps(data_sensor)

    print(f"Publishing to {MQTT_TOPIC}: {message}")
    
    # Publish Data ke Ubidots    
    client.publish(MQTT_TOPIC, message.encode())
    
    # Kirim Data ke MongoDB melalui API Flask    
    response = urequests.post(HTTP_URL, data=message, headers={'Content-Type': 'application/json'})
        
    time.sleep(5)