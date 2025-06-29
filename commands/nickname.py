# === commands/nickname.py ===
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nickname(self, ctx, member):
        prompt = f"Give a funny, unique nickname for {member}."
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=40,
                temperature=0.95,
            )
            await ctx.send(f"🏷️ Nickname idea: {response.choices[0].message.content.strip()}")
        except Exception as e:
            await ctx.send("❌ Nickname engine overloaded.")
            print(e)

async def setup(bot):
    await bot.add_cog(Nickname(bot))
