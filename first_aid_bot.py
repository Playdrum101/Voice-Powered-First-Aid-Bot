import json
import os
import speech_recognition as sr
import spacy
from gtts import gTTS
import playsound

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def load_first_aid_data(filename="first_aid_data.json"):
    """Loads the first-aid instructions from the JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def speak(text):
    """Converts text to speech and plays it."""
    try:
        tts = gTTS(text=text, lang='en')
        filename = "response.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Error in TTS: {e}")
        print(text)

def listen_to_user():
    """Captures audio from the microphone and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.pause_threshold = 2
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return None
    except UnboundLocalError:
        # This can happen if listen() fails before audio is assigned
        print("Could not capture audio. Please try again.")
        return None

def process_command(text, data):
    """
    Processes the command by checking for injury keywords and their synonyms.
    """
    doc = nlp(text.lower())
    
    # Iterate through each injury defined in our JSON data
    for injury_keyword, injury_data in data["injuries"].items():
        # Create a list of all possible terms for this injury
        all_terms = [injury_keyword] + injury_data.get("synonyms", [])
        
        # Check if any word from the user's speech matches any term
        for token in doc:
            if token.lemma_ in all_terms:
                return injury_keyword # Return the main keyword (e.g., "sprain")
    return None

def give_instructions(injury, data):
    """Provides step-by-step instructions, with a special warning for critical injuries."""
    injury_entry = data["injuries"].get(injury)
    if not injury_entry:
        speak(f"Sorry, I don't have instructions for {injury}.")
        return

    # --- NEW: Critical Injury Check ---
    if injury_entry.get("critical", False):
        critical_warning = f"Warning: {injury} can be a life-threatening emergency. My first step is to advise you to call emergency services immediately. I will provide interim steps, but this is not a substitute for professional help."
        print(critical_warning)
        speak(critical_warning)
    
    instructions = injury_entry.get("instructions", [])
    if not instructions:
        speak(f"I couldn't find detailed steps for {injury}.")
        return

    intro_message = f"Okay, here are the first-aid steps for a {injury}."
    print(f"\n--- First-Aid for: {injury.capitalize()} ---")
    print(intro_message)
    speak(intro_message)
    
    for i, step in enumerate(instructions):
        step_message = f"Step {i + 1}: {step}"
        print(step_message)
        speak(step_message)
        
        if i < len(instructions) - 1:
            prompt_message = "Say 'next' to continue, or 'stop' to end."
            speak(prompt_message)
            while True:
                response = listen_to_user()
                if response:
                    if "next" in response:
                        break
                    elif "stop" in response:
                        stop_message = "Stopping instructions. How else can I help?"
                        print(f"\n{stop_message}")
                        speak(stop_message)
                        return
                        
    final_message = f"Those are all the steps for a {injury}. Please remember to seek professional medical help if needed."
    print("--- End of Instructions ---")
    print(final_message)
    speak(final_message)

# --- The Main Application Loop ---
if __name__ == "__main__":
    # Load the data once at the start
    first_aid_data = load_first_aid_data()

    # --- Crucial Safety Disclaimer ---
    disclaimer = """
    Welcome to the First-Aid Assistant. 
    Before we begin, please remember, I am a First Aid assistant and not a medical professional.
    For any serious or life-threatening situation, you must call your local emergency services immediately.
    This tool is for informational purposes for minor injuries only.
    """
    print(disclaimer)
    speak(disclaimer)

    while True:
        # Listen for the main command
        command = listen_to_user()

        if command:
            if any(word in command for word in ["goodbye", "exit", "quit"]):
                speak("Goodbye! Stay safe.")
                break

            # --- UPDATED: Process command using the full data dictionary ---
            injury = process_command(command, first_aid_data)

            if injury:
                give_instructions(injury, first_aid_data)
            else:
                # Basic fallback if no injury is detected
                speak("I'm sorry, I can only provide first-aid advice. Please tell me the injury, for example, What to do for a burn?")