import music21 as m21

def play_note(pitch, length, velocity):
    note_1 = m21.note.Note(pitch, quarterLength=length)
    note_1.volume.velocity = velocity

    note_2 = m21.note.Note(pitch, quarterLength=length)
    note_2.volume.velocity = velocity

    # Create streams for both instruments
    piano_stream = m21.stream.Stream()
    violin_stream = m21.stream.Stream()
    
    # Add Piano and Violin instruments to their respective streams
    piano_stream.append(m21.instrument.Piano())
    violin_stream.append(m21.instrument.Violin())
    
    # Append notes to their respective streams
    piano_stream.append(note_1)
    violin_stream.append(note_2)
    
    # Create a single stream by merging the two streams
    merged_stream = m21.stream.Stream()
    merged_stream.insert(0, piano_stream)
    merged_stream.insert(0, violin_stream)
    
    # Create a player for the merged stream and play it
    player = m21.midi.realtime.StreamPlayer(merged_stream)
    player.play()
    player.stop()  # Ensure the player stops properly after playing

# Example usage:
play_note(pitch="C4", length=2, velocity=127)
