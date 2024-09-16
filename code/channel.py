from flask import Flask, request, jsonify
import pygame
import pygame.midi
import threading

# 初始化 pygame 和 pygame.midi
pygame.init()
pygame.midi.init()

# 设置显示窗口
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Keyboard Controlled Music")

# 列出所有可用的 MIDI 输出设备
print(pygame.midi.get_count())
print("Available MIDI Output devices:")
for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    print(f"Device {i}: interface - {info[0]}, name - {info[1]}, is_input - {info[2]}, is_output - {info[3]}")

# 尝试打开 MIDI 输出设备
try:
    midi_out = pygame.midi.Output(0)
    print("MIDI Output opened successfully.")
except Exception as e:
    print(f"Failed to open MIDI Output: {e}")
    midi_out = None