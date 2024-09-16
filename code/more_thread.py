import pygame
import pygame.midi
import music21 as m21
import threading
import time

# Initialize pygame and pygame.midi
pygame.init()
pygame.midi.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Keyboard Controlled Music")

# Set up the MIDI output
midi_out = pygame.midi.Output(0)

# Map instruments to MIDI program numbers
instrument_programs = {
    'Piano': 0,
    'Xylophone': 13,
    'Celesta': 8,
    'Violin': 40,
    'Flute': 73,
    'Aahs': 52,
    'Harmonica': 22,
    'Harp': 46,
    'Tuba': 58,
    'English Horn': 69,
    # Add more instruments as needed
}

def read_notes_from_file(file_path):
    notes = []
    with open(file_path, 'r') as file:
        for line in file:
            # 解析每一行的信息
            note_info = line.strip().split()
            note_value = int(note_info[0].split('=')[1])
            time_value = int(note_info[1].split('=')[1])
            notes.append((note_value, time_value))
    return notes

def get_current_note(notes, current_time):
    current_note = 40
    for note, time in notes:
        if time > current_time:
            break
        current_note = note
    return current_note

# Function to play a note with music21 and pygame.midi
def play_note_with_instrument(note, length, velocity, instrument):
    # note: 音高, length: 持续时间 (秒), velocity: 音量, instrument: 乐器

    # Set the MIDI instrument
    program_number = instrument_programs.get(instrument, 0)  # 或许可以直接使用 channel 名字

    midi_out.set_instrument(program_number)

    # Create the MIDI note on and off events
    midi_out.note_on(note, velocity)
    threading.Timer(length, lambda: midi_out.note_off(note, velocity)).start()

# Function to handle key press and play notes
def handle_key_press(key, notes_0, notes_1, notes_2, notes_3):
    current_time = time.time() - start_time
    current_time_ms = int(current_time * 1000)  # Convert to milliseconds
    print(f"Time: {current_time_ms} ms")
    instrument = 'Harp'
    pitch_offset = 12
    time_last = 0.8

    note_0 = get_current_note(notes_0, current_time_ms)
    note_1 = get_current_note(notes_1, current_time_ms)
    note_2 = get_current_note(notes_2, current_time_ms)
    note_3 = get_current_note(notes_3, current_time_ms)

    if key == pygame.K_z:
        threading.Thread(target=play_note_with_instrument, args=(note_0+pitch_offset, time_last, 127, instrument)).start()
    elif key == pygame.K_x:
        threading.Thread(target=play_note_with_instrument, args=(note_1+pitch_offset, time_last, 127, instrument)).start()
    elif key == pygame.K_c:
        threading.Thread(target=play_note_with_instrument, args=(note_2+pitch_offset, time_last, 127, instrument)).start()
    elif key == pygame.K_v:
        threading.Thread(target=play_note_with_instrument, args=(note_3+pitch_offset, time_last, 127, instrument)).start()

    elif key == pygame.K_q:
        threading.Thread(target=play_note_with_instrument, args=(60, 0.4, 127, 'Celesta')).start()  # C4
    elif key == pygame.K_2:
        threading.Thread(target=play_note_with_instrument, args=(61, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_w:
        threading.Thread(target=play_note_with_instrument, args=(62, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_3:
        threading.Thread(target=play_note_with_instrument, args=(63, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_e:
        threading.Thread(target=play_note_with_instrument, args=(64, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_r:
        threading.Thread(target=play_note_with_instrument, args=(65, 0.4, 127, 'Celesta')).start()  # G4
    elif key == pygame.K_5:
        threading.Thread(target=play_note_with_instrument, args=(66, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_t:
        threading.Thread(target=play_note_with_instrument, args=(67, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_6:
        threading.Thread(target=play_note_with_instrument, args=(68, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_y:
        threading.Thread(target=play_note_with_instrument, args=(69, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_7:
        threading.Thread(target=play_note_with_instrument, args=(70, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_u:
        threading.Thread(target=play_note_with_instrument, args=(71, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_i:
        threading.Thread(target=play_note_with_instrument, args=(72, 0.4, 127, 'Celesta')).start()  # C5
    elif key == pygame.K_9:
        threading.Thread(target=play_note_with_instrument, args=(73, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_o:
        threading.Thread(target=play_note_with_instrument, args=(74, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_0:
        threading.Thread(target=play_note_with_instrument, args=(75, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_p:
        threading.Thread(target=play_note_with_instrument, args=(76, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_LEFTBRACKET:
        threading.Thread(target=play_note_with_instrument, args=(77, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_EQUALS:
        threading.Thread(target=play_note_with_instrument, args=(78, 0.4, 127, 'Celesta')).start()
    elif key == pygame.K_RIGHTBRACKET:
        threading.Thread(target=play_note_with_instrument, args=(79, 0.4, 127, 'Celesta')).start()

# read txt
notes_0 = read_notes_from_file("output_0.txt")
notes_1 = read_notes_from_file("output_1.txt")
notes_2 = read_notes_from_file("output_2.txt")
notes_3 = read_notes_from_file("output_3.txt")

# Display initial message
font = pygame.font.Font(None, 36)
text = font.render('Press any key to start', True, (255, 255, 255))
screen.blit(text, (50, 130))
pygame.display.flip()

# Wait for a key press to start
waiting = True
while waiting:
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        pygame.display
        font = pygame.font.Font(None, 36)
        text = font.render('Starts!', True, (0, 255, 255))
        screen.blit(text, (50, 130))
        pygame.display.flip()
        waiting = False

# Record the start time
start_time = time.time()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_key_press(event.key, notes_0, notes_1, notes_2, notes_3)

# Quit pygame and pygame.midi
pygame.quit()
pygame.midi.quit()

