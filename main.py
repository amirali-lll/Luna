from agent.agent import Agent


def main():
    print("Welcome to your AI agent! Type 'exit' to quit.")
    agent = Agent("Luna")
    while True:
        user_input = input("You>/ ")
        if user_input.strip().lower() == "exit":
            break
        if not user_input.strip():
            print("Please enter a valid input.")
            continue
        print("Assistant>/", agent.chat(user_input))
        print("Conversation History:", agent.messages)

if __name__ == "__main__":
    main()