"""
Interfaces module for different input/output methods.

This module provides a clean abstraction layer for different ways
to interact with the AI assistant (CLI, Voice, Web, etc.).
"""

from .base import InputInterface, OutputInterface
from .cli import TerminalInput, TerminalOutput, TerminalInterface

class InterfaceManager:
    """Manager class to create and configure different interface types"""
    
    def __init__(self, input_type="cli", output_type="cli"):
        self.input_interface = self._create_input(input_type)
        self.output_interface = self._create_output(output_type)
        self.interface_type = input_type
    
    def _create_input(self, input_type):
        """Create input interface based on type"""
        if input_type == "cli":
            return TerminalInput()
        else:
            raise ValueError(f"Unknown input type: {input_type}")
    
    def _create_output(self, output_type):
        """Create output interface based on type"""
        if output_type == "cli":
            return TerminalOutput()
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


def create_interface_manager(input_type="cli", output_type="cli") -> InterfaceManager:
    """Convenience function to create an interface manager"""
    return InterfaceManager(input_type, output_type)


__all__ = [
    'InputInterface',
    'OutputInterface', 
    'TerminalInput',
    'TerminalOutput',
    'TerminalInterface',
    'InterfaceManager',
    'create_terminal_interface',
    'create_interface_manager'
]
