# === commands/predict.py ===
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

class Predict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def predict(self, ctx):
        prompt = "Give a sarcastic or funny daily energy prediction."
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.9,
            )
            await ctx.send(f"🔮 {response.choices[0].message.content.strip()}")
        except Exception as e:
            await ctx.send("❌ Couldn’t predict your vibe today.")
            print(e)

async def setup(bot):
    await bot.add_cog(Predict(bot))
