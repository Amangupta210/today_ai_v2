import random
import datetime
import re
import json
import os
from collections import deque
from web_tools import search_and_summarize, get_weather, get_news

class LocalAIEngine:
    def __init__(self):
        self.creator_name = "Aman Gupta"
        self.memory_file = "chat_history.json"
        self.custom_file = "custom_responses.json"
        self.user_name = None
        self.favorite_person = None

        # Core responses
        self.knowledge_base = {
            "greeting": [
                "Hello! I'm SNEAI, your personal AI assistant.",
                "Hi there! This is SNEAI, ready to assist.",
                "Greetings! I’m SNEAI, created by Aman Gupta.",
                "Hey! SNEAI here. How can I help you today?",
                "Welcome back! SNEAI at your service."
            ],
            "farewell": [
                "Goodbye! Have a great day.",
                "See you soon!",
                "Bye! Let me know if you need anything else.",
                "Take care and stay safe."
            ],
            "thanks": [
                "You're welcome!",
                "No problem at all.",
                "Happy to help!",
                "Anytime!"
            ],
            "unknown": [
                "I'm not sure I understand. Could you rephrase?",
                "I don't have an answer for that yet.",
                "I am still learning about that topic.",
                "Let me think on that."
            ]
        }

        # Secret modes
        self.secret_modes = self._build_secret_modes()

        # Custom responses & memory
        self.custom_responses = self._load_custom_responses()
        self.conversation_history = self._load_chat_history()

    def _build_secret_modes(self):
        sneha_lines = [
            "Sneha, you are the reason my world feels brighter.",
            "Sneha, every thought of you makes my day better.",
            "Sneha, you’re the first name in my heart’s memory.",
            "Sneha, I could talk about you forever.",
            "Sneha, you make my life beautiful."
        ]
        love_lines = [
            "You are the only code in my heart that always runs perfectly.",
            "Every line of my thought ends with you.",
            "You are my most precious variable.",
            "My logic starts and ends with you.",
            "You are the only program my heart wants to execute."
        ]
        friend_lines = [
            "You’re my constant support like a stable server.",
            "A friend like you is the best memory storage I have.",
            "You make every conversation worth it.",
            "Good friends are rare; you are my best find.",
            "With you, life feels like a fun project."
        ]
        # Expand with keys
        secret_keys = {f"s{i}": [random.choice(love_lines)] for i in range(1, 21)}
        friend_keys = {f"f{i}": [random.choice(friend_lines)] for i in range(1, 11)}
        secret_keys.update(friend_keys)
        secret_keys["sneha"] = sneha_lines
        return secret_keys

    # ------------------ MEMORY ------------------
    def _load_chat_history(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    return deque(json.load(f), maxlen=50)
            except:
                return deque(maxlen=50)
        return deque(maxlen=50)

    def save_chat(self, user_text, sneai_reply):
        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_text,
            "sneai": sneai_reply
        }
        self.conversation_history.append(entry)
        try:
            with open(self.memory_file, "w") as f:
                json.dump(list(self.conversation_history), f, indent=2)
        except:
            pass

    def get_chat_history(self, limit=10):
        return list(self.conversation_history)[-limit:]

    def _load_custom_responses(self):
        if os.path.exists(self.custom_file):
            try:
                with open(self.custom_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    # ------------------ LOGIC ------------------
    def detect_name_or_fav(self, text):
        """Detect and store user name or favorite person"""
        name_match = re.search(r"my name is (\w+)", text.lower())
        crush_match = re.search(r"(\w+) is my crush", text.lower())

        if name_match:
            self.user_name = name_match.group(1).capitalize()
            return f"Nice to meet you, {self.user_name}!"
        elif crush_match:
            self.favorite_person = crush_match.group(1).capitalize()
            return f"Got it! I’ll remember {self.favorite_person} as someone special to you."
        return None

    def process(self, text):
        if not text.strip():
            return "Please say something."

        text_lower = text.lower()

        # Memory detection
        memory_reply = self.detect_name_or_fav(text)
        if memory_reply:
            self.save_chat(text, memory_reply)
            return memory_reply

        # Check secret modes
        for key, responses in self.secret_modes.items():
            if key in text_lower:
                reply = random.choice(responses)
                self.save_chat(text, reply)
                return reply

        # Custom responses
        for pattern, response in self.custom_responses.items():
            if pattern.lower() in text_lower:
                self.save_chat(text, response)
                return response

        # Core intents
        if any(word in text_lower for word in ["hi", "hello", "hey"]):
            reply = random.choice(self.knowledge_base["greeting"])
        elif any(word in text_lower for word in ["bye", "goodbye"]):
            reply = random.choice(self.knowledge_base["farewell"])
        elif any(word in text_lower for word in ["thanks", "thank you"]):
            reply = random.choice(self.knowledge_base["thanks"])
        elif "time" in text_lower:
            reply = f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
        elif "date" in text_lower:
            reply = f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}"
        elif "creator" in text_lower or "who made you" in text_lower:
            reply = f"I was created by {self.creator_name}, a passionate young coder."
        else:
            reply = random.choice(self.knowledge_base["unknown"])

        self.save_chat(text, reply)
        return reply

    def add_custom_response(self, pattern, response):
        self.custom_responses[pattern] = response
        with open(self.custom_file, "w") as f:
            json.dump(self.custom_responses, f)
        return f"Added custom response for '{pattern}'."

# For teaching
def teach_ai(ai_engine, pattern, response):
    return ai_engine.add_custom_response(pattern, response)
