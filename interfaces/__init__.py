"""
Interfaces module for different input/output methods.

This module provides a clean abstraction layer for different ways
to interact with the AI assistant (CLI, Voice, Web, etc.).
"""

from .base import InputInterface, OutputInterface
from .cli import TerminalInput, TerminalOutput, TerminalInterface

# Try to import voice interfaces (may fail if dependencies not installed)
try:
    from .voice import VoiceInput, VoiceOutput, VoiceInterface, create_voice_interface
    VOICE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Voice interfaces not available: {e}")
    VOICE_AVAILABLE = False
    VoiceInput = None
    VoiceOutput = None
    VoiceInterface = None
    create_voice_interface = None


class InterfaceManager:
    """Manager class to create and configure different interface types"""
    
    def __init__(self, input_type="cli", output_type="cli", **kwargs):
        self.input_interface = self._create_input(input_type, **kwargs)
        self.output_interface = self._create_output(output_type, **kwargs)
        self.interface_type = input_type
    
    def _create_input(self, input_type, **kwargs):
        """Create input interface based on type"""
        if input_type == "cli":
            return TerminalInput()
        elif input_type == "voice":
            if not VOICE_AVAILABLE:
                raise ValueError("Voice interface not available. Install voice dependencies.")
            return VoiceInput(kwargs.get('api_key'))
        else:
            raise ValueError(f"Unknown input type: {input_type}")
    
    def _create_output(self, output_type, **kwargs):
        """Create output interface based on type"""
        if output_type == "cli":
            return TerminalOutput()
        elif output_type == "voice":
            if not VOICE_AVAILABLE:
                raise ValueError("Voice interface not available. Install voice dependencies.")
            return VoiceOutput(
                kwargs.get('api_key'), 
                kwargs.get('voice', 'alloy')
            )
        else:
            raise ValueError(f"Unknown output type: {output_type}")
    
    async def get_input(self) -> str:
        """Get input using the configured input interface"""
        return await self.input_interface.get_input()
    
    async def send_output(self, message: str) -> None:
        """Send output using the configured output interface"""
        await self.output_interface.send_output(message)
    
    async def stream_output(self, message_stream) -> None:
        """Stream output using the configured output interface"""
        await self.output_interface.stream_output(message_stream)


def create_terminal_interface() -> TerminalInterface:
    """Convenience function to create a terminal interface"""
    return TerminalInterface()


def create_interface_manager(input_type="cli", output_type="cli", **kwargs) -> InterfaceManager:
    """Convenience function to create an interface manager"""
    return InterfaceManager(input_type, output_type, **kwargs)


# Export all available interfaces
__all__ = [
    'InputInterface',
    'OutputInterface', 
    'TerminalInput',
    'TerminalOutput',
    'TerminalInterface',
    'InterfaceManager',
    'create_terminal_interface',
    'create_interface_manager',
    'VOICE_AVAILABLE'
]

# Add voice interfaces to exports if available
if VOICE_AVAILABLE:
    __all__.extend([
        'VoiceInput',
        'VoiceOutput', 
        'VoiceInterface',
        'create_voice_interface'
    ])
