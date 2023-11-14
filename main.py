"""
    Murad:
    CHECK THE [TODO]: 's!!!!

    VERY IMPORTANT!!!!
"""

# load the token env
load_dotenv()
# Connect to database
db_connect()

# OpenAI GPT-3.5 API key
openai.api_key = "your_openai_api_key"

intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
# client.run(os.getenv('BOT_TOKEN'))