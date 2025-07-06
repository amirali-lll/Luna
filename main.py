from agent.agent import Agent
import asyncio
import sys
import readline


async def main():
    print("Welcome to your AI agent! Type 'exit' to quit.")
    agent = Agent("Luna")
    
    while True:
        user_input = input("\nYou>/ ")
        if user_input.strip().lower() == "exit":
            break
        if not user_input.strip():
            print("Please enter a valid input.")
            continue
        # Add to readline history for up/down navigation
        readline.add_history(user_input)

        print("Assistant>/ ", end="", flush=True)

        # Stream the response
        async for chunk in agent.stream_chat(user_input):
            print(chunk, end="", flush=True)
        
        print("\n")  # Add newline after streaming is complete


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