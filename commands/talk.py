# === commands/talk.py ===
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def talk(self, ctx, *, user_message):
        summary = "This is a sample personality summary."  # Ideally fetched from DB
        prompt = f"""
        You are a Discord bot with this personality:
        {summary}
        Respond naturally to the following:
        User: {user_message}
        Bot:
        """
        try:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8,
            )
            await ctx.send(response.choices[0].message.content.strip())
        except Exception as e:
            await ctx.send("⚠️ Failed to generate reply.")
            print(e)

async def setup(bot):
    await bot.add_cog(Talk(bot))
