"""
Voice interface module for speech-to-text and text-to-speech functionality.

This module provides different levels of voice interaction:
1. Simple API-based voice input/output
2. Voice Activity Detection (VAD) 
3. Wake word detection ("Hey Luna")
"""

from .input import VoiceInput, SimpleVoiceInput
from .output import VoiceOutput, QuietVoiceOutput
from .config import *

class VoiceInterface:
    """Combined voice interface for both input and output"""
    
    def __init__(self, api_key: str = None, voice: str = TTS_VOICE, quiet_mode: bool = False):
        self.input = SimpleVoiceInput(api_key)
        
        if quiet_mode:
            self.output = QuietVoiceOutput(api_key, voice)
        else:
            self.output = VoiceOutput(api_key, voice)
    
    async def get_input(self) -> str:
        """Get voice input"""
        return await self.input.get_input()
    
    async def send_output(self, message: str) -> None:
        """Send voice output"""
        await self.output.send_output(message)
    
    async def stream_output(self, message_stream) -> None:
        """Stream voice output"""
        await self.output.stream_output(message_stream)
    
    async def send_welcome_message(self) -> None:
        """Send welcome message"""
        welcome_msg = "Hello! I'm Luna, your AI voice assistant. I'm ready to help you!"
        await self.send_output(welcome_msg)
    
    async def send_goodbye_message(self) -> None:
        """Send goodbye message"""
        goodbye_msg = "Goodbye! Have a wonderful day!"
        await self.send_output(goodbye_msg)


def create_voice_interface(api_key: str = None, voice: str = TTS_VOICE, quiet_mode: bool = False) -> VoiceInterface:
    """Convenience function to create a voice interface"""
    return VoiceInterface(api_key, voice, quiet_mode)


__all__ = [
    'VoiceInput',
    'SimpleVoiceInput', 
    'VoiceOutput',
    'QuietVoiceOutput',
    'VoiceInterface',
    'create_voice_interface',
    'SAMPLE_RATE',
    'CHUNK_SIZE',
    'WAKE_WORD',
    'TTS_VOICE'
]
