import discord
from discord.ext import commands
import json
import os
from collections import Counter
import re
import emoji
from openai import OpenAI
from dotenv import load_dotenv

# Load .env with your OpenRouter key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = "server_profiles.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_profiles():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_profiles(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

word_pattern = re.compile(r"\b\w+\b")
def clean_message(message):
    return re.sub(r"http\S+|<@\S+>", "", message.lower())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    profiles = load_profiles()
    guild_id = str(message.guild.id)

    content = clean_message(message.content)
    words = word_pattern.findall(content)

    # Emojis
    unicode_emojis = [char for char in content if emoji.is_emoji(char)]
    custom_emojis = re.findall(r"<a?:\w+:\d+>", message.content)
    emojis = unicode_emojis + custom_emojis

    if guild_id not in profiles:
        profiles[guild_id] = {
            "word_counts": {},
            "emoji_counts": {},
            "summary": "No profile yet."
        }

    for word in words:
        profiles[guild_id]["word_counts"][word] = profiles[guild_id]["word_counts"].get(word, 0) + 1
    for e in emojis:
        profiles[guild_id]["emoji_counts"][e] = profiles[guild_id]["emoji_counts"].get(e, 0) + 1

    save_profiles(profiles)
    await bot.process_commands(message)

@bot.command()
async def learn_personality(ctx):
    from nltk.corpus import stopwords
    import string

    profiles = load_profiles()
    guild_id = str(ctx.guild.id)

    if guild_id not in profiles:
        await ctx.send("Not enough data yet.")
        return

    word_counts = profiles[guild_id]["word_counts"]
    emoji_counts = profiles[guild_id]["emoji_counts"]

    # 1. Filter stopwords
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        import nltk
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))

    filtered_words = {
        w: c for w, c in word_counts.items()
        if w.isalpha() and len(w) > 2 and w.lower() not in stop_words
    }

    top_words = Counter(filtered_words).most_common(5)
    word_list = ', '.join([f'"{w[0]}"' for w in top_words]) if top_words else "not enough unique words"

    # 2. Format emojis
    def format_emoji(e):
        if e.startswith("<:") or e.startswith("<a:"):
            name = re.findall(r":(\w+):", e)
            return f":{name[0]}:" if name else "[custom emoji]"
        return e

    top_emojis = Counter(emoji_counts).most_common(3)
    emoji_list = ' '.join([format_emoji(e[0]) for e in top_emojis]) if top_emojis else "none yet"

    # 3. Mood detection based on top emojis
    emoji_mood_map = {
        "😂": "Meme Chaos",
        "🤣": "Total Madness",
        "❤️": "Wholesome Vibes",
        "🔥": "Hype Squad",
        "💀": "Dark Academia",
        "😈": "Sassy Energy",
        "🌸": "Cute & Chill",
        "😎": "Cool & Unbothered"
    }
    detected_moods = [emoji_mood_map.get(e[0], None) for e in top_emojis if e[0] in emoji_mood_map]
    mood = detected_moods[0] if detected_moods else "Mysterious Vibe"

    # 4. Top active members
    member_counts = {}
    async for msg in ctx.channel.history(limit=1000):
        if not msg.author.bot:
            member_counts[msg.author] = member_counts.get(msg.author, 0) + 1

    top_members = sorted(member_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tags = ', '.join([member.mention for member, _ in top_members]) if top_members else "no active users"

    # 5. Final summary
    summary = f"✨ This server gives off strong vibes of: {word_list}\n"
    summary += f"🔥 Emoji energy: {emoji_list} — Mood: **{mood}**\n"
    summary += f"🏆 Most active legends: {top_tags}"

    profiles[guild_id]["summary"] = summary
    save_profiles(profiles)

    await ctx.send(f"🧠 Personality learned!\n{summary}")

    from nltk.corpus import stopwords
    import string

    profiles = load_profiles()
    guild_id = str(ctx.guild.id)

    if guild_id not in profiles:
        await ctx.send("Not enough data yet.")
        return

    word_counts = profiles[guild_id]["word_counts"]
    emoji_counts = profiles[guild_id]["emoji_counts"]

    # English stopwords
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        import nltk
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))

    # Clean and filter words
    filtered_words = {
        w: c for w, c in word_counts.items()
        if w.isalpha() and len(w) > 2 and w.lower() not in stop_words
    }

    top_words = Counter(filtered_words).most_common(5)
    top_emojis = Counter(emoji_counts).most_common(3)

    if top_words:
        word_list = ', '.join([f'"{w[0]}"' for w in top_words])
    else:
        word_list = "not enough unique words"

    # Format emojis: custom or unicode
    def format_emoji(e):
        if e.startswith("<:") or e.startswith("<a:"):
            name = re.findall(r":(\w+):", e)
            return f":{name[0]}:" if name else "[custom emoji]"
        return e  # unicode emoji like 😎

    emoji_list = ' '.join([format_emoji(e[0]) for e in top_emojis]) if top_emojis else "none yet"

    summary = f"✨ This server gives off strong vibes of: {word_list}\n"
    summary += f"🔥 Emoji energy: {emoji_list}"

    profiles[guild_id]["summary"] = summary
    save_profiles(profiles)

    await ctx.send(f"🧠 Personality learned!\n{summary}")

    profiles = load_profiles()
    guild_id = str(ctx.guild.id)

    if guild_id not in profiles:
        await ctx.send("Not enough data yet.")
        return

    word_counts = profiles[guild_id]["word_counts"]
    emoji_counts = profiles[guild_id]["emoji_counts"]

    # Clean and filter words
    filtered_words = {
        w: c for w, c in word_counts.items()
        if w.isalpha() and len(w) > 2 and c > 2  # avoid IDs, links, short fillers
    }

    top_words = Counter(filtered_words).most_common(5)
    top_emojis = Counter(emoji_counts).most_common(3)

    if top_words:
        word_list = ', '.join([f'"{w[0]}"' for w in top_words])
    else:
        word_list = "not enough data"

    emoji_list = ' '.join([e[0] for e in top_emojis]) if top_emojis else "none yet"

    summary = f"✨ This server gives off strong vibes of: {word_list}\n"
    summary += f"🔥 Emoji energy: {emoji_list}"

    profiles[guild_id]["summary"] = summary
    save_profiles(profiles)

    await ctx.send(f"🧠 Personality learned!\n{summary}")


@bot.command()
async def personality(ctx):
    profiles = load_profiles()
    guild_id = str(ctx.guild.id)
    if guild_id in profiles:
        await ctx.send(f"🧠 Personality: {profiles[guild_id].get('summary', 'No personality learned yet.')}")
    else:
        await ctx.send("No personality data found for this server.")
async def get_last_message_of(ctx, member):
    async for msg in ctx.channel.history(limit=100):
        if msg.author == member and not msg.content.startswith('!'):
            return msg
    return None

async def get_last_message_of(ctx, member):
    async for msg in ctx.channel.history(limit=100):
        if msg.author == member and not msg.content.startswith('!'):
            return msg
    return None

@bot.command()
async def rewrite(ctx, member: discord.Member):
    message = await get_last_message_of(ctx, member)
    if not message:
        await ctx.send("Couldn’t find anything to rewrite.")
        return

    style = re.search(r'genz|shakespeare|pirate', ctx.message.content.lower())
    style = style.group(0) if style else "Shakespearean"

    prompt = f"Rewrite this message in {style} style:\n\n'{message.content}'"

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.8,
        )
        await ctx.send(response.choices[0].message.content.strip())
    except Exception as e:
        await ctx.send("❌ Failed to rewrite.")
        print(e)

@bot.command()
async def predict(ctx):
    prompt = "Give a creative, sarcastic or funny daily energy prediction for a Discord user."
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

@bot.command()
async def burn(ctx, member: discord.Member):
    prompt = f"Roast {member.display_name} in a funny, clever and safe-for-Discord way."
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.9,
        )
        await ctx.send(f"🔥 {response.choices[0].message.content.strip()}")
    except Exception as e:
        await ctx.send("❌ Roast failed. {member.display_name} is unroastable (for now).")
        print(e)

@bot.command()
async def compliment(ctx, member: discord.Member):
    prompt = f"Give a creative, poetic and funny compliment for someone named {member.display_name}."
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.85,
        )
        await ctx.send(f"💖 {response.choices[0].message.content.strip()}")
    except Exception as e:
        await ctx.send("❌ Compliment generator broke. That’s awkward.")
        print(e)

@bot.command()
async def topic(ctx):
    prompt = "Generate a funny or hot take topic for a Discord debate."
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.95,
        )
        await ctx.send(f"🧠 Debate Topic: {response.choices[0].message.content.strip()}")
    except Exception as e:
        await ctx.send("❌ No spicy takes today.")
        print(e)

@bot.command()
async def aura(ctx, member: discord.Member = None):
    member = member or ctx.author
    prompt = f"Describe the vibe, aura, or energy of a Discord user named {member.display_name}. Be poetic, clever, and imaginative."
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

@bot.command()
async def nickname(ctx, member: discord.Member = None):
    member = member or ctx.author
    prompt = f"Give a funny, unique or ironic nickname for a Discord user named {member.display_name}."
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=40,
            temperature=0.95,
        )
        await ctx.send(f"🏷️ New nickname idea: {response.choices[0].message.content.strip()}")
    except Exception as e:
        await ctx.send("❌ Nickname engine overloaded.")
        print(e)

@bot.command()
async def ship(ctx, member1: discord.Member, member2: discord.Member):
    prompt = f"Create a couple name (ship name) and compatibility analysis between {member1.display_name} and {member2.display_name} in a funny or cute way."
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.9,
        )
        await ctx.send(f"💘 {response.choices[0].message.content.strip()}")
    except Exception as e:
        await ctx.send("❌ Love ship sank. Try again later.")
        print(e)

@bot.command()
async def highlight(ctx, message_id: int):
    try:
        msg = await ctx.channel.fetch_message(message_id)
        channel = discord.utils.get(ctx.guild.text_channels, name="hall-of-fame")
        if channel:
            await channel.send(f"⭐ Highlighted by {ctx.author.mention}:\n> {msg.content}\n— {msg.author.mention}")
            await ctx.send("Message immortalized ✨")
        else:
            await ctx.send("No #hall-of-fame channel found.")
    except:
        await ctx.send("Couldn’t fetch that message. Check the ID?")

@bot.command()
async def vibechart(ctx):
    from collections import Counter
    profiles = load_profiles()
    guild_id = str(ctx.guild.id)
    if guild_id not in profiles:
        await ctx.send("No personality data yet. Use !learn_all first.")
        return

    emoji_counts = profiles[guild_id].get("emoji_counts", {})
    top_emojis = Counter(emoji_counts).most_common(5)
    chart = "\n".join([f"{e[0]} : {e[1]}x" for e in top_emojis])
    await ctx.send(f"📊 Top Emoji Energy This Server Radiates:\n{chart if chart else 'none yet'}")

@bot.command()
async def talk(ctx, *, user_message):
    profiles = load_profiles()
    guild_id = str(ctx.guild.id)
    summary = profiles.get(guild_id, {}).get("summary", "No personality summary available.")

    prompt = f"""
You are a Discord bot with the personality described below:

{summary}

Respond to the user message in a matching tone, casually and naturally.

User: {user_message}
Bot:
"""

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",  # or openai/gpt-3.5-turbo if available
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.8,
        )
        reply = response.choices[0].message.content.strip()
        await ctx.send(reply)

    except Exception as e:
        await ctx.send("⚠️ Failed to generate reply.")
        print(f"OpenRouter error: {e}")


@bot.command()
async def who(ctx, *, question: str):
    question = question.lower().strip()

    if "daddy" in question:
        await ctx.send("👑 Oh honey, **Swift** runs this place. Always has, always will. Period.")
    elif "mommy" in question:
        await ctx.send("💋 That’s **Pantera**, the one who raised chaos and grace at the same damn time.")
    elif "gay" in question:
        await ctx.send("🌈 **Lou**? Baby, Lou didn’t choose the gay life — the glitter chose *them* ✨💅")
    else:
        await ctx.send("😶 Girl... I don’t even know who that is. Try again, but make it spicy.")

@bot.command()
async def learn_all(ctx, limit: int = 1000):
    await ctx.send(f"📚 Scanning the last {limit} messages in this channel...")

    profiles = load_profiles()
    guild_id = str(ctx.guild.id)

    if guild_id not in profiles:
        profiles[guild_id] = {
            "word_counts": {},
            "emoji_counts": {},
            "summary": "No profile yet."
        }

    word_counts = profiles[guild_id]["word_counts"]
    emoji_counts = profiles[guild_id]["emoji_counts"]

    word_pattern = re.compile(r"\b\w+\b")

    async for message in ctx.channel.history(limit=limit):
        if message.author.bot:
            continue

        content = clean_message(message.content)
        words = word_pattern.findall(content)

        unicode_emojis = [char for char in content if emoji.is_emoji(char)]
        custom_emojis = re.findall(r"<a?:\w+:\d+>", message.content)
        emojis = unicode_emojis + custom_emojis

        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        for e in emojis:
            emoji_counts[e] = emoji_counts.get(e, 0) + 1

    save_profiles(profiles)
    await ctx.send("✅ Done! Learned from the past. You can now use `!learn_personality`.")


bot.run("DISCORD_TOKEN")
