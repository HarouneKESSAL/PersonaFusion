# === commands/learn_personality.py ===
from discord.ext import commands
from sqlalchemy.future import select
from database.models import SessionLocal, GuildWord, GuildEmoji, GuildProfile
from collections import Counter
import re
from nltk.corpus import stopwords

class LearnPersonality(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="learn_personality")
    async def learn_personality(self, ctx):
        async with SessionLocal() as session:
            guild_id = str(ctx.guild.id)
            result = await session.execute(select(GuildWord).filter_by(guild_id=guild_id))
            word_counts = {row.word: row.count for row in result.scalars()}
            emoji_result = await session.execute(select(GuildEmoji).filter_by(guild_id=guild_id))
            emoji_counts = {row.emoji: row.count for row in emoji_result.scalars()}

            try:
                stop_words = set(stopwords.words('english'))
            except:
                import nltk
                nltk.download('stopwords')
                stop_words = set(stopwords.words('english'))

            filtered_words = {w: c for w, c in word_counts.items() if w.isalpha() and len(w) > 2 and w not in stop_words}
            top_words = Counter(filtered_words).most_common(5)
            word_list = ', '.join([f'"{w[0]}"' for w in top_words]) if top_words else "not enough data"

            emoji_mood_map = {
                "😂": "Meme Chaos", "❤️": "Wholesome Vibes", "🔥": "Hype Squad",
                "💀": "Dark Academia", "😈": "Sassy Energy", "🌸": "Cute & Chill"
            }
            top_emojis = Counter(emoji_counts).most_common(3)
            mood = next((emoji_mood_map.get(e[0]) for e in top_emojis if e[0] in emoji_mood_map), "Mysterious")
            emoji_list = ' '.join([e[0] for e in top_emojis]) or "none"

            summary = f"✨ This server gives off strong vibes of: {word_list}\n🔥 Emoji energy: {emoji_list} — Mood: **{mood}**"
            gp = (await session.execute(select(GuildProfile).filter_by(guild_id=guild_id))).scalar()
            if gp: gp.summary = summary
            else: session.add(GuildProfile(guild_id=guild_id, summary=summary))
            await session.commit()
            await ctx.send(f"🧠 Personality learned!\n{summary}")

async def setup(bot):
    await bot.add_cog(LearnPersonality(bot))
