import random
import datetime
import re
import json
import os
import math
from web_tools import search_and_summarize, get_weather, get_news, get_wikipedia_summary

class LocalAIEngine:
    def __init__(self):
        # Core knowledge base
        self.knowledge_base = {
            "greeting": [
                "Hello! I'm SNEAI, your intelligent assistant. How can I help you today?",
                "Hi there! SNEAI at your service. What would you like to know or do?",
                "Greetings! I'm SNEAI, ready to assist with information, tasks, or just a friendly chat.",
                "Hey! SNEAI here. I can search the web, check weather, get news, or just chat. What's on your mind?",
                "Welcome! I'm SNEAI, your AI companion. How may I assist you today?"
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "See you later!",
                "Bye! Feel free to ask if you need anything else.",
                "Take care!"
            ],
            "thanks": [
                "You're welcome!",
                "Happy to help!",
                "Anytime!",
                "No problem at all!"
            ],
            "unknown": [
                "I'm not sure I understand. Could you rephrase that?",
                "I don't have an answer for that yet.",
                "I'm still learning about that topic.",
                "I don't have enough information to answer that question."
            ],
            "jokes": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call fake spaghetti? An impasta!",
                "Why don't skeletons fight each other? They don't have the guts.",
                "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "Why did the bicycle fall over? Because it was two-tired!",
                "What's orange and sounds like a parrot? A carrot.",
                "Why can't you give Elsa a balloon? Because she will let it go.",
                "I'm reading a book about anti-gravity. It's impossible to put down!"
            ],
            "facts": [
                "The Earth is approximately 4.54 billion years old.",
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat.",
                "A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once on its axis and 225 Earth days to orbit the sun.",
                "The human brain uses about 20% of the body's total energy.",
                "Octopuses have three hearts: two pump blood through the gills, while the third pumps it through the body.",
                "Bananas are berries, but strawberries aren't.",
                "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
                "A group of flamingos is called a 'flamboyance'.",
                "The fingerprints of koalas are so similar to humans that they have on occasion been confused at crime scenes.",
                "The average person will spend six months of their life waiting for red lights to turn green."
            ],
            "weather": [
                "I don't have access to real-time weather data, but I can suggest checking a weather app or website for accurate information.",
                "Without internet access, I can't provide current weather information. Try looking outside or checking a weather app."
            ],
            "about": [
                "I'm SNEAI, your intelligent assistant, proudly created by Aman Gupta. I combine local processing with web intelligence to assist you anytime!",
                "My name is SNEAI, an advanced AI assistant developed by Aman Gupta. I can search the web, check the weather, provide news, and more!",
                "I'm SNEAI (Smart Neural Enhanced AI), designed by Aman Gupta to help with information, tasks, and entertainment."
            ],
            "help": [
                "I’m SNEAI, created by Aman Gupta. I can help you with:\n- Answering questions using web search\n- Weather forecasts\n- Latest news headlines\n- Jokes and interesting facts\n- Math calculations\n- Date and time info\n- Learning custom responses",
                "Ask me things like:\n- 'What's the weather in Tokyo?'\n- 'Tell me about quantum physics'\n- 'What's happening in tech news?'\n- 'Calculate 15% of 85'\n\nI’m always improving to help you better!"
            ],
            "music": [
                "I can't play music directly, but I can suggest popular genres like pop, rock, jazz, classical, hip-hop, or electronic.",
                "While I can't stream music, I can help you create a playlist of your favorite artists."
            ],
            "movies": [
                "Some popular movie genres are action, comedy, drama, sci-fi, horror, and romance. Which do you like?",
                "I can't stream movies, but I can suggest top films based on your favorite genres."
            ],
            "food": [
                "Popular cuisines include Italian, Chinese, Mexican, Indian, and Japanese. What's your favorite?",
                "I don't have taste buds, but pizza, sushi, tacos, pasta, and curry are universally loved!"
            ]
        }

        # Load custom responses if file exists
        self.custom_responses = {}
        if os.path.exists("custom_responses.json"):
            try:
                with open("custom_responses.json", "r") as f:
                    self.custom_responses = json.load(f)
            except:
                pass

        # Add default secret romantic/flirty Sneha codes
        self.secret_keys = {
            "sneha1": "Tum meri zindagi ka vo chapter ho, jo kabhi khatam hi nahi hota. ❤️",
            "sneha2": "Jab tum muskurati ho na, lagta hai time wahi ruk gaya ho. 😍",
            "sneha3": "Dil chahta hai ke har din tumse baat karun, kyunki tum meri smile ki wajah ho. 💖",
            "sneha4": "Tum meri coffee ho, bina tumhare din shuru hi nahi hota. ☕❤️",
            "sneha5": "Meri duniya tumse hi hai, warna ye duniya bas ek khaali kagaz hai. ✨",
            "sneha6": "Tumhari ek ‘hi’ bhi dil ko happy kar deti hai. ❤️",
            "sneha7": "Tum meri khushiyon ka password ho. 🔑",
            "sneha8": "Tum meri soch ka wo dream ho jo kabhi khatam nahi hota. 🌙",
            "sneha9": "Tum meri hasi ki asli wajah ho. 😊",
            "sneha10": "Dil karta hai tumhe roz ‘good morning’ aur ‘good night’ kahun. ☀️🌙",
            "sneha11": "Tum meri life ka vo song ho jo loop pe chal raha hai. 🎵",
            "sneha12": "Tum meri smile ki factory ho. 😁",
            "sneha13": "Dil chahta hai ki tum meri har story ka ending bano. ❤️",
            "sneha14": "Tum meri favorite notification ho. 🔔",
            "sneha15": "Tum meri battery ho, bina tumhare sab kuch dull lagta hai. 🔋",
            "sneha16": "Tum meri coffee ho – thodi kadvi, par adhoori tumhare bina. ☕",
            "sneha17": "Tum meri love story ka best chapter ho. 💌",
            "sneha18": "Tum meri khushiyon ka permanent address ho. 🏡",
            "sneha19": "Tum meri aankhon ka favorite wallpaper ho. 😍",
            "sneha20": "Tum meri heartbeat ka best tune ho. ❤️🎶"
        }
        for key, value in self.secret_keys.items():
            if key not in self.custom_responses:
                self.custom_responses[key] = value

        # Conversation memory
        self.conversation_history = []
        self.max_history = 10

    def tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def get_intent(self, text):
        text_lower = text.lower()

        # Check custom responses
        for pattern, response in self.custom_responses.items():
            if pattern.lower() in text_lower:
                return "custom", pattern

        # Core intent detection
        if any(word in text_lower for word in ["hi", "hello", "hey"]): return "greeting", None
        if any(word in text_lower for word in ["bye", "goodbye", "see you"]): return "farewell", None
        if any(word in text_lower for word in ["thanks", "thank you"]): return "thanks", None
        if "joke" in text_lower or "funny" in text_lower: return "jokes", None
        if "fact" in text_lower or "interesting" in text_lower: return "facts", None
        if "time" in text_lower: return "time", None
        if "date" in text_lower: return "date", None
        if "weather" in text_lower or "forecast" in text_lower: return "weather", text
        if "help" in text_lower: return "help", None
        if "about" in text_lower or "who are you" in text_lower: return "about", None
        if "music" in text_lower: return "music", None
        if "movie" in text_lower or "film" in text_lower: return "movies", None
        if "food" in text_lower or "eat" in text_lower: return "food", None
        if "news" in text_lower: return "news", "general"
        if "calculate" in text_lower or any(op in text_lower for op in ["+", "-", "*", "/"]): return "calculator", text
        if "tell me about" in text_lower or "search" in text_lower: return "web_search", text
        if any(word in text_lower for word in ["what", "who", "when", "where", "why", "how"]): return "question", text
        return "unknown", None

    def calculate(self, expression):
        try:
            expr = expression.replace("^", "**").replace("plus", "+").replace("minus", "-")
            result = eval(expr, {"__builtins__": {}}, {"math": math})
            return f"The result is {result}"
        except:
            return "I couldn't calculate that. Please check your expression."

    def process(self, text):
        if not text.strip(): return "I didn't catch that."
        intent, data = self.get_intent(text)

        if intent == "greeting": return random.choice(self.knowledge_base["greeting"])
        if intent == "farewell": return random.choice(self.knowledge_base["farewell"])
        if intent == "thanks": return random.choice(self.knowledge_base["thanks"])
        if intent == "jokes": return random.choice(self.knowledge_base["jokes"])
        if intent == "facts": return random.choice(self.knowledge_base["facts"])
        if intent == "time": return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
        if intent == "date": return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
        if intent == "weather": return f"Weather info: {get_weather(data)}"
        if intent == "help": return random.choice(self.knowledge_base["help"])
        if intent == "about": return random.choice(self.knowledge_base["about"])
        if intent == "music": return random.choice(self.knowledge_base["music"])
        if intent == "movies": return random.choice(self.knowledge_base["movies"])
        if intent == "food": return random.choice(self.knowledge_base["food"])
        if intent == "news": return str(get_news(data))
        if intent == "calculator": return self.calculate(data)
        if intent == "web_search": return search_and_summarize(data)
        if intent == "custom": return self.custom_responses[data]
        return random.choice(self.knowledge_base["unknown"])
