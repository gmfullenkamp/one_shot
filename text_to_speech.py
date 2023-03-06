import pyttsx3

# TODO: Set up a database of text, docx, pdf, etc. files and leave this running in me ears
file_path = r"C:\Users\gmful\Downloads\CNET HW 3 Unabridged.txt"

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Get a list of available voices
voices = engine.getProperty('voices')

# Set the voice to use
engine.setProperty('voice', voices[1].id)  # Use the first voice in the list

# Open the text file for reading
with open(file_path, 'r') as file:
    # Read the entire file as text
    text = file.read()

# Set the voice rate and volume
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Convert the text to speech and speak it
engine.say(text)
engine.runAndWait()
# TODO: Have an optional listen or output argument that can save an mp3 file instead to listen to later
