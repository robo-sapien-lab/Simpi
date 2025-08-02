# Simpi Singh - AI-Powered Reddit Bot

Simpi Singh is a multi-user Reddit bot powered by Venice from OpenRouter, designed to provide engaging, personalized interactions with Reddit users.

## Features

- 🧠 Contextual Memory & User Preferences
- 🎭 Dynamic Persona & Tone Adaptation
- 🛡️ Built-in Moderation & Safety Controls
- 📊 Analytics & Performance Tracking
- 🔌 Pluggable Architecture
- ⚡ Async Operation with Rate Limiting

## Setup

1. Clone the repository:
```bash
git clone https://github.com/robo-sapien-lab/Simpi.git
cd Simpi
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and configure your environment variables:
```bash
cp .env.example .env
```

5. Set up Redis and PostgreSQL databases

6. Start the bot:
```bash
python main.py
```

## Environment Variables

Required environment variables in your `.env` file:

```env
# Reddit API Credentials
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_bot_username
REDDIT_PASSWORD=your_bot_password

# Venice API
VENICE_API_KEY=your_venice_api_key

# Database URLs
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://user:pass@localhost:5432/simpi

# Webhooks (optional)
SLACK_WEBHOOK_URL=your_slack_webhook
DISCORD_WEBHOOK_URL=your_discord_webhook
```

## Plugin Development

To create a new plugin:

1. Create a new Python file in the `plugins/` directory
2. Inherit from `plugins.base.BasePlugin`
3. Implement required methods
4. The plugin will be automatically discovered and loaded

Example plugin:
```python
from plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    name = "my_plugin"
    
    async def handle_message(self, message):
        # Plugin logic here
        pass
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
