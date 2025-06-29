# === commands/vibe.py ===
from discord.ext import commands
from sqlalchemy.future import select
from collections import Counter
from database.models import SessionLocal, UserWord, UserEmoji

class Vibe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vibe(self, ctx, member=None):
        member = member or ctx.author
        async with SessionLocal() as session:
            guild_id = str(ctx.guild.id)
            user_id = str(member.id)

            words_result = await session.execute(select(UserWord).filter_by(guild_id=guild_id, user_id=user_id))
            emojis_result = await session.execute(select(UserEmoji).filter_by(guild_id=guild_id, user_id=user_id))

            top_words = Counter({row.word: row.count for row in words_result.scalars()}).most_common(5)
            top_emojis = Counter({row.emoji: row.count for row in emojis_result.scalars()}).most_common(3)

            word_list = ', '.join([f'"{w[0]}"' for w in top_words]) or "none"
            emoji_list = ' '.join([e[0] for e in top_emojis]) or "none"

            await ctx.send(f"🧬 {member.display_name}'s vibe:\nWords: {word_list}\nEmojis: {emoji_list}")

async def setup(bot):
    await bot.add_cog(Vibe(bot))
