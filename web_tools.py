import requests
from bs4 import BeautifulSoup
import wikipedia
import json
import re
import time
import random

# Use html5lib parser instead of lxml
BS4_PARSER = 'html5lib'

# User agent with SNEAI's identity
USER_AGENT = "Mozilla/5.0 (compatible; SNEAI/1.0; +https://github.com/Amangupta210/today_ai_v2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Cache for search results to avoid repeated requests
search_cache = {}
cache_expiry = 3600  # 1 hour

def get_search_results(query, num_results=5):
    """Get search results for a query using DuckDuckGo"""
    # Check cache first
    cache_key = f"search_{query}"
    if cache_key in search_cache and time.time() - search_cache[cache_key]["timestamp"] < cache_expiry:
        return search_cache[cache_key]["results"]
    
    try:
        # Use DuckDuckGo HTML search
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, BS4_PARSER)
            results = []
            
            # Extract search results
            for result in soup.select('.result'):
                title_elem = result.select_one('.result__title')
                snippet_elem = result.select_one('.result__snippet')
                url_elem = result.select_one('.result__url')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text().strip()
                    snippet = snippet_elem.get_text().strip()
                    url = url_elem.get_text().strip() if url_elem else ""
                    
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "url": url
                    })
                    
                    if len(results) >= num_results:
                        break
            
            # Cache the results
            search_cache[cache_key] = {
                "results": results,
                "timestamp": time.time()
            }
            
            return results
        else:
            return []
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_wikipedia_summary(query, sentences=3):
    """Get a summary from Wikipedia"""
    try:
        # Search for Wikipedia articles
        search_results = wikipedia.search(query, results=5)
        
        if not search_results:
            return None
        
        # Try to get the page for the first result
        for result in search_results:
            try:
                page = wikipedia.page(result)
                summary = wikipedia.summary(result, sentences=sentences)
                return {
                    "title": page.title,
                    "summary": summary,
                    "url": page.url
                }
            except wikipedia.exceptions.DisambiguationError as e:
                # Try the first option from disambiguation
                if e.options:
                    try:
                        page = wikipedia.page(e.options[0])
                        summary = wikipedia.summary(e.options[0], sentences=sentences)
                        return {
                            "title": page.title,
                            "summary": summary,
                            "url": page.url
                        }
                    except:
                        continue
            except:
                continue
        
        return None
    except Exception as e:
        print(f"Wikipedia error: {e}")
        return None

def scrape_webpage_content(url):
    """Scrape content from a webpage"""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, BS4_PARSER)
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 1000 characters
            return text[:1000]
        else:
            return None
    except Exception as e:
        print(f"Web scraping error: {e}")
        return None

def get_weather(city):
    """Get weather information for a city"""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w+%p"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except Exception as e:
        print(f"Weather error: {e}")
        return None

def get_news(topic="general", count=3):
    """Get latest news headlines"""
    try:
        # Use a free news API
        url = f"https://newsdata.io/api/1/news?apikey=pub_30049e4f9b3c5c6f3c2c1b8e7c5c8d7c8d7c&q={topic}&language=en&size={count}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                return data["results"]
            else:
                # Fallback to static news if API fails
                return get_static_news(topic, count)
        else:
            return get_static_news(topic, count)
    except Exception as e:
        print(f"News error: {e}")
        return get_static_news(topic, count)

def get_static_news(topic="general", count=3):
    """Fallback static news when API fails"""
    static_news = {
        "general": [
            {"title": "Global Climate Summit Concludes with New Agreements", "description": "World leaders have agreed on new measures to combat climate change."},
            {"title": "Tech Giants Announce Collaboration on AI Ethics", "description": "Major technology companies form coalition to establish ethical AI guidelines."},
            {"title": "Scientists Discover Potential New Treatment for Cancer", "description": "Breakthrough research shows promising results in early clinical trials."}
        ],
        "technology": [
            {"title": "New Smartphone Features Revolutionary Battery Technology", "description": "Latest device claims to offer week-long battery life on a single charge."},
            {"title": "Quantum Computing Breakthrough Announced", "description": "Researchers achieve stable qubit operation at room temperature."},
            {"title": "Major Software Update Brings AI Features to Millions of Devices", "description": "Update includes enhanced privacy controls and performance improvements."}
        ],
        "science": [
            {"title": "Mars Rover Discovers Signs of Ancient Water", "description": "New evidence suggests Mars once had significant surface water."},
            {"title": "Astronomers Identify Potentially Habitable Exoplanet", "description": "Planet orbits within the habitable zone of a nearby star system."},
            {"title": "Genetic Modification Shows Promise in Treating Rare Diseases", "description": "Clinical trials report positive outcomes for previously untreatable conditions."}
        ]
    }
    
    if topic.lower() in static_news:
        return static_news[topic.lower()][:count]
    else:
        return static_news["general"][:count]

def search_and_summarize(query, search_type='auto'):
    """Search for information and summarize results based on user preference"""
    try:
        results = []
        sources = []
        
        # Determine search strategy based on user preference
        if search_type == 'wiki' or search_type == 'auto':
            # Try Wikipedia
            wiki_result = get_wikipedia_summary(query, sentences=3)
            if wiki_result:
                results.append(wiki_result['summary'])
                sources.append(f"Wikipedia: {wiki_result['url']}")
                
                # If user specifically asked for wiki only, return just that
                if search_type == 'wiki':
                    return f"According to Wikipedia:\n\n{wiki_result['summary']}\n\nSource: {wiki_result['url']}"
        
        # Get web search results
        if search_type == 'web' or search_type == 'auto':
            search_results = get_search_results(query, num_results=4)
            if search_results:
                for result in search_results[:3]:
                    results.append(result['snippet'])
                    if result['url']:
                        sources.append(result['url'])
                
                # If user specifically asked for web only, return just that
                if search_type == 'web':
                    combined_info = "Based on web search results:\n\n"
                    for i, result in enumerate(search_results[:3]):
                        combined_info += f"{i+1}. {result['snippet']}\n"
                    if sources:
                        combined_info += "\nSources:\n" + "\n".join(sources[:3])
                    return combined_info
        
        # Combine all results if we have any
        if results:
            combined_info = f"Here's what I found about '{query}':\n\n"
            for i, result in enumerate(results[:4]):
                combined_info += f"{result}\n\n"
            
            if sources:
                combined_info += "Sources:\n" + "\n".join(sources[:3])
            
            return combined_info
        
        return None
    except Exception as e:
        print(f"Error in search_and_summarize: {e}")
        return "I tried to search for information in real-time, but encountered a technical issue. Please try a different query."