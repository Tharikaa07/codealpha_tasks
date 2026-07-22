import random
import datetime

# Store conversation memory
memory = {"name": None}

GREETING_RESPONSES = [
    "Hi there!", "Hello!", "Hey! Good to see you.", "Hiya!"
]

MOOD_RESPONSES_POSITIVE = [
    "That's great to hear!", "Awesome, glad you're doing well!", "Nice! Keep that energy up."
]

MOOD_RESPONSES_NEGATIVE = [
    "Sorry to hear that. I hope things get better soon.",
    "That sounds tough. Take it one step at a time.",
    "I'm here if you want to talk about it."
]

UNKNOWN_RESPONSES = [
    "Hmm, I'm not sure I understand. Could you rephrase?",
    "Sorry, I didn't quite get that.",
    "Can you say that a different way?"
]

def get_time_based_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif hour < 17:
        return "Good afternoon!"
    else:
        return "Good evening!"

def get_response(user_input):
    text = user_input.lower().strip()

    if "my name is" in text:
        name = text.split("my name is")[-1].strip().title()
        memory["name"] = name
        return f"Nice to meet you, {name}! I'll remember that."

    if "what is my name" in text or "what's my name" in text:
        if memory["name"]:
            return f"Your name is {memory['name']}, right?"
        return "I don't think you've told me your name yet!"

    if "hello" in text or "hi" in text or "hey" in text:
        return random.choice(GREETING_RESPONSES) + " " + get_time_based_greeting()

    if "how are you" in text:
        return "I'm just a program, but I'm running smoothly! How about you?"

    if any(word in text for word in ["good", "great", "happy", "awesome", "fine"]):
        return random.choice(MOOD_RESPONSES_POSITIVE)

    if any(word in text for word in ["sad", "bad", "tired", "upset", "not good"]):
        return random.choice(MOOD_RESPONSES_NEGATIVE)

    if "your name" in text:
        return "I'm CodeAlpha Bot, your friendly assistant."

    if "joke" in text:
        return "Why do programmers prefer dark mode? Because light attracts bugs!"

    if "help" in text:
        return "You can tell me your name, ask how I am, share how you're feeling, or ask for a joke!"

    if "bye" in text or "exit" in text or "quit" in text:
        name = memory["name"] if memory["name"] else "friend"
        return f"Goodbye, {name}! Have a wonderful day."

    return random.choice(UNKNOWN_RESPONSES)

def chat():
    print("Chatbot: " + get_time_based_greeting() + " I'm CodeAlpha Bot. Type 'bye' to exit.\n")

    while True:
        user_input = input("You: ")

        if not user_input.strip():
            print("Chatbot: Please type something.\n")
            continue

        response = get_response(user_input)
        print(f"Chatbot: {response}\n")

        if any(word in user_input.lower() for word in ["bye", "exit", "quit"]):
            break

if __name__ == "__main__":
    chat()
