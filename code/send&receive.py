from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# 设备地址字典，用于存储每个ESP32的地址
devices = {
    'ESP32_1': 'http://192.168.43.218:80/play_note',
    'ESP32_2': 'http://192.168.43.106:81/play_note'
}

def send_note_to_device(device_url, frequency, duration):
    import requests
    params = {'frequency': frequency, 'duration': duration}
    try:
        response = requests.get(device_url, params=params)
        print(f'Response from {device_url}: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Error sending to {device_url}: {str(e)}')

def schedule_music_playback():
    # Example of scheduling notes to ESP32 devices 
    while True:
        send_note_to_device(devices['ESP32_1'], 440, 500)  # A4 note, 500 ms
        send_note_to_device(devices['ESP32_2'], 523, 500)  # C5 note, 500 ms
        time.sleep(1)  # Wait for 1 second before sending next set of notes 一秒发送一次，后续再看mid文件
        print("sented!")

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    device_id = data.get('device_id')
    sensor_value = data.get('sensor_value')
    # Process the received data
    print(f"Received from {device_id}: {sensor_value}")
    # Optionally, send response back to ESP32
    return jsonify({'status': 'success', 'message': 'Data received'})

if __name__ == '__main__':
    music_thread = threading.Thread(target=schedule_music_playback)
    music_thread.start()
    app.run(host='0.0.0.0', port=5000)
