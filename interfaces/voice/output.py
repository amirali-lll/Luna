"""
Voice output interface using OpenAI TTS API for Text-to-Speech.
"""

import asyncio
import tempfile
import os
import sys
import subprocess
from typing import AsyncGenerator
from openai import OpenAI
from ..base import OutputInterface
from .config import *


class VoiceOutput(OutputInterface):
    """Voice output interface using OpenAI TTS API"""
    
    def __init__(self, api_key: str = None, voice: str = TTS_VOICE):
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required for voice output")
        
        self.client = OpenAI(api_key=self.api_key)
        self.voice = voice
        self._first_chunk = True
    
    async def send_output(self, message: str) -> None:
        """Convert text to speech and play it"""
        if not message.strip():
            return
        
        try:
            print(f"🔊 Speaking: {message}")
            
            # Generate speech using OpenAI TTS
            audio_file_path = await self._generate_speech(message)
            
            if audio_file_path:
                # Play the audio
                await self._play_audio(audio_file_path)
                
                # Clean up temporary file
                try:
                    os.unlink(audio_file_path)
                except OSError:
                    pass
            
        except Exception as e:
            print(f"❌ Error in voice output: {e}")
            # Fallback to text output
            print(f"Assistant: {message}")
    
    async def stream_output(self, message_stream: AsyncGenerator[str, None]) -> None:
        """Stream text and convert to speech"""
        accumulated_text = ""
        sentence_endings = ('.', '!', '?', '\n')
        
        self._first_chunk = True
        
        try:
            async for chunk in message_stream:
                if self._first_chunk:
                    print("Assistant: ", end="", flush=True)
                    self._first_chunk = False
                
                accumulated_text += chunk
                print(chunk, end="", flush=True)
                
                # Check if we have a complete sentence
                if any(chunk.endswith(ending) for ending in sentence_endings):
                    sentence = accumulated_text.strip()
                    if sentence:
                        # Speak the complete sentence
                        await self.send_output(sentence)
                    accumulated_text = ""
            
            # Speak any remaining text
            if accumulated_text.strip():
                await self.send_output(accumulated_text.strip())
            
            print("\n")  # Add final newline
            
        except Exception as e:
            print(f"\n❌ Error during streaming: {e}")
    
    async def _generate_speech(self, text: str) -> str:
        """Generate speech using OpenAI TTS API"""
        try:
            loop = asyncio.get_event_loop()
            
            # Run the API call in a thread pool
            audio_file_path = await loop.run_in_executor(
                None,
                self._generate_speech_sync,
                text
            )
            
            return audio_file_path
            
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            return None
    
    def _generate_speech_sync(self, text: str) -> str:
        """Synchronous speech generation"""
        try:
            # Create temporary file for audio
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".mp3",
                dir=TEMP_AUDIO_DIR,
                delete=False
            )
            
            # Generate speech
            response = self.client.audio.speech.create(
                model=TTS_MODEL,
                voice=self.voice,
                input=text,
                response_format="mp3"
            )
            
            # Write audio data to file
            with open(temp_file.name, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Error in TTS API call: {e}")
            return None
    
    async def _play_audio(self, audio_file_path: str) -> None:
        """Play audio file using system audio player"""
        try:
            loop = asyncio.get_event_loop()
            
            # Use appropriate audio player for macOS
            if sys.platform == "darwin":  # macOS
                cmd = ["afplay", audio_file_path]
            elif sys.platform.startswith("win"):  # Windows
                cmd = ["start", "", audio_file_path]  # Windows
            else:
                # Fallback for Linux and other systems
                cmd = ["play", audio_file_path]  # Requires sox
            
            # Run audio player asynchronously
            await loop.run_in_executor(
                None,
                self._run_audio_command,
                cmd
            )
            
        except Exception as e:
            print(f"❌ Error playing audio: {e}")
    
    def _run_audio_command(self, cmd):
        """Run audio command synchronously"""
        try:
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
        except Exception as e:
            print(f"❌ Error running audio command: {e}")
    
    async def send_listening_sound(self) -> None:
        """Play a sound to indicate the assistant is listening"""
        # For now, just print an indicator
        print("🎧 Listening...")
    
    async def send_thinking_sound(self) -> None:
        """Play a sound to indicate the assistant is thinking"""
        print("🤔 Thinking...")


class QuietVoiceOutput(VoiceOutput):
    """Voice output that doesn't print text to console"""
    
    async def send_output(self, message: str) -> None:
        """Convert text to speech without printing"""
        if not message.strip():
            return
        
        try:
            # Generate and play speech without printing the message
            audio_file_path = await self._generate_speech(message)
            
            if audio_file_path:
                await self._play_audio(audio_file_path)
                try:
                    os.unlink(audio_file_path)
                except OSError:
                    pass
            
        except Exception as e:
            print(f"❌ Error in voice output: {e}")
    
    async def stream_output(self, message_stream: AsyncGenerator[str, None]) -> None:
        """Stream and speak without printing text"""
        accumulated_text = ""
        sentence_endings = ('.', '!', '?', '\n')
        
        try:
            async for chunk in message_stream:
                accumulated_text += chunk
                
                # Speak complete sentences
                if any(chunk.endswith(ending) for ending in sentence_endings):
                    sentence = accumulated_text.strip()
                    if sentence:
                        await self.send_output(sentence)
                    accumulated_text = ""
            
            # Speak any remaining text
            if accumulated_text.strip():
                await self.send_output(accumulated_text.strip())
            
        except Exception as e:
            print(f"❌ Error during streaming: {e}")
