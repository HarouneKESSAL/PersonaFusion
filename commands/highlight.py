# === commands/highlight.py ===
from discord.ext import commands
import discord

class Highlight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def highlight(self, ctx, message_id: int):
        try:
            msg = await ctx.channel.fetch_message(message_id)
            channel = discord.utils.get(ctx.guild.text_channels, name="hall-of-fame")
            if channel:
                await channel.send(f"⭐ Highlighted by {ctx.author.mention}:> {msg.content}\n— {msg.author.mention}")
                await ctx.send("Message immortalized ✨")
            else:
                await ctx.send("No #hall-of-fame channel found.")
        except:
            await ctx.send("Couldn’t fetch that message. Check the ID?")

async def setup(bot):
    await bot.add_cog(Highlight(bot))
