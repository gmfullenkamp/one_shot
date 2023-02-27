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


def generate_random_music(num_notes, tempo, min_octave=-2, max_octave=2, min_duration=0.25, max_duration=4.0):
    # list of available note names
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # randomly select notes, octaves, and durations
    random_notes = [random.choice(notes) for i in range(num_notes)]
    random_octaves = [random.randint(min_octave, max_octave) for i in range(num_notes)]
    random_durations = [random.uniform(min_duration, max_duration) for i in range(num_notes)]

    # convert note names and octaves to MIDI note numbers
    midi_notes = [note_to_midi(note, octave) for note, octave in zip(random_notes, random_octaves)]

    # play the random melody
    play_piano(midi_notes, random_durations, tempo)


# example usage
generate_random_music(8, 120)
