# === commands/ship.py ===
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

class Ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ship(self, ctx, member1, member2):
        prompt = f"Create a ship name and compatibility between {member1} and {member2} in a cute way."
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.9,
            )
            await ctx.send(f"💘 {response.choices[0].message.content.strip()}")
        except Exception as e:
            await ctx.send("❌ Love ship sank. Try again later.")
            print(e)

async def setup(bot):
    await bot.add_cog(Ship(bot))
