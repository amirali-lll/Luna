from agent.chats import chat


def main():
    print("Welcome to your AI agent! Type 'exit' to quit.")
    messages = []
    while True:
        user_input = input("You>/ ")
        if user_input.strip().lower() == "exit":
            break
        if not user_input.strip():
            print("Please enter a valid input.")
            continue
        response = chat(user_input, messages)
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": response})
        print("Assistant>/", response)

if __name__ == "__main__":
    main()