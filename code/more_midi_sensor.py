from flask import Flask, request, jsonify
import pygame
import pygame.midi
import threading

app = Flask(__name__)

# 初始化 pygame 和 pygame.midi
pygame.init()
pygame.midi.init()

# 设置显示窗口
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Keyboard Controlled Music")

# 设置 MIDI 输出
midi_out = pygame.midi.Output(0)

# 乐器与 MIDI 程序号映射
instrument_programs = {
    'Piano': 0,
    'Violin': 40,
    'Flute': 73,
    # 可以根据需要添加更多乐器
}

# 使用 music21 和 pygame.midi 播放音符的函数
def play_note_with_instrument(note, length, velocity, instrument):
    # 设置 MIDI 乐器
    program_number = instrument_programs.get(instrument, 0)
    midi_out.set_instrument(program_number)

    # 确保 velocity 是整数
    velocity = int(velocity)

    # 创建 MIDI 音符开和关的事件
    midi_out.note_on(note, velocity)
    threading.Timer(length, lambda: midi_out.note_off(note, velocity)).start()

# 接收数据的路由
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    device_id = data.get('device_id')

    # 处理接收到的数据并播放相应的音符
    if device_id == 'ESP32_1':  # 第一个传感器
        sensor_1 = data.get('sensor_value')
        # 将传感器的值从0-4095映射到0-127，并转换为整数
        velocity_1 = int(sensor_1) // 32
        threading.Thread(target=play_note_with_instrument, args=(60, 2, velocity_1, 'Piano')).start()  # C4

    elif device_id == 'ESP32_2':  # 第二个传感器
        sensor_2 = data.get('sensor_value')
        # 将传感器的值从0-4095映射到0-127，并转换为整数
        velocity_2 = int(sensor_2) // 32
        threading.Thread(target=play_note_with_instrument, args=(64, 2, velocity_2, 'Violin')).start()  # E4

    sensor_value = data.get('sensor_value')
    print(f"Received from {device_id}: {sensor_value}")

    # 返回响应
    return jsonify({'status': 'success', 'message': 'Data received'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# 退出 pygame 和 pygame.midi
pygame.quit()
pygame.midi.quit()
