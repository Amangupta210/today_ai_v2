import random
import datetime
import re
import json
import os
import math
import threading
from collections import Counter
from web_tools import search_and_summarize, get_weather, get_news, get_wikipedia_summary

class LocalAIEngine:
    def __init__(self):
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
                "I'm SNEAI, your intelligent assistant created by Aman Gupta. I combine local processing with web intelligence to answer your questions, provide information, and assist with various tasks. Unlike other assistants, I don't rely heavily on external APIs, making me efficient and responsive.",
                "My name is SNEAI, an advanced AI assistant designed to help you with information, tasks, and entertainment. I can search the web, check the weather, provide news updates, tell jokes, and much more - all while maintaining a lightweight footprint.",
                "I'm SNEAI (Smart Neural Enhanced AI), your personal digital companion. I was created to provide intelligent assistance through a combination of built-in knowledge and selective web searching. I'm constantly learning and improving to serve you better."
            ],
            "help": [
                "As SNEAI, I can help you with:\n- Answering questions using web search\n- Providing weather forecasts for any location\n- Sharing the latest news headlines\n- Telling jokes and interesting facts\n- Performing calculations\n- Giving time and date information\n- Learning custom responses\n\nTry asking me things like:\n- 'What's the weather in Tokyo?'\n- 'Tell me about quantum physics'\n- 'What's happening in technology news?'\n- 'Calculate 15% of 85'\n\nI'm constantly improving to serve you better!",
                "SNEAI at your service! Here's what I can do for you:\n- Search the web for information\n- Check weather conditions worldwide\n- Get the latest news updates\n- Tell jokes and share interesting facts\n- Perform mathematical calculations\n- Provide time and date information\n- Learn from our conversations\n\nFeel free to ask me anything, and I'll do my best to help!"
            ],
            "music": [
                "I can't play music directly, but I can suggest some genres you might enjoy: pop, rock, jazz, classical, hip-hop, or electronic.",
                "While I can't stream music, I can recommend creating a playlist with your favorite artists for different moods."
            ],
            "movies": [
                "Some popular movie genres include action, comedy, drama, sci-fi, horror, and romance. What type of movies do you enjoy?",
                "I can't stream movies, but I can suggest creating a watchlist of films you'd like to see based on your favorite genres."
            ],
            "food": [
                "Some popular cuisines around the world include Italian, Chinese, Mexican, Indian, and Japanese. Do you have a favorite?",
                "I don't have taste buds, but I've heard that pizza, sushi, tacos, pasta, and curry are among the most beloved foods globally."
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
        
        # Initialize conversation memory
        self.conversation_history = []
        self.max_history = 10

    def tokenize(self, text):
        """Simple tokenization by converting to lowercase and splitting on non-alphanumeric characters"""
        text = text.lower()
        return re.findall(r'\w+', text)
    
    def get_intent(self, text):
        """Determine the intent of the user's message"""
        text_lower = text.lower()
        
        # Check for custom responses first
        for pattern, response in self.custom_responses.items():
            if pattern.lower() in text_lower:
                return "custom", pattern
        
        # Check for specific commands/intents
        if any(word in text_lower for word in ["hi", "hello", "hey", "greetings"]):
            return "greeting", None
        
        if any(word in text_lower for word in ["bye", "goodbye", "see you", "farewell"]):
            return "farewell", None
            
        if any(word in text_lower for word in ["thanks", "thank you", "appreciate"]):
            return "thanks", None
            
        if any(word in text_lower for word in ["joke", "funny", "laugh", "humor"]):
            return "jokes", None
            
        if any(word in text_lower for word in ["fact", "interesting", "did you know"]):
            return "facts", None
            
        if "time" in text_lower and not "sometime" in text_lower:
            return "time", None
            
        if "date" in text_lower and not "update" in text_lower:
            return "date", None
            
        if any(word in text_lower for word in ["weather", "temperature", "forecast", "rain", "sunny"]) and any(word in text_lower for word in ["in", "at", "for"]):
            # Extract location
            location = None
            words = text_lower.split()
            for i, word in enumerate(words):
                if word in ["in", "at", "for"] and i+1 < len(words):
                    location = words[i+1]
                    if i+2 < len(words) and words[i+2] not in ["in", "at", "for", "is", "are", "?"]:  # Include city name with multiple words
                        location += " " + words[i+2]
            return "weather", location
        elif any(word in text_lower for word in ["weather", "temperature", "forecast", "rain", "sunny"]):
            return "weather", "current location"
            
        if any(word in text_lower for word in ["help", "assist", "guidance", "support", "can you do"]):
            return "help", None
            
        if any(word in text_lower for word in ["about you", "who are you", "your name", "what are you"]):
            return "about", None
            
        if any(word in text_lower for word in ["music", "song", "playlist", "artist", "band", "listen"]):
            return "music", None
            
        if any(word in text_lower for word in ["movie", "film", "watch", "cinema", "tv show", "series"]):
            return "movies", None
            
        if any(word in text_lower for word in ["food", "eat", "restaurant", "cuisine", "dish", "recipe"]):
            return "food", None
            
        if any(word in text_lower for word in ["news", "headlines", "current events", "latest"]):
            # Extract topic
            topic = "general"
            if "technology" in text_lower or "tech" in text_lower:
                topic = "technology"
            elif "science" in text_lower:
                topic = "science"
            elif "sports" in text_lower:
                topic = "sports"
            elif "business" in text_lower or "finance" in text_lower:
                topic = "business"
            elif "health" in text_lower or "medical" in text_lower:
                topic = "health"
            return "news", topic
            
        if "calculate" in text_lower or any(op in text_lower for op in ["+", "-", "*", "/", "plus", "minus", "times", "divided"]):
            return "calculator", text
            
        if "tell me about" in text_lower or "search for" in text_lower or "look up" in text_lower:
            query = text_lower.replace("tell me about", "").replace("search for", "").replace("look up", "").strip()
            return "web_search", query
            
        # Check for questions
        if any(word in text_lower for word in ["what", "who", "when", "where", "why", "how", "is", "are", "can", "could", "would", "should"]):
            return "question", text
            
        # Default to unknown intent
        return "unknown", None
    
    def calculate(self, expression):
        """Enhanced calculator function"""
        # Replace words with symbols
        expression = expression.lower()
        expression = re.sub(r'plus|add', '+', expression)
        expression = re.sub(r'minus|subtract', '-', expression)
        expression = re.sub(r'times|multiply by', '*', expression)
        expression = re.sub(r'divided by|divide', '/', expression)
        expression = re.sub(r'squared', '**2', expression)
        expression = re.sub(r'cubed', '**3', expression)
        expression = re.sub(r'square root of', 'math.sqrt(', expression)
        if 'math.sqrt(' in expression and not ')' in expression:
            expression += ')'  # Close the square root parenthesis
        
        # Extract numbers and operators
        numbers = re.findall(r'\d+\.?\d*', expression)
        operators = re.findall(r'[\+\-\*\/\(\)\^]', expression)
        
        if len(numbers) < 1:
            return "I need at least one number to perform a calculation."
            
        try:
            # Try to evaluate the expression safely
            # First, extract just the math expression
            math_expr = ''
            for char in expression:
                if char.isdigit() or char in '+-*/().^ ':
                    math_expr += char
                    
            # Replace ^ with ** for exponentiation
            math_expr = math_expr.replace('^', '**')
            
            # Evaluate the expression
            result = eval(math_expr, {"__builtins__": {}}, {"math": math})
            
            # Format the result
            if isinstance(result, int) or result.is_integer():
                return f"The result is {int(result)}"
            else:
                return f"The result is {result:.2f}"
        except Exception as e:
            # Try the simpler approach if the above fails
            try:
                result = float(numbers[0])
                for i in range(min(len(operators), len(numbers) - 1)):
                    if operators[i] == '+':
                        result += float(numbers[i + 1])
                    elif operators[i] == '-':
                        result -= float(numbers[i + 1])
                    elif operators[i] == '*':
                        result *= float(numbers[i + 1])
                    elif operators[i] == '/':
                        result /= float(numbers[i + 1])
                
                # Format the result
                if result.is_integer():
                    return f"The result is {int(result)}"
                else:
                    return f"The result is {result:.2f}"
            except:
                return "I couldn't perform that calculation. Please check your input."
    
    def answer_question(self, question):
        """Enhanced question answering based on keywords"""
        question_lower = question.lower()
        
        # Add the question to history
        self.conversation_history.append(question)
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        # Common questions and answers
        qa_pairs = {
            "your name": "I'm SNEAI, your local AI assistant.",
            "you do": "I'm a local AI assistant designed to help with simple tasks, answer questions, and provide information without requiring internet access.",
            "your purpose": "My purpose is to assist you with information, answer questions, and provide entertainment through jokes and facts, all without needing an internet connection.",
            "created you": "I was created as a local AI assistant that doesn't require external API calls.",
            "made you": "I was developed as a local AI assistant that works offline without external API dependencies.",
            "how old": "I don't have an age in the traditional sense. I'm a software program designed to assist you.",
            "your favorite": "As an AI, I don't have personal preferences, but I'm programmed to be helpful and informative!",
            "you like": "As an AI, I don't have personal preferences, but I'm here to assist you with whatever you need!",
            "you think": "I process information based on patterns and rules, but I don't 'think' in the human sense. I'm designed to be helpful!",
            "you feel": "I don't experience emotions, but I'm programmed to provide helpful and friendly responses.",
            "you live": "I exist as a software program running on your device. I don't have a physical existence or location.",
            "meaning of life": "The meaning of life is a philosophical question that has different answers for different people. Some say it's 42!",
            "how are you": "I'm functioning well and ready to assist you! How can I help today?",
            "your creator": "I was created as a local AI assistant that works offline.",
            "you real": "I'm a real AI program, though I don't have consciousness or feelings like humans do.",
            "you human": "No, I'm an AI assistant designed to help you with various tasks and questions.",
            "you learn": "I can learn new responses when you teach me using the 'Teach SNEAI' feature.",
            "current year": f"The current year is {datetime.datetime.now().year}.",
            "current month": f"The current month is {datetime.datetime.now().strftime('%B')}.",
            "current day": f"Today is {datetime.datetime.now().strftime('%A')}.",
            "capital of": "I have limited knowledge about geography. You can teach me about specific capitals using the 'Teach SNEAI' feature.",
            "president of": "I have limited knowledge about current political leaders. You can teach me specific information using the 'Teach SNEAI' feature.",
            "population of": "I don't have access to current population statistics. You can teach me specific population facts using the 'Teach SNEAI' feature.",
            "distance between": "I don't have access to geographical distance information. You can teach me specific distances using the 'Teach SNEAI' feature.",
            "how to cook": "I don't have specific cooking instructions, but generally, cooking involves preparing ingredients and applying heat. You can teach me specific recipes using the 'Teach SNEAI' feature.",
            "how to make": "I don't have specific instructions for making things, but you can teach me using the 'Teach SNEAI' feature.",
            "how to fix": "I don't have specific repair instructions, but you can teach me using the 'Teach SNEAI' feature.",
            "best way to": "The best approach often depends on your specific situation. You can teach me specific advice using the 'Teach SNEAI' feature.",
            "difference between": "I don't have specific comparative information, but you can teach me using the 'Teach SNEAI' feature."
        }
        
        # Check for matches in our QA pairs
        for key, answer in qa_pairs.items():
            if key in question_lower:
                return answer
        
        # Try to find relevant information from previous conversation
        tokens = self.tokenize(question)
        for prev_question in reversed(self.conversation_history[:-1]):  # Exclude current question
            prev_tokens = self.tokenize(prev_question)
            common_tokens = set(tokens) & set(prev_tokens)
            if len(common_tokens) > 2:  # If there are common keywords
                return "Based on our previous conversation, I think this relates to " + prev_question
        
        # If we can't find a specific answer, try to give a helpful response based on keywords
        if "how" in question_lower and "you" in question_lower:
            return "I'm doing well! I'm here to help you with information and answer your questions."
            
        if "what" in question_lower and "you" in question_lower and "do" in question_lower:
            return "I can answer questions, tell jokes and facts, provide time and date information, perform simple calculations, and learn from our interactions."
            
        if "who" in question_lower and "you" in question_lower:
            return "I'm SNEAI, a local AI assistant designed to work without requiring external API calls."
        
        return random.choice(self.knowledge_base["unknown"])
    
    def add_custom_response(self, pattern, response):
        """Add a custom response pattern"""
        self.custom_responses[pattern] = response
        try:
            with open("custom_responses.json", "w") as f:
                json.dump(self.custom_responses, f)
            return True
        except:
            return False
    
    def process(self, text):
        """Process user input and generate a response"""
        if not text or text.strip() == "":
            return "I didn't catch that. Could you please say something?"
            
        intent, data = self.get_intent(text)
        
        if intent == "greeting":
            return random.choice(self.knowledge_base["greeting"])
            
        elif intent == "farewell":
            return random.choice(self.knowledge_base["farewell"])
            
        elif intent == "thanks":
            return random.choice(self.knowledge_base["thanks"])
            
        elif intent == "jokes":
            return random.choice(self.knowledge_base["jokes"])
            
        elif intent == "facts":
            return random.choice(self.knowledge_base["facts"])
            
        elif intent == "time":
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
            
        elif intent == "date":
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
            
        elif intent == "weather":
            if data and data != "current location":
                weather_info = get_weather(data)
                if weather_info:
                    return f"Weather in {data}: {weather_info}"
                else:
                    return f"I couldn't get the weather for {data}. Please try again later."
            else:
                return "Please specify a location for the weather forecast. For example, 'What's the weather in New York?'"
            
        elif intent == "help":
            return random.choice(self.knowledge_base["help"])
            
        elif intent == "about":
            return random.choice(self.knowledge_base["about"])
            
        elif intent == "music":
            return random.choice(self.knowledge_base["music"])
            
        elif intent == "movies":
            return random.choice(self.knowledge_base["movies"])
            
        elif intent == "food":
            return random.choice(self.knowledge_base["food"])
            
        elif intent == "news":
            news_items = get_news(data, 3)
            if news_items:
                response = f"Here are the latest {data} headlines:\n\n"
                for i, item in enumerate(news_items):
                    response += f"{i+1}. {item['title']}\n{item.get('description', '')}\n\n"
                return response
            else:
                return f"I couldn't fetch the latest news. Please try again later."
            
        elif intent == "calculator":
            return self.calculate(data)
            
        elif intent == "web_search":
            # Start a thread to search the web
            result = search_and_summarize(data)
            if result:
                return result
            else:
                return f"I searched for information about '{data}' but couldn't find relevant results."
            
        elif intent == "question":
            # First try to answer from our knowledge base
            local_answer = self.answer_question(data)
            
            # If we don't have a specific answer, search the web
            if local_answer in self.knowledge_base["unknown"]:
                web_result = search_and_summarize(data)
                if web_result:
                    return web_result
                else:
                    return local_answer
            else:
                return local_answer
            
        elif intent == "custom":
            return self.custom_responses[data]
            
        else:
            # For unknown intents, try web search as a fallback
            web_result = search_and_summarize(text)
            if web_result:
                return web_result
            else:
                return random.choice(self.knowledge_base["unknown"])

# For teaching the AI new responses
def teach_ai(ai_engine, pattern, response):
    success = ai_engine.add_custom_response(pattern, response)
    if success:
        return f"I've learned to respond to '{pattern}' with '{response}'."
    else:
        return "I couldn't save that response. Please try again."