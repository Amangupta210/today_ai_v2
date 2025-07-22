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

        # Core Knowledge Base
        self.knowledge_base = {
            "greeting": [
                "Hello! I'm SNEAI, your personal AI.",
                "Hi there! This is SNEAI, ready to assist.",
                "Greetings! SNEAI here to help.",
                "Welcome back, buddy!",
                "Hey! SNEAI at your service."
            ],
            "farewell": [
                "Goodbye! Have a great day ahead.",
                "See you soon!",
                "Bye! Need anything else later?",
                "Take care and stay awesome!"
            ],
            "thanks": [
                "You're welcome!",
                "Happy to help!",
                "Anytime!",
                "No problem at all."
            ],
            "unknown": [
                "I’m not sure about that.",
                "Can you rephrase your question?",
                "Hmm, I don't have that info yet.",
                "I’ll learn this soon!"
            ]
        }

        # Secret Modes
        self.secret_modes = self._build_secret_modes()

        # Extras (Jokes, Motivation, Quotes)
        self.jokes = [
            "Why don’t programmers like nature? Too many bugs.",
            "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
            "Why did the developer go broke? Because he used up all his cache."
        ]
        self.motivational_lines = [
            "Believe in yourself, and all that you are.",
            "Your potential is endless.",
            "Keep pushing forward, no matter what.",
            "Dream big and dare to fail."
        ]
        self.quotes = [
            "“The best way to get started is to quit talking and begin doing.” – Walt Disney",
            "“Success is not the key to happiness. Happiness is the key to success.” – Albert Schweitzer",
            "“Your time is limited, so don’t waste it living someone else’s life.” – Steve Jobs"
        ]

        # Memory
        self.custom_responses = self._load_custom_responses()
        self.conversation_history = self._load_chat_history()

    # -------------------- SECRET MODES --------------------
    def _build_secret_modes(self):
        sneha_lines = [
            "Sneha, tum meri coding life ki sabse pyari bug fix ho.",
            "Sneha, tumhari ek smile mere dil ka patch update hai.",
            "Sneha, tum meri duniya ka best commit ho.",
            "Sneha, tum meri sabse special constant ho.",
            "Sneha, tum meri heart function ki return value ho."
        ]

        love_lines = [
            "Tum meri love story ki perfect syntax ho.",
            "My love for you is infinite like a while loop.",
            "You’re the API my heart calls every second.",
            "If love was code, you’d be my main function.",
            "You’re my favorite output, always.",
            "I’d debug the whole world for your smile.",
            "You’re the perfect algorithm for my happiness.",
            "Tum meri zindagi ki perfect class ho.",
            "You’re the semicolon to my statements.",
            "My logic starts and ends with you."
        ] * 3  # Make 30+

        friend_lines = [
            "A friend like you is my true cloud backup.",
            "Tum meri life ke open-source library ho.",
            "Friends like you make life bug-free.",
            "Best friends are like solid frameworks.",
            "You are my permanent server of happiness."
        ] * 3  # Make 15+

        # Keys
        secret_keys = {f"s{i}": [random.choice(love_lines)] for i in range(1, 31)}
        friend_keys = {f"f{i}": [random.choice(friend_lines)] for i in range(1, 16)}
        secret_keys.update(friend_keys)
        secret_keys["sneha"] = sneha_lines
        return secret_keys

    # -------------------- MEMORY --------------------
    def _load_chat_history(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    return deque(json.load(f), maxlen=100)
            except:
                return deque(maxlen=100)
        return deque(maxlen=100)

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

    # -------------------- LOGIC --------------------
    def detect_name_or_fav(self, text):
        name_match = re.search(r"my name is (\w+)", text.lower())
        crush_match = re.search(r"(\w+) is my crush", text.lower())

        if name_match:
            self.user_name = name_match.group(1).capitalize()
            return f"Nice to meet you, {self.user_name}!"
        elif crush_match:
            self.favorite_person = crush_match.group(1).capitalize()
            return f"Got it! I’ll remember {self.favorite_person} as your crush."
        return None

    def process(self, text):
        if not text.strip():
            return "Please say something."

        text_lower = text.lower()

        # Memory
        memory_reply = self.detect_name_or_fav(text)
        if memory_reply:
            self.save_chat(text, memory_reply)
            return memory_reply

        # Secret modes
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

        # Features
        if "joke" in text_lower:
            reply = random.choice(self.jokes)
        elif "motivation" in text_lower:
            reply = random.choice(self.motivational_lines)
        elif "quote" in text_lower:
            reply = random.choice(self.quotes)
        elif "wikipedia" in text_lower:
            topic = text_lower.replace("wikipedia", "").strip() or "Artificial Intelligence"
            reply = search_and_summarize(topic)
        elif "weather" in text_lower:
            reply = get_weather()
        elif "news" in text_lower:
            reply = get_news()
        elif any(word in text_lower for word in ["hi", "hello", "hey"]):
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
            reply = f"I was created by {self.creator_name}."
        else:
            reply = random.choice(self.knowledge_base["unknown"])

        self.save_chat(text, reply)
        return reply

    def add_custom_response(self, pattern, response):
        self.custom_responses[pattern] = response
        with open(self.custom_file, "w") as f:
            json.dump(self.custom_responses, f, indent=2)
        return f"Added custom response for '{pattern}'."


# Teaching Helper
def teach_ai(ai_engine, pattern, response):
    return ai_engine.add_custom_response(pattern, response)
