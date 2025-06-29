# === commands/topic.py ===
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

class Topic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def topic(self, ctx):
        prompt = "Generate a funny or hot take topic for a Discord debate."
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.95,
            )
            await ctx.send(f"🧠 Debate Topic: {response.choices[0].message.content.strip()}")
        except Exception as e:
            await ctx.send("❌ No spicy takes today.")
            print(e)

async def setup(bot):
    await bot.add_cog(Topic(bot))
