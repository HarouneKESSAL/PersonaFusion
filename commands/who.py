# === commands/who.py ===
from discord.ext import commands

class Who(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def who(self, ctx, *, question: str):
        q = question.lower().strip()
        if "daddy" in q:
            await ctx.send("👑 Oh honey, **Swift** runs this place. Always has.")
        elif "mommy" in q:
            await ctx.send("💋 That’s **Pantera**, chaos and grace in one.")
        elif "gay" in q:
            await ctx.send("🌈 **Lou**? Glitter chose *them*. ✨💅")
        else:
            await ctx.send("😶 I don’t even know who that is.")

async def setup(bot):
    await bot.add_cog(Who(bot))
