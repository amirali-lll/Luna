import asyncio
import sys
import readline
from typing import AsyncGenerator
from ..base import InputInterface, OutputInterface


class TerminalInput(InputInterface):
    """Terminal-based input interface using standard input"""
    
    def __init__(self):
        # Configure readline for better terminal experience
        self._setup_readline()
    
    def _setup_readline(self):
        """Setup readline for command history and editing"""
        try:
            # Enable tab completion and history
            readline.parse_and_bind('tab: complete')
            readline.parse_and_bind('set editing-mode emacs')
            
            # Set up history file (optional)
            import os
            history_file = os.path.expanduser("~/.luna_history")
            try:
                readline.read_history_file(history_file)
                # Limit history size
                readline.set_history_length(1000)
            except FileNotFoundError:
                pass
            
            # Save history on exit
            import atexit
            atexit.register(readline.write_history_file, history_file)
            
        except ImportError:
            # readline not available on some systems
            pass
    
    async def get_input(self) -> str:
        """Get input from terminal with async support"""
        loop = asyncio.get_event_loop()
        
        try:
            # Run input() in thread pool to avoid blocking
            user_input = await loop.run_in_executor(
                None, self._get_user_input
            )
            
            # Add to readline history for up/down navigation
            if user_input.strip():
                try:
                    readline.add_history(user_input)
                except NameError:
                    pass  # readline not available
            
            return user_input.strip()
            
        except (EOFError, KeyboardInterrupt):
            return "exit"
    
    def _get_user_input(self) -> str:
        """Blocking input operation"""
        try:
            return input("\nYou>/ ")
        except (EOFError, KeyboardInterrupt):
            return "exit"


class TerminalOutput(OutputInterface):
    """Terminal-based output interface using standard output"""
    
    def __init__(self, prefix: str = "Assistant>/ "):
        self.prefix = prefix
        self._first_chunk = True
    
    async def send_output(self, message: str) -> None:
        """Send complete message to terminal"""
        print(f"{self.prefix}{message}")
    
    async def stream_output(self, message_stream: AsyncGenerator[str, None]) -> None:
        """Stream output to terminal as it arrives"""
        self._first_chunk = True
        
        try:
            async for chunk in message_stream:
                if self._first_chunk:
                    # Print prefix only for the first chunk
                    print(self.prefix, end="", flush=True)
                    self._first_chunk = False
                
                # Print chunk without newline, flush immediately
                print(chunk, end="", flush=True)
            
            # Add final newline after streaming is complete
            print("\n")
            
        except Exception as e:
            print(f"\nError during streaming: {e}")
    
    async def send_error(self, error_message: str) -> None:
        """Send error message to terminal with special formatting"""
        print(f"\n❌ Error: {error_message}")
    
    async def send_info(self, info_message: str) -> None:
        """Send info message to terminal with special formatting"""
        print(f"ℹ️  {info_message}")
    
    async def send_success(self, success_message: str) -> None:
        """Send success message to terminal with special formatting"""
        print(f"✅ {success_message}")


class TerminalInterface:
    """Combined terminal interface for both input and output"""
    
    def __init__(self, input_prefix: str = "\nYou>/ ", output_prefix: str = "Assistant>/ "):
        self.input = TerminalInput()
        self.output = TerminalOutput(output_prefix)
        self.input_prefix = input_prefix
    
    async def get_input(self) -> str:
        """Get input from terminal"""
        return await self.input.get_input()
    
    async def send_output(self, message: str) -> None:
        """Send output to terminal"""
        await self.output.send_output(message)
    
    async def stream_output(self, message_stream: AsyncGenerator[str, None]) -> None:
        """Stream output to terminal"""
        await self.output.stream_output(message_stream)
    
    async def send_welcome_message(self) -> None:
        """Send welcome message when starting"""
        await self.output.send_info("Welcome to Luna! Your AI assistant!")
        await self.output.send_info("Type your message or 'exit' to quit.")
    
    async def send_goodbye_message(self) -> None:
        """Send goodbye message when exiting"""
        await self.output.send_success("Goodbye! Have a great day!")
    
    def clear_screen(self) -> None:
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
