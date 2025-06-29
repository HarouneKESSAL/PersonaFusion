# === commands/aura.py ===
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

class Aura(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def aura(self, ctx, member=None):
        name = member or ctx.author
        prompt = f"Describe the vibe or aura of {name}. Be poetic and clever."
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.9,
            )
            await ctx.send(f"🌈 {response.choices[0].message.content.strip()}")
        except Exception as e:
            await ctx.send("❌ Aura detection failed.")
            print(e)

async def setup(bot):
    await bot.add_cog(Aura(bot))
