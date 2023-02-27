import pygame.midi
import random
import time


def play_piano(notes, durations, tempo):
    # initialize Pygame MIDI
    pygame.midi.init()

    # select MIDI device
    device_id = 0
    midi_out = pygame.midi.Output(device_id)
    print("Using MIDI device:", pygame.midi.get_device_info(device_id))

    # calculate delay time based on tempo
    delay = 60 / tempo

    # play melody
    for i in range(len(notes)):
        note = notes[i]
        duration = durations[i] * delay
        midi_out.note_on(note, 127)  # start playing the note
        time.sleep(duration)  # wait for the specified duration
        midi_out.note_off(note, 127)  # stop playing the note

    # close MIDI device
    del midi_out
    pygame.midi.quit()


def note_to_midi(note, octave=0):
    # dictionary mapping note names to MIDI note numbers
    note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4,
                'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9,
                'A#': 10, 'B': 11}

    # separate note name into pitch and accidental (if any)
    pitch = note[0]
    if len(note) > 1 and note[1] in ('#', 'b'):
        pitch += note[1]

    # lookup MIDI note number based on pitch and accidental
    if pitch in note_map:
        midi_note = note_map[pitch] + octave * 12 + 60
        if midi_note < 0 or midi_note > 127:
            return None
        else:
            return midi_note
    else:
        return None


def generate_random_music(num_notes, tempo, key='C', scale='major', min_octave=-1, max_octave=1,
                          min_duration=0.25, max_duration=4.0):
    # dictionary mapping scale degrees to semitone offsets
    scale_map = {'major': [0, 2, 4, 5, 7, 9, 11],
                 'natural_minor': [0, 2, 3, 5, 7, 8, 10]}

    # list of available note names
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # calculate semitone offsets for the selected scale
    root_note = note_to_midi(key)
    scale_degrees = scale_map[scale]
    semitone_offsets = [(root_note + degree) % 12 for degree in scale_degrees]

    # randomly select notes, octaves, and durations within the key and scale
    random_notes = [random.choice([note for note in notes if note_to_midi(note) % 12 in semitone_offsets]) for i in range(num_notes)]
    random_octaves = [random.randint(min_octave, max_octave) for i in range(num_notes)]
    random_durations = [random.uniform(min_duration, max_duration) for i in range(num_notes)]

    # convert note names and octaves to MIDI note numbers
    midi_notes = [note_to_midi(note, octave) for note, octave in zip(random_notes, random_octaves)]

    # play the random melody
    play_piano(midi_notes, random_durations, tempo)


def generate_scale(tempo, key='C', scale='major', octave=0):
    # dictionary mapping scale degrees to semitone offsets
    scale_map = {'major': [0, 2, 4, 5, 7, 9, 11, 12],
                 'natural_minor': [0, 2, 3, 5, 7, 8, 10, 12]}

    # list of available note names
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # calculate semitone offsets for the selected scale
    root_note = note_to_midi(key, octave=octave)
    scale_degrees = scale_map[scale]
    semitone_offsets = [(root_note + degree) % 12 for degree in scale_degrees]

    # select notes from the scale and calculate their MIDI note numbers
    scale_notes = [note for note in notes if note_to_midi(note, octave=octave) % 12 in semitone_offsets]
    midi_notes = [note_to_midi(note, octave=octave) for note in scale_notes]
    midi_notes.append(midi_notes[0] + 12)

    # create a sequence that goes up and down the scale
    sequence = list(range(len(midi_notes))) + list(range(len(midi_notes) - 2, -1, -1))

    # generate a list of note durations (in seconds) for each note in the sequence
    duration = 60 / tempo  # duration of a quarter note
    durations = [duration] * len(sequence)

    # play the scale at the specified tempo and sequence
    midi_sequence = [midi_notes[i] for i in sequence]
    duration_sequence = [durations[i] for i in sequence]
    play_piano(midi_sequence, duration_sequence, tempo)


# example usage
generate_scale(120, key='A', scale='natural_minor')

generate_random_music(10, 120, key='A', scale='natural_minor')
