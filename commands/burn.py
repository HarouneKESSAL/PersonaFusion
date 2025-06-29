# === commands/burn.py ===
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

class Burn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def burn(self, ctx, member):
        prompt = f"Roast {member} in a clever and funny way."
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.9,
            )
            await ctx.send(f"🔥 {response.choices[0].message.content.strip()}")
        except Exception as e:
            await ctx.send("❌ Roast failed.")
            print(e)

async def setup(bot):
    await bot.add_cog(Burn(bot))
