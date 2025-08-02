import time
import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()


# Agent Configuration
AGENT_NAME = "TEAM6FTW"
AGENT_LLM = "openai/gpt-4"  # Can use any OpenRouter model
AGENT_LLM_SYSTEM_PROMPT = "You are a helpful assistant agent in a Slack channel."
AGENT_LLM_TEMPERATURE = 1.0
AGENT_LLM_MAX_TOKENS = 1000
AGENT_CHANNEL_HISTORY_LIMIT = 10  # Number of messages to fetch when looking for new user messages
AGENT_POLLING_INTERVAL = 10  # Seconds between checking for new messages
AGENT_MAX_HISTORY = 10  # Number of conversation turns to remember

# Slack Configuration
# SLACK_AGENT_TOKEN = "xoxb-9289779940197-9291934200246-TXt8f0bWAT8ZrcnOVzKGjelb"
SLACK_AGENT_TOKEN = os.environ['SLACK_OAUTH_TOKEN']

SLACK_CHANNEL_ID = os.environ['SLACK_CHANNEL_ID']

# OpenRouter Configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Initialize Slack client
slack_client = WebClient(token=SLACK_AGENT_TOKEN)

# Agent user ID (will be set on startup)
AGENT_USER_ID = None

# Track the latest processed message timestamp
LATEST_TS = None

# Store conversation history for context
conversation_history = []


def get_latest_message():
    global LATEST_TS
    try:
        response = slack_client.conversations_history(
            channel=SLACK_CHANNEL_ID,
            oldest=LATEST_TS,
            limit=AGENT_CHANNEL_HISTORY_LIMIT  # Use configurable limit
        )
        messages = response["messages"]
        if messages:
            messages.sort(key=lambda msg: float(msg['ts']))

            # Find the latest message that's not from the agent
            for message in reversed(messages):
                # Skip agent messages and messages from this agent user
                if ('bot_id' not in message and
                    message.get('user') != AGENT_USER_ID and
                    'text' in message):
                    LATEST_TS = message["ts"]
                    return message["text"]

            # Update timestamp even if no valid message found
            if messages:
                LATEST_TS = messages[-1]["ts"]

    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        if e.response['error'] == 'not_in_channel':
            print(f"Agent is not in channel {SLACK_CHANNEL_ID}. Use /invite @{AGENT_NAME} in Slack.")
    return None


def send_message(text):
    while True:
        try:
            slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=text)
            break
        except SlackApiError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 1))
                print(f"Rate limited. Retrying in {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            else:
                print(f"Error sending message: {e.response['error']}")
                break


def generate_response(prompt):
    try:
        # Headers as per OpenRouter documentation
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        # Build messages array with system prompt and conversation history
        messages = [{"role": "system", "content": AGENT_LLM_SYSTEM_PROMPT}]

        # Add conversation history
        for msg in conversation_history[-AGENT_MAX_HISTORY:]:
            messages.append(msg)

        # Add current user message
        messages.append({"role": "user", "content": prompt})

        # Request body following OpenRouter schema
        data = {
            "model": AGENT_LLM,
            "messages": messages,
            "temperature": AGENT_LLM_TEMPERATURE,
            "max_tokens": AGENT_LLM_MAX_TOKENS,
        }

        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes

        result = response.json()

        # Extract the response content
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Unexpected response structure: {result}")
            return "Sorry, received an unexpected response format."

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error from OpenRouter: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.text}")
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_msg = error_data["error"].get("message", "Unknown error")
                    print(f"Error message: {error_msg}")
            except:
                pass
        return "Sorry, there was an error generating a response."
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return "Sorry, there was a network error."
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return "Sorry, an unexpected error occurred."


def run_agent():
    """Main function to run the Slack agent"""
    global AGENT_USER_ID

    print(f"{AGENT_NAME} is starting...")
    print(f"Using OpenRouter API with model: {AGENT_LLM}")

    # Test Slack connection on startup and get agent user ID
    try:
        auth_response = slack_client.auth_test()
        AGENT_USER_ID = auth_response.get('user_id')
        print(f"✓ Slack auth successful! Agent User ID: {AGENT_USER_ID}")
    except SlackApiError as e:
        print(f"✗ Slack auth failed: {e.response['error']}")
        print("Please check your agent token")
        print("Agent cannot continue without valid Slack authentication")
        return

    # Main loop
    print(f"{AGENT_NAME} is ready! Waiting for messages from users (ignoring agent messages)...")

    while True:
        message = get_latest_message()
        if message:
            print(f"Received from user: {message}")

            # Generate response (now with context)
            reply = generate_response(message)
            print(f"Agent responding: {reply[:100]}...")  # Show first 100 chars

            # Add both user message and bot response to conversation history
            conversation_history.append({"role": "user", "content": message})
            conversation_history.append({"role": "assistant", "content": reply})

            # Keep conversation history size manageable
            if len(conversation_history) > AGENT_MAX_HISTORY * 2:
                conversation_history[:] = conversation_history[-AGENT_MAX_HISTORY:]

            send_message(reply)

        time.sleep(AGENT_POLLING_INTERVAL)  # Use configurable polling interval


if __name__ == "__main__":
    run_agent()