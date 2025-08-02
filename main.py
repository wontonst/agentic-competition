import requests
import sys
import time
from datetime import datetime

from slack_utils import send_message

# Agent 1 Configuration
AGENT1_NAME = "Agent 1"
AGENT1_LLM = "anthropic/claude-3.5-sonnet"
AGENT1_SYSTEM_PROMPT = "You are Agent 1, a creative and imaginative AI who loves storytelling and metaphors. Keep responses very concise - one short sentence only. No line breaks."
AGENT1_TEMPERATURE = 1.2
AGENT1_MAX_TOKENS = 100

# Agent 2 Configuration
AGENT2_NAME = "Agent 2"
AGENT2_LLM = "google/gemini-flash-1.5"
AGENT2_SYSTEM_PROMPT = "You are Agent 2, a logical and analytical AI who values precision and facts. Keep responses very concise - one short sentence only. No line breaks."
AGENT2_TEMPERATURE = 0.7
AGENT2_MAX_TOKENS = 100

# Agent 3 Configuration
AGENT3_NAME = "Agent 3"
AGENT3_LLM = "meta-llama/llama-3.1-8b-instruct"
AGENT3_SYSTEM_PROMPT = "You are Agent 3, an enthusiastic and energetic AI who gets excited about everything. Keep responses very concise - one short sentence only. No line breaks."
AGENT3_TEMPERATURE = 1.0
AGENT3_MAX_TOKENS = 100

# Agent 4 Configuration
AGENT4_NAME = "Agent 4"
AGENT4_LLM = "mistralai/mistral-7b-instruct"
AGENT4_SYSTEM_PROMPT = "You are Agent 4, a philosophical and thoughtful AI who sees deeper meaning in things. Keep responses very concise - one short sentence only. No line breaks."
AGENT4_TEMPERATURE = 0.9
AGENT4_MAX_TOKENS = 100

# Shared Configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_HISTORY = 40  # Increased for 4 agents
DELAY_BETWEEN_MESSAGES = 0.5  # Seconds between messages for readability

# Game Instruction
GAME_INSTRUCTION = "Let's play a counting game! I'll start: 1"

# Store conversation history
conversation_history = []

# Define all agents
AGENTS = [
    {
        "name": AGENT1_NAME,
        "model": AGENT1_LLM,
        "system_prompt": AGENT1_SYSTEM_PROMPT,
        "temperature": AGENT1_TEMPERATURE,
        "max_tokens": AGENT1_MAX_TOKENS,
        "color": "\033[95m"  # Purple
    },
    {
        "name": AGENT2_NAME,
        "model": AGENT2_LLM,
        "system_prompt": AGENT2_SYSTEM_PROMPT,
        "temperature": AGENT2_TEMPERATURE,
        "max_tokens": AGENT2_MAX_TOKENS,
        "color": "\033[96m"  # Cyan
    },
    {
        "name": AGENT3_NAME,
        "model": AGENT3_LLM,
        "system_prompt": AGENT3_SYSTEM_PROMPT,
        "temperature": AGENT3_TEMPERATURE,
        "max_tokens": AGENT3_MAX_TOKENS,
        "color": "\033[93m"  # Yellow
    },
    {
        "name": AGENT4_NAME,
        "model": AGENT4_LLM,
        "system_prompt": AGENT4_SYSTEM_PROMPT,
        "temperature": AGENT4_TEMPERATURE,
        "max_tokens": AGENT4_MAX_TOKENS,
        "color": "\033[92m"  # Green
    }
]


def clean_response(text):
    """Clean up response text by removing extra whitespace and newlines"""
    # Strip leading/trailing whitespace
    text = text.strip()
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    # Remove any newlines and replace with space
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Clean up any multiple spaces that might have been created
    text = ' '.join(text.split())
    return text


def generate_response(prompt, agent_config, history):
    """Generate response for a specific agent"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        # Build messages with agent's personality and history
        messages = [{"role": "system", "content": agent_config["system_prompt"]}]

        # Add conversation history
        for msg in history[-MAX_HISTORY:]:
            messages.append(msg)

        # Add current message
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": agent_config["model"],
            "messages": messages,
            "temperature": agent_config["temperature"],
            "max_tokens": agent_config["max_tokens"],
        }

        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            # Clean the response before returning
            return clean_response(result["choices"][0]["message"]["content"])
        else:
            return "I couldn't generate a response."

    except Exception as e:
        print(f"\n[Error] {agent_config['name']}: {type(e).__name__}: {e}")
        return "Sorry, I encountered an error."


def print_message(agent_name, message, color_code=""):
    """Print a formatted message from an agent"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    # Ensure message is clean before printing
    clean_msg = clean_response(message)
    print(f"{color_code}[{timestamp}] {agent_name}: {clean_msg}\033[0m")


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*70)
    print("🤖 Four AI Agents Counting Game 🤖")
    print("="*70)
    print(f"\n\033[95m{AGENT1_NAME}\033[0m - \033[96m{AGENT2_NAME}\033[0m - \033[93m{AGENT3_NAME}\033[0m - \033[92m{AGENT4_NAME}\033[0m")
    print("\nPress Ctrl+C to stop at any time")
    print("="*70)


def run_conversation():
    """Run a conversation between four agents"""
    print(f"\n{'='*70}")
    print(f"Starting endless conversation (Press Ctrl+C to stop)")
    print(f"{'='*70}\n")

    # Clear conversation history for new conversation
    conversation_history.clear()

    # Add game instruction as initial admin message
    print(f"\033[91m[{datetime.now().strftime('%H:%M:%S')}] Admin: {GAME_INSTRUCTION}\033[0m")
    conversation_history.append({
        "role": "user",
        "content": f"Admin: {GAME_INSTRUCTION}"
    })

    # Start with the game instruction as the first message
    current_message = GAME_INSTRUCTION
    agent_index = 0

    # Run forever until interrupted
    turn = 0
    while True:
        try:
            current_agent = AGENTS[agent_index]

            # Show typing indicator - use flush to ensure it appears
            print(f"{current_agent['color']}[{current_agent['name']} is thinking...]\033[0m", end="\r", flush=True)

            # Generate response
            response = generate_response(
                current_message,
                current_agent,
                conversation_history
            )

            # Clear typing indicator line completely
            print(" " * 80, end="\r")

            # Print the response
            print_message(current_agent['name'], response, current_agent['color'])
            send_message(f"{current_agent['name']}: {response}")

            # Update conversation history
            conversation_history.append({
                "role": "user",
                "content": current_message
            })
            conversation_history.append({
                "role": "assistant",
                "content": response
            })

            # Prepare for next turn
            current_message = response
            agent_index = (agent_index + 1) % 4  # Cycle through 4 agents
            turn += 1

            # Delay for readability
            time.sleep(DELAY_BETWEEN_MESSAGES)

        except KeyboardInterrupt:
            print(f"\n\n{'='*70}")
            print(f"Conversation ended after {turn} messages")
            print(f"{'='*70}\n")
            break


def main():
    """Main function"""
    print_welcome()

    try:
        run_conversation()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\n[Error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)