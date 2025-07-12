"""
Voice interface configuration and constants.
"""

import os
from typing import Optional

# Audio configuration
SAMPLE_RATE = 16000  # 16kHz sample rate for better speech recognition
CHUNK_SIZE = 1024   # Audio chunk size for processing
CHANNELS = 1        # Mono audio
AUDIO_FORMAT = "int16"  # 16-bit integer format

# Voice Activity Detection (VAD) settings
VAD_MODE = 3        # WebRTC VAD aggressiveness (0-3, 3 = most aggressive)
SILENCE_DURATION = 2.0  # Seconds of silence before stopping recording
MIN_SPEECH_DURATION = 0.5  # Minimum seconds of speech to process

# Wake word settings
WAKE_WORD = "hey luna"
WAKE_WORD_SENSITIVITY = 0.5  # Porcupine wake word sensitivity (0.0-1.0)

# API Keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Voice model settings
STT_MODEL = "whisper-large-v3-turbo"  # Groq Whisper model
TTS_MODEL = "gpt-4o-mini-tts"      # OpenAI TTS model
TTS_VOICE = "nova"      # OpenAI TTS voice (alloy, echo, fable, onyx, nova, shimmer)
TTS_INSTRUCTIONS = " Use a friendly and engaging tone.Speak casually and naturally."

# Audio file settings
TEMP_AUDIO_DIR = "/tmp/luna_audio"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
