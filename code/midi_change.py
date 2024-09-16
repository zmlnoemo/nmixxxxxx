import mido

# MIDI 文件路径
midi_file_path = "D:\sources\DDDDDDDDDDIIIIIIIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPP\me1.mid"
# 结果文件路径
result_file_path = "D:\sources\DDDDDDDDDDIIIIIIIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPP\mid_result.txt"

# MIDI 文件加载
mid = mido.MidiFile(midi_file_path)

# 用于存放 0 ~ 127 音高 对应的 音符频率
note_frequency = [0] * 128

# 这里选取 69 音高的频率 440Hz , 这是个整数 , 方便计算
standard_frequency = 440.0

# 计算每个音符的频率
for i in range(128):
    note_frequency[i] = round((standard_frequency / 32.0) * (2 ** ((i - 9.0) / 12.0)))

# 将结果写入文件
with open(result_file_path, "w") as file:
    for i, track in enumerate(mid.tracks):
        file.write('Track {}: {}\n'.format(i, track.name))
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)
            file.write(str(msg))
            if msg.type == 'note_on' or msg.type == 'note_off':
                note = msg.note
                frequency = note_frequency[note]
                file.write(f' fre = {frequency}')
            file.write('\n')

print("频率转换完成并写入文件。")

# import mido

# mid = mido.MidiFile("D:\sources\DDDDDDDDDDIIIIIIIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPP\me1.mid")

# with open("D:\sources\DDDDDDDDDDIIIIIIIIIIIIIIIIIIIIIIIPPPPPPPPPPPPPP\mid_result.txt", "w") as file:
#     for i, track in enumerate(mid.tracks):#enumerate()：创建索引序列，索引初始为0
#         file.write('Track {}: {}\n'.format(i, track.name))
#         print('Track {}: {}'.format(i, track.name))
#         for msg in track:#每个音轨的消息遍历
#             print(msg)
#             file.write(str(msg) + '\n')