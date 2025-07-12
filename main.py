from agent.agent import Agent
from interfaces import create_terminal_interface
import asyncio
import sys


async def main():
    terminal = create_terminal_interface()
    await terminal.send_welcome_message()
    
    agent = Agent("Luna")
    
    while True:
        user_input = await terminal.get_input()
        
        if user_input.lower() == "exit":
            await terminal.send_goodbye_message()
            break
        
        if not user_input:
            await terminal.output.send_info("Please enter a valid input.")
            continue
        
        response_stream = agent.stream_chat(user_input)
        await terminal.stream_output(response_stream)


def sync_main():
    """Synchronous wrapper for the async main function."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    sync_main()