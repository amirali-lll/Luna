from .tools import built_in_tools, get_tool_functions
from .chats import completion
import json


class Agent:
    def __init__(self, name: str):
        self.name = name
        self.tools = []
        self.messages = []
        self.tools.extend(built_in_tools)
        self.tool_functions = get_tool_functions()
        
    def add_message(self, role: str, content: str, tool_calls=None):
        """Add a message to the conversation history."""
        message = {"role": role, "content": content}
        if tool_calls:
            message["tool_calls"] = tool_calls
        self.messages.append(message)
        
    def execute_tool_call(self, tool_call):
        """Execute a tool call and return the result."""
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name in self.tool_functions:
            try:
                result = self.tool_functions[function_name](**function_args)
                return json.dumps(result)
            except Exception as e:
                return f"Error executing {function_name}: {str(e)}"
        else:
            return f"Unknown function: {function_name}"
    
    def chat(self, prompt: str):
        """Send a message to the chat and get a response."""
        if prompt:
            self.add_message("user", prompt)
        
        # Get response from OpenAI with tools
        response = completion(self.messages, self.tools)
        
        # Check if the response contains tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            # Add the assistant's message with tool calls
            self.add_message("assistant", response.content, response.tool_calls)
            
            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_result = self.execute_tool_call(tool_call)
                
                # Add the tool result to the conversation
                self.messages.append({
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tool_call.id
                })
            
            # Get the final response after tool execution
            final_response = completion(self.messages, self.tools)
            self.add_message("assistant", final_response.content)
            return final_response.content
        else:
            # No tool calls, just add the response
            self.add_message("assistant", response.content)
            return response.content