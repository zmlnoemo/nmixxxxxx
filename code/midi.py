import music21 as m21
from music21.instrument import MIDI_PROGRAM_TO_INSTRUMENT

def play_note(pitch="C4", length=2, velocity=127, instrument='Piano'):
    note_1 = m21.note.Note(pitch, quarterLength=length)
    note_1.volume.velocity = velocity
    stream_1 = m21.stream.Stream()
    
    # Add the specified instrument to the stream
    instrument_dict = {
        'Piano': m21.instrument.Piano(),
        'Violin': m21.instrument.Violin(),
        'Flute': m21.instrument.Flute(),
        # Add more instruments as needed
        #TODOoo

    }
    
    if instrument in instrument_dict:
        stream_1.append(instrument_dict[instrument])
    else:
        print(f"Instrument '{instrument}' not recognized. Defaulting to Piano.")
        stream_1.append(m21.instrument.Piano())
        
    stream_1.append(note_1)
    s_player = m21.midi.realtime.StreamPlayer(stream_1)
    s_player.play()
    s_player.stop()  # Ensure the player stops properly after playing

# Example usage
play_note()
