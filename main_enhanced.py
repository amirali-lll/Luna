"""
Enhanced main application with support for CLI and Voice interfaces.
"""

from agent.agent import Agent
from interfaces import create_terminal_interface, create_voice_interface, VOICE_AVAILABLE
import asyncio
import sys
import argparse


async def run_cli_mode():
    """Run the application in CLI mode"""
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


async def run_voice_mode():
    """Run the application in voice mode"""
    if not VOICE_AVAILABLE:
        print("❌ Voice mode not available. Please install voice dependencies:")
        print("   pip install pyaudio openai")
        return
    
    try:
        voice = create_voice_interface()
        await voice.send_welcome_message()
        
        agent = Agent("Luna")
        
        print("\n🎤 Voice mode activated!")
        print("📝 Instructions:")
        print("   - Press Enter to start recording")
        print("   - Speak your message")
        print("   - Say 'exit' to quit")
        print("   - Use Ctrl+C to stop recording early")
        
        while True:
            user_input = await voice.get_input()
            
            if user_input.lower() in ["exit", "goodbye", "quit"]:
                await voice.send_goodbye_message()
                break
            
            if not user_input:
                print("🔇 No speech detected. Try again.")
                continue
            
            print(f"💭 You said: {user_input}")
            
            # Send thinking sound and get response
            await voice.output.send_thinking_sound()
            response_stream = agent.stream_chat(user_input)
            answer = ''
            async for chunk in response_stream:
                answer += chunk
            await voice.output.send_output(answer)
            
            print(f"🤖 Luna said: {answer}")
    
    except KeyboardInterrupt:
        print("\n👋 Voice mode stopped by user")
    except Exception as e:
        print(f"❌ Error in voice mode: {e}")
        print("🔄 Falling back to CLI mode...")
        await run_cli_mode()


async def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Luna AI Voice Assistant")
    parser.add_argument(
        "--mode", 
        choices=["cli", "voice"], 
        default="cli",
        help="Interface mode (default: cli)"
    )
    parser.add_argument(
        "--voice",
        choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        default="alloy",
        help="TTS voice selection (default: alloy)"
    )
    
    args = parser.parse_args()
    
    print("🌙 Luna AI Assistant")
    print("=" * 50)
    
    if args.mode == "voice":
        await run_voice_mode()
    else:
        await run_cli_mode()


def sync_main():
    """Synchronous wrapper for the async main function."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    sync_main()
