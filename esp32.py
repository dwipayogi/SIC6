from umqtt.simple import MQTTClient
import network
import time
import json
import machine
import dht
import urequests
import gc

# Konfigurasi WiFi
SSID = "OMAHKU"
PASSWORD = "20192019"

# Konfigurasi HTTP Server (Flask API)
HTTP_URL = "https://samsung.yogserver.web.id/data/post/sensor"

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
led = machine.Pin(13, machine.Pin.OUT)

# Loop utama
while True:
    try:
        # Baca sensor
        sensor.measure()
        motion = pir.value()

        led.value(motion)
            
        data_sensor = {
            "temperature": sensor.temperature(),
            "humidity": sensor.humidity(),
            "motion": motion,
        }
        message = json.dumps(data_sensor)

        # Publish ke MQTT
        print(f"Publishing to {MQTT_TOPIC}: {message}")
        client.publish(MQTT_TOPIC, message.encode())

        # Kirim ke server Flask API
        try:
            response = urequests.post(
                HTTP_URL,
                data=message,
                headers={'Content-Type': 'application/json'}
            )
            response.close()  # Penting untuk membebaskan memori
        except Exception as http_err:
            print("HTTP Error:", http_err)

        # Bersihkan memori
        gc.collect()
        time.sleep(5)

    except Exception as main_err:
        print("Main Loop Error:", main_err)
        gc.collect()
        time.sleep(5)
