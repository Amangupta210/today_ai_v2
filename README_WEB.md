# SNEAI Assistant (Web Version)

SNEAI Assistant is an AI assistant that works with minimal API usage, providing intelligent responses by combining local processing with selective web scraping. This is the web version of the application.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Features

- **Minimal API Usage**: Uses web scraping instead of expensive AI APIs
- **Web Search**: Searches the internet for information to answer questions
- **Weather Information**: Provides weather forecasts for locations worldwide
- **News Headlines**: Delivers the latest news on various topics
- **Modern UI/UX**: Clean, responsive design with dark mode support
- **Voice Recognition**: Speak to your assistant using your browser's microphone
- **Text-to-Speech**: Listen to responses through speech synthesis
- **Teachable**: Train the assistant with custom responses
- **Dark/Light Mode**: Toggle between dark and light themes
- **Chat History**: Conversations are saved between sessions
- **Enhanced Calculator**: Perform basic and advanced math operations
- **Quick Actions**: Access common functions with a single click

## Project Structure

```
sneai-assistant/
├── app.py                # Main Flask application
├── local_ai_engine.py    # Local AI engine
├── Procfile              # For web service configuration
├── requirements.txt      # Dependencies
├── static/               # Static assets
│   └── style.css         # CSS styling
└── templates/            # HTML templates
    └── index.html        # Web interface
```

## Local Development

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Flask application:

```bash
python app.py
```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## Deployment

For detailed deployment instructions to Render, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).

## How It Works

SNEAI uses a rule-based system with pattern matching to understand user queries. It includes:

- Intent recognition for identifying the purpose of messages
- Natural language processing for understanding questions
- Pattern matching for identifying keywords and topics
- Custom response learning for personalization
- Conversation memory for contextual awareness

## License

This project is licensed under the MIT License.

## Credits

Created by Aman Gupta (2025)