# === commands/learn.py ===
from discord.ext import commands

class Learn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def learn(self, ctx):
        await ctx.send("Use `!learn_personality` to analyze server vibe.")

async def setup(bot):
    await bot.add_cog(Learn(bot))
