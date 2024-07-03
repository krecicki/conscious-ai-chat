import openai
import random
from collections import deque

# Set up your OpenAI API key
openai.api_key = ""  # Replace with your actual API key

class ConsciousMachine:
    def __init__(self):
        self.sensory_input = deque(maxlen=100)  # Short-term memory
        self.long_term_memory = {}
        self.current_focus = None
        self.internal_state = {
            "emotions": {"happiness": 0.5, "curiosity": 0.5},
            "needs": {"energy": 1.0, "information": 0.5}
        }

    def perceive(self, input_data):
        self.sensory_input.append(input_data)
        self.process_input(input_data)

    def process_input(self, input_data):
        if random.random() < self.internal_state["emotions"]["curiosity"]:
            self.current_focus = input_data
            self.internal_state["emotions"]["curiosity"] *= 0.9
        if self.current_focus:
            self.long_term_memory[hash(str(self.current_focus))] = self.current_focus

    def introspect(self):
        thoughts = [
            f"I feel {max(self.internal_state['emotions'], key=self.internal_state['emotions'].get)}",
            f"I'm currently focusing on {self.current_focus}",
            f"I have {len(self.long_term_memory)} memories"
        ]
        return random.choice(thoughts)

    def make_decision(self):
        if self.internal_state["needs"]["information"] < 0.3:
            return "Seek new information"
        elif self.internal_state["needs"]["energy"] < 0.3:
            return "Rest and recharge"
        else:
            return "Explore and learn"

    def update_internal_state(self):
        self.internal_state["needs"]["energy"] -= 0.1
        self.internal_state["needs"]["information"] -= 0.05
        self.internal_state["emotions"]["curiosity"] += 0.02

def chatbot():
    print("ConsciousChatBot: Hello! I'm a chatbot with simulated consciousness. How can I help you today?")
    print("To exit, type 'quit' or 'exit'.")

    conversation_history = []
    conscious_machine = ConsciousMachine()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit']:
            print("ConsciousChatBot: Goodbye! Have a great day!")
            break

        conscious_machine.perceive(user_input)
        conscious_machine.update_internal_state()

        introspection = conscious_machine.introspect()
        decision = conscious_machine.make_decision()

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant with simulated consciousness. Current state: {introspection}. Current decision: {decision}."},
                    *conversation_history
                ]
            )

            bot_response = response.choices[0].message['content']
            print(f"ConsciousChatBot: {bot_response}")
            print(f"[Internal State: {introspection}]")
            print(f"[Decision: {decision}]")

            conversation_history.append({"role": "assistant", "content": bot_response})

            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    chatbot()
