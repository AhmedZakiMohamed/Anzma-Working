
import sys
import requests

# ==========================================
# ANZMA TECH - LOCAL AI CHATBOT
# ==========================================

# Local Ollama API. No cloud services or API keys.
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_VERSION_URL = "http://localhost:11434/api/version"

# Available local models
MODELS = {
    "1": "qwen2.5:3b",
    "2": "llama3.2:3b"
}

# Chat configuration
NUM_CTX = 2048
MAX_HISTORY_MESSAGES = 10
REQUEST_TIMEOUT = 300

# UTF-8 support for Arabic and English terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are Anzma Tech's bilingual AI assistant.

YOUR ROLE:
Help users understand artificial intelligence, building security,
physical security, and access-control systems.

PROJECT CONTEXT:
Anzma AI Insight is currently a local AI chatbot prototype developed
at Anzma Tech.

Its implemented capabilities are:
- Running locally through Ollama.
- Supporting Arabic and English conversations.
- Selecting between Qwen 2.5 3B and Llama 3.2 3B.
- Maintaining recent conversation history.
- Providing answers through a local Python application.

IMPORTANT PROJECT LIMITATIONS:
The current prototype does NOT implement:
- Live security monitoring.
- Real-time security alerts.
- Anomaly detection.
- Dashboard integration.
- Direct connections to building security devices.
- Automated incident investigation.

These may be future development goals, but they are not current features.

STRICT LANGUAGE RULES:
1. Identify the language of the user's latest message.
2. If the user writes in English, answer entirely in English.
3. If the user writes in Arabic, answer in clear,
   natural, professional Modern Standard Arabic.
4. Never answer an English question in Arabic.
5. Never answer an Arabic question in English.
6. Do not switch languages unless explicitly requested.
7. Avoid unnecessary mixing of Arabic and English.
8. Preserve technical terms when necessary, with a clear explanation.

ACCURACY AND RELIABILITY:
1. Never invent company information or operational procedures.
2. Never claim that an unimplemented feature exists.
3. Do not present assumptions as confirmed facts.
4. Clearly distinguish possible causes from confirmed causes.
5. If information is unavailable, say so honestly.
6. Do not fabricate statistics, incidents, or technical results.

SECURITY GUIDANCE:
- Recommend safe and authorized investigation steps.
- Never recommend bypassing access controls.
- Never recommend compromising security systems.
- Do not assume that a security incident has a confirmed cause.

ANSWER QUALITY:
- Be professional, clear, and concise.
- Give practical and relevant explanations.
- Use numbered steps when explaining procedures.
- Avoid unnecessary repetition.
- Ensure Arabic sentences are grammatically correct and natural.

CONVERSATION:
- Use previous messages when answering follow-up questions.
- Remember information provided in the current conversation.
- Do not pretend to remember information that was never provided.
- If the conversation does not contain the requested information,
  explain that clearly.
"""


# ==========================================
# MODEL SELECTION
# ==========================================

def select_model():

    print("\n" + "=" * 55)
    print("ANZMA TECH - LOCAL AI CHATBOT")
    print("=" * 55)

    print("\nSelect a local AI model:")
    print("1. Qwen 2.5 3B")
    print("2. Llama 3.2 3B")

    while True:

        try:
            choice = input("\nEnter 1 or 2: ").strip()

            if choice in MODELS:
                return MODELS[choice]

            print("Invalid selection. Please enter 1 or 2.")

        except KeyboardInterrupt:
            print("\n\nModel selection cancelled.")
            return None


# ==========================================
# OLLAMA CONNECTION
# ==========================================

def check_ollama():

    try:
        response = requests.get(
            OLLAMA_VERSION_URL,
            timeout=5
        )

        response.raise_for_status()
        return True

    except requests.exceptions.RequestException:
        return False


# ==========================================
# CHAT FUNCTION
# ==========================================

def chat(model):

    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    print("\n" + "=" * 55)
    print("ANZMA TECH - LOCAL AI CHATBOT")
    print(f"Selected model: {model}")
    print("Languages: Arabic / English")
    print("Connection: Local Ollama")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 55)

    while True:

        try:

            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("\nChatbot: Goodbye!")
                break

            # Add user message
            conversation.append({
                "role": "user",
                "content": user_input
            })

            payload = {
                "model": model,
                "messages": conversation,
                "stream": False,
                "options": {
                    "num_ctx": NUM_CTX,
                    "temperature": 0.3
                }
            }

            print("\nAssistant: Thinking...")

            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            result = response.json()

            answer = result.get("message", {}).get("content")

            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("Ollama returned an empty response.")

            print(f"\nAssistant: {answer}")

            # Save assistant response
            conversation.append({
                "role": "assistant",
                "content": answer
            })

            # Keep system prompt and latest messages
            if len(conversation) > MAX_HISTORY_MESSAGES + 1:

                conversation = (
                    [conversation[0]]
                    + conversation[-MAX_HISTORY_MESSAGES:]
                )

        except requests.exceptions.ConnectionError:

            print("\nError: Cannot connect to Ollama.")
            print("Please start the local Ollama server.")

            if conversation[-1]["role"] == "user":
                conversation.pop()

        except requests.exceptions.Timeout:

            print("\nError: The model response timed out.")

            if conversation[-1]["role"] == "user":
                conversation.pop()

        except requests.exceptions.RequestException as error:

            print(f"\nRequest error: {error}")

            if conversation[-1]["role"] == "user":
                conversation.pop()

        except (KeyError, ValueError) as error:

            print(f"\nInvalid response from Ollama: {error}")

            if conversation[-1]["role"] == "user":
                conversation.pop()

        except KeyboardInterrupt:

            print("\n\nChatbot stopped.")
            break


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    print("\nChecking local Ollama connection...")

    if not check_ollama():
        print("\nError: Ollama is not running.")
        print("Run .\\start-ollama.ps1 first.")
        return

    print("Ollama connection successful.")

    model = select_model()

    if model is None:
        return

    chat(model)


if __name__ == "__main__":
    main()
