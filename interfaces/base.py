from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional

class InputInterface(ABC):
    @abstractmethod
    async def get_input(self) -> str:
        """Get input from the interface"""
        pass

class OutputInterface(ABC):
    @abstractmethod
    async def send_output(self, message: str) -> None:
        """Send output to the interface"""
        pass
    
    @abstractmethod
    async def stream_output(self, message_stream: AsyncGenerator[str, None]) -> None:
        """Stream output to the interface"""
        pass