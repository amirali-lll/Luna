"""
Voice input interface using OpenAI Whisper API for Speech-to-Text.
"""

import asyncio
import pyaudio
import wave
import tempfile
import os
from typing import Optional
from openai import OpenAI
from ..base import InputInterface
from .config import *


class VoiceInput(InputInterface):
    """Voice input interface using OpenAI Whisper API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required for voice input")
        
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY             
        )
        self.audio = pyaudio.PyAudio()
        self.is_recording = False
        
    async def get_input(self) -> str:
        """Record audio and convert to text using OpenAI Whisper"""
        try:
            print("🎤 Listening... (Press Ctrl+C to stop recording)")
            
            # Record audio
            audio_file_path = await self._record_audio()
            
            if not audio_file_path:
                return ""
            
            # Convert to text using OpenAI Whisper
            text = await self._transcribe_audio(audio_file_path)
            
            # Clean up temporary file
            try:
                os.unlink(audio_file_path)
            except OSError:
                pass
            
            return text.strip()
            
        except KeyboardInterrupt:
            print("\n🛑 Recording stopped by user")
            return ""
        except Exception as e:
            print(f"❌ Error in voice input: {e}")
            return ""
    
    async def _record_audio(self) -> Optional[str]:
        """Record audio from microphone"""
        stream = None
        try:
            # Create audio stream
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE
            )
            
            print("🔴 Recording...")
            frames = []
            self.is_recording = True
            
            # Record for a fixed duration or until interrupted
            # For now, we'll use a simple approach - record for 5 seconds
            duration = 5  # seconds
            total_frames = int(SAMPLE_RATE / CHUNK_SIZE * duration)
            
            for _ in range(total_frames):
                if not self.is_recording:
                    break
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                frames.append(data)
            
            print("⏹️  Recording finished")
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".wav", 
                dir=TEMP_AUDIO_DIR,
                delete=False
            )
            
            with wave.open(temp_file.name, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(b''.join(frames))
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return None
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
    
    async def _transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using OpenAI Whisper API"""
        try:
            loop = asyncio.get_event_loop()
            
            # Run the API call in a thread pool to avoid blocking
            result = await loop.run_in_executor(
                None,
                self._transcribe_sync,
                audio_file_path
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            return ""
    
    def _transcribe_sync(self, audio_file_path: str) -> str:
        """Synchronous transcription call"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=STT_MODEL,
                    file=audio_file,
                )
            return transcript.text
        except Exception as e:
            print(f"❌ Error in Whisper API call: {e}")
            return ""
    
    def stop_recording(self):
        """Stop the current recording"""
        self.is_recording = False
    
    def __del__(self):
        """Cleanup audio resources"""
        try:
            self.audio.terminate()
        except:
            pass


class SimpleVoiceInput(VoiceInput):
    """Simplified voice input with manual control"""
    
    async def get_input(self) -> str:
        """Get voice input with user control"""
        print("🎤 Press Enter to start recording, then speak...")
        input()  # Wait for user to press Enter
        
        return await super().get_input()
