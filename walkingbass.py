import music21 as m21

# Create the 12-bar blues in F with walking bass and chords
score = m21.stream.Score()

# Define the chords and walking bass notes
chords = [
    ('F7', 'F3 A3 C4 E-4'),
    ('F7', 'F3 G3 A3 B-3'),
    ('F7', 'F3 A3 C4 E-4'),
    ('F7', 'F3 G3 A3 B-3'),
    ('B-7', 'B-2 D3 F3 A-3'),
    ('B-7', 'B-2 C3 D3 E-3'),
    ('F7', 'F3 A3 C4 E-4'),
    ('F7', 'F3 G3 A3 B-3'),
    ('C7', 'C3 E3 G3 B-3'),
    ('B-7', 'B-2 D3 F3 A-3'),
    ('F7', 'F3 A3 C4 E-4'),
    ('F7', 'F3 G3 A3 B-3')
]

# Create parts for the right and left hands
right_hand = m21.stream.Part()
right_hand.id = 'Right Hand'
left_hand = m21.stream.Part()
left_hand.id = 'Left Hand'

# Add the chords and walking bass to the parts
for chord_name, bass_notes in chords:
    chord = m21.harmony.ChordSymbol(chord_name)
    bass = m21.chord.Chord(bass_notes.split())
    
    right_hand.append(chord)
    left_hand.append(bass)

# Add the parts to the score
score.append(right_hand)
score.append(left_hand)

# Display the score
score.show('musicxml.png')
