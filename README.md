# Voice-Powered First Aid Bot

A simple, local-first voice assistant that listens for common first-aid scenarios and reads out step-by-step guidance. It uses your microphone for speech input, spaCy for lightweight NLP, and text-to-speech for audible responses. The knowledge base is a JSON file you can edit and extend.

## Features
- Voice input using your default microphone
- Keyword and synonym matching powered by spaCy tokenization/lemmatization
- Step-by-step, voice-guided instructions with interactive "next" and "stop"
- Safety warnings for critical injuries (e.g., choking)
- Easy-to-edit JSON knowledge base with `synonyms`, `summary`, `instructions`

## Disclaimer
This tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. For emergencies or life‑threatening situations, call your local emergency number immediately.

## Project Structure
- `first_aid_bot.py` — Main application logic (listening, NLP, TTS, and flow)
- `first_aid_data.json` — Knowledge base of injuries and instructions
- `README.md` — This guide

## Prerequisites
- Python 3.9+ (Windows recommended for the setup steps below)
- A working microphone
- Internet access (for Google Speech Recognition and gTTS by default)

## Installation (Windows)
1) Create a virtual environment (optional but recommended)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies
```powershell
pip install SpeechRecognition spacy gTTS playsound==1.2.2
```

3) Microphone backend (PyAudio)
PyAudio wheels can be finicky on Windows. Easiest route:
```powershell
pip install pipwin
pipwin install pyaudio
```

4) Install spaCy model
```powershell
python -m spacy download en_core_web_sm
```

## Running the Bot
```powershell
python first_aid_bot.py
```
You’ll hear a disclaimer first, then the bot will listen for your command. Try:
- "What to do for a burn?"
- "I have a nosebleed"
- "Someone is choking"
- "I got a bee sting"

During instructions, say "next" to continue to the next step or "stop" to end.

## Knowledge Base (JSON) Schema
Each injury entry in `first_aid_data.json` looks like this:
```json
{
  "injuries": {
    "burn": {
      "synonyms": ["burnt", "scald"],
      "category": "Heat/Chemical",
      "summary": "Immediate cooling of the affected area to minimize tissue damage.",
      "critical": false,
      "instructions": [
        "First, ...",
        "Next, ..."
      ]
    }
  }
}
```
- `synonyms`: Extra terms that should also map to this injury. Include plural/singular, layman terms, and common phrases (e.g., "bee sting").
- `category`: Logical grouping (e.g., Bleeding, Breathing, Bites & Stings).
- `summary`: One-line overview for maintainers.
- `critical`: If `true`, the bot will speak an emergency warning first.
- `instructions`: Ordered list of steps. Keep them concise, actionable, and safe.

### Adding a new injury
1) Open `first_aid_data.json` and add a new object under `injuries`.
2) Provide a clear `synonyms` list, a short `summary`, a `critical` flag, and `instructions`.
3) Save the file and re-run the bot. No code changes required.

## How command matching works
- The user’s speech is transcribed to text.
- The text is tokenized and lemmatized with spaCy.
- The bot checks for matches against each injury’s main keyword and `synonyms`.
  - For single-word terms, it compares against token lemmas.
  - For multi-word phrases (e.g., "bee sting", "can’t breathe"), ensure your code checks phrases against the full text string.

## Troubleshooting
- No microphone detected
  - Ensure your default recording device is enabled in Windows Sound settings.
  - Test with `python -m speech_recognition` for diagnostics.

- Speech recognition fails (RequestError)
  - Requires internet for Google’s API. Check your connection or try again later.

- Text-to-speech errors on Windows (Error 263 with MP3 playback)
  - Caused by the Windows MCI subsystem when playing MP3s with `playsound` and a reused filename.
  - Mitigations:
    - Use a unique temp filename every time and delete after playback.
    - Ensure a valid default audio output device is selected and not disabled.
    - Consider swapping to `pyttsx3` (offline) to avoid MP3 playback entirely.

- spaCy model not found
  - Re-run: `python -m spacy download en_core_web_sm`

## Security & Privacy
- Audio is sent to Google for speech recognition by default. Do not use this for sensitive or private information. For a fully offline stack, consider Vosk (ASR) and pyttsx3 (TTS).

## Roadmap Ideas
- Offline ASR/TTS options
- Richer NLP for multi-word/phrase detection and intent parsing
- Confidence prompts ("Did you mean…?")
- More injuries and localized content

## License
MIT (add a LICENSE file if you plan to open source).
