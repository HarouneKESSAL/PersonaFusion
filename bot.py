# Directory structure:
# persona_fusion/
# ├── bot.py
# ├── database/
# │   ├── __init__.py
# │   ├── models.py
# │   └── init_db.py
# ├── commands/
# │   ├── __init__.py
# │   ├── learn.py
# │   ├── vibe.py
# │   ├── talk.py
# │   ├── burn.py
# │   ├── compliment.py
# │   ├── topic.py
# │   ├── nickname.py
# │   └── ship.py
# ├── utils/
# │   ├── __init__.py
# │   ├── personality.py
# │   └── logger.py

# === 1. bot.py ===
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")

async def load_extensions():
    commands_dir = "commands"
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"{commands_dir}.{filename[:-3]}")
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")
TOKEN = os.getenv("DISCORD_TOKEN")
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())

