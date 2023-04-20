import os

import openai
import nest_asyncio
import json

from lib.key_store import KeyValueStore

# Apply the nest_asyncio fix for Jupyter Notebook
nest_asyncio.apply()

# Load API keys
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up OpenAI API client
openai.api_key = OPENAI_API_KEY

# Set up the key-value store
store = KeyValueStore('store.pkl')