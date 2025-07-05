from .tools import built_in_tools
from .chats import completion



class Agent:
    def __init__(self, name: str):
        self.name = name
        self.tools = []
        self.messages = []
        self.tools.extend(built_in_tools)
        
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.messages.append({"role": role, "content": content})
        
    
    def chat(self, prompt: str):
        """Send a message to the chat and get a response."""
        if prompt:
            self.add_message("user", prompt)
        response = completion(self.messages)
        self.add_message("assistant", response)
        return response