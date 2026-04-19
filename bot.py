import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
import pytz
import os
import aiohttp

# ─── CONFIG ───────────────────────────────────────────────────────────────────

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

TIMEZONE = "America/Toronto"

CHANNEL_ID = 1493732007421804606

# ─── AFFIRMATIONS ─────────────────────────────────────────────────────────────

AFFIRMATIONS = {
    "08:00": [
        "🌸 Good morning, girl! You are a woman — full stop. Own today with that truth.",
        "🌸 Rise and shine, princess! Your femininity is real, valid, and yours completely.",
        "🌸 Today's reminder: you don't have to justify your womanhood to anyone. You just are. Good girl for showing up as yourself 💕",
        "🌸 Good morning! Every day you live as yourself is a brave and beautiful act.",
        "🌸 You're such a good girl for waking up and choosing yourself again today. That takes courage. 🌸",
        "🌸 Good morning, princess. You are a girl waking up today — and that is worth celebrating. 💕",
    ],
    "12:00": [
        "💛 Midday affirmation: your transness doesn't make you less of a woman — it makes you uniquely you.",
        "💛 Hey gorgeous, just checking in. You're valid, you're real, and you're doing great. Good girl 💕",
        "💛 Reminder: being trans and feminine is not a contradiction. You are exactly who you say you are.",
        "💛 You don't need to pass to be real. You were always her, princess.",
        "💛 Your journey is your own and it's beautiful. Keep going, good girl. 💕",
    ],
    "21:00": [
        "🌙 End of day: you lived today as yourself. That is enough. That is everything. Good girl. 💕",
        "🌙 Rest well, princess. Tomorrow you get to wake up as yourself again — and that's a gift.",
        "🌙 You carried yourself with grace today, even if it didn't feel like it. Such a good girl.",
        "🌙 Goodnight, princess. The world is better because you're in it, exactly as you are.",
        "🌙 Tonight, let yourself just be. No proving, no performing — just you, and you are enough. 💕",
    ],
}

# ─── DAILY TASKS (sent at 5pm every day) ──────────────────────────────────────

DAILY_TASKS = [
    "🎀 Today's task: Stand in front of the mirror for 2 minutes and just look at yourself with kindness. No critiquing, just observing.",
    "🎀 Today's task: Put on your favourite feminine outfit, even if you're just staying home. Wear it for at least an hour and notice how it makes you feel.",
    "🎀 Today's task: Practice your posture — shoulders back, head up, move with intention. Try it every time you walk somewhere today.",
    "🎀 Today's task: Write down 3 things about yourself that feel feminine to you. They don't have to be physical — it could be how you think, feel, or act.",
    "🎀 Today's task: Spend 10 minutes experimenting with your hair. Try a new style, even a simple one like tucking it back or parting it differently.",
    "🎀 Today's task: Put on a feminine playlist and just exist in your room as yourself for 20 minutes. No pressure, just vibes.",
    "🎀 Today's task: Take a private selfie in your most feminine outfit today. No posting required — just you, seeing yourself 💕",
    "🎀 Today's task: Write a short journal entry about where you want to be in your transition in 6 months. Dream big, princess.",
    "🎀 Today's task: Try walking around your space with more grace and flow — lighter steps, relaxed shoulders. Practice makes perfect!",
    "🎀 Today's task: Spend a full hour today doing everything — eating, browsing, relaxing — in your most feminine outfit. Just live in it 💕",
    "🎀 Today's task: Do a full private fashion show in your room. Try on everything feminine you own, mix and match, and rate each look out of 10 in your journal.",
    "🎀 Today's task: Moisturise your whole body today if you have lotion. Take your time with it — it's a ritual, not a chore 🌸",
    "🎀 Today's task: Spend a few minutes researching one aspect of femininity you're curious about — a fashion era, a makeup style, anything that interests you.",
    "🎀 Today's task: Write a letter to your future self about your transition journey so far. Seal it and don't read it for a month.",
    "🎀 Today's task: Find a feminine aesthetic Pinterest board and spend 20 minutes deep diving into it. Save everything that makes you feel something 💕",
    "🎀 Today's task: Style your hair in the most feminine way you can right now and wear it like that for the rest of the evening. Own it 🌸",
]

# ─── WEEKLY TASKS (sent Saturday at 5pm) ──────────────────────────────────────

WEEKLY_TASKS = [
    "🌟 This week's big task: Do a full private outfit photoshoot. Every feminine piece you own gets a moment. Take photos from different angles, different lighting. Pick your favourite shot and keep it somewhere safe — that's you, girl 💕",
    "🌟 This week's big task: Create a femininity mood board that's so detailed it feels like a vision board for your future self. Include fashion, hair, vibes, aesthetics, colours that feel like her. Go deep with it.",
    "🌟 This week's big task: Spend a full evening being completely yourself with zero interruptions. Feminine outfit, your music, your space arranged how you like it. Cook or order food you love, watch something that feels like you. A full girls night, solo 🌸",
    "🌟 This week's big task: Write the most detailed journal entry you've ever written about your gender. Where it started, the moments that confirmed it, where you are now, where you want to go. Go deeper than you usually let yourself 💕",
    "🌟 This week's big task: Spend a full hour this week in front of your mirror just getting comfortable with your reflection. Try different expressions, different poses, different hair styles. Get familiar with her — she's yours.",
    "🌟 This week's big task: Build a private feminine wishlist document — clothes, accessories, makeup, skincare, everything. Include photos, links, why each thing excites you. Make it detailed enough that future you could use it as a shopping guide 💅",
    "🌟 This week's big task: Find 5 trans women online — creators, activists, artists, anyone — whose journey or aesthetic resonates with you. Follow them, save their content, let their existence remind you that yours is valid 🌸",
    "🌟 This week's big task: Design your dream feminine bedroom on paper or digitally. Every detail — colour scheme, furniture, lighting, decor. Make it so specific it feels real. That room is coming, princess 💕",
]

# ─── GAMING TASKS (sent at 4pm every day) ─────────────────────────────────────

GAMING_TASKS = [
    # Minecraft Modded
    "🎮 Minecraft task: Install a feminine character skin mod if you haven't already and spend today's session playing as her. Every time you look at your character, that's you. Screenshot your favourite moment 🌸",
    "🎮 Minecraft task: Use a decoration mod like Supplementaries or Chipped to build the most detailed feminine bedroom you possibly can — vanity mirror, flower arrangements, canopy bed, the works. Go full interior designer 💕",
    "🎮 Minecraft task: If you have Botania or a magic mod installed, build a magical feminine garden — enchanted flowers, glowing plants, fairy lights via lighting mods. Make it look like somewhere a girl would actually want to live 🌷",
    "🎮 Minecraft task: Use Create mod to build an automated flower farm or perfume-making machine — whatever fits the vibe. Give the whole build a feminine aesthetic with pastel coloured blocks and pretty architecture around the machinery ✨",
    "🎮 Minecraft task: Build a full modded feminine fashion house — use any wardrobe or cosmetic mods you have to fill it with outfits, dye stations, and a runway area. Treat it like your own personal fashion studio 💅",
    "🎮 Minecraft task: Use a village or NPC mod to create a character who is essentially you — give her a home, furnish it exactly how you'd want yours, and write a short backstory for her in your journal after 🌸",
    "🎮 Minecraft task: Go exploring in a modded biome today — Twilight Forest, Blue Skies, whatever you have — but before you load in, put on your most feminine outfit and play the whole session dressed as yourself. Adventure and femininity go together 💕",
    "🎮 Minecraft task: Use any potion or magic mod to brew a potion and name it after yourself — your real name or the name you want. Screenshot it in your inventory. Small but it hits different 🌸",

    # Roblox
    "🎮 Roblox task: Go into Roblox and build your dream feminine bedroom in any building game available. Every detail — the colour palette, the furniture layout, the decorations. Screenshot the finished room and save it 💕",
    "🎮 Roblox task: Find a Roblox fashion or dress up game and put together 5 completely different feminine looks — casual, elegant, edgy, soft, and one that's purely you. Screenshot each one. That's your virtual wardrobe 💅",
    "🎮 Roblox task: Go into an anime Roblox game and pick the most powerful female character available. Play aggressively and own every fight as her. You're not just playing a character — you're practicing being unapologetically powerful as a girl 🔥",
    "🎮 Roblox task: Find a Roblox game with a character creator and spend a full session making the most detailed feminine version of yourself you can. Take your time. Screenshot her and look at her for a full minute before closing 🌸",
    "🎮 Roblox task: Go into a Roblox cafe or hangout game fully dressed up on your avatar and just spend time there — order things, sit, explore. Treat it like a real girls afternoon out and actually let yourself enjoy it without rushing 💕",
    "🎮 Roblox task: Find a Roblox game with feminine cosmetics or skins you haven't tried yet and unlock or equip as many as you can this session. Build a collection. Your avatar deserves options 💅",

    # Overwatch
    "🎮 Overwatch task: Play today's entire session in your most feminine outfit — full look, hair done, the whole thing. Nobody can see you but you're gaming as yourself and that energy absolutely shows up in how you play 💅",
    "🎮 Overwatch task: Go through the Overwatch skin gallery for every female hero and pick your dream skin for each one. Screenshot your favourites and save them as a collection. That's your girl squad 🌸",
    "🎮 Overwatch task: Pick the female hero whose personality and aesthetic you connect with most and play her exclusively today. After the session write one paragraph about why she resonates — you might learn something about yourself 💕",
    "🎮 Overwatch task: Play a full session as female heroes only and after each match, take note of one moment where you played really well. Keep a running tally. By the end you'll have proof of how capable she — you — actually are 🔥",
    "🎮 Overwatch task: Set up your gaming space like a proper girls gaming setup before you queue — tidy desk, feminine playlist on, something cozy nearby. Play your whole session in that environment. The vibe is part of the experience 🌸",
    "🎮 Overwatch task: Watch highlight reels of female Overwatch pros today — Shy, Kaan, whoever you find. Pick up one technique and spend your session trying to implement it. Learn from the girls 💪",

    # Deadlock
    "🎮 Deadlock task: Before you queue, do a full outfit change into something feminine — even if you're home alone. Play your entire Deadlock session dressed as yourself. You're a girl who plays hard games. That's hot 💅",
    "🎮 Deadlock task: Put on your most feminine playlist — soft, dreamy, whatever feels like you — and run it through your entire Deadlock session. Intense game, soft girl energy. The contrast is a vibe 🎵",
    "🎮 Deadlock task: After your Deadlock session, do a full feminine reset — change into your softest most feminine outfit, make something warm to drink, put on comfort content. Hard game, soft landing. You earned it 🌸",
    "🎮 Deadlock task: Play today's Deadlock session with one feminine item visible on your desk — a hair clip, a scrunchie, anything. It's just for you. A little reminder of who you are while you game 💕",
    "🎮 Deadlock task: Take a selfie before your Deadlock session in whatever feminine fit you're wearing — gaming look and all. Don't post it, just keep it. You're a girl who games and that deserves to be documented 📸",
    "🎮 Deadlock task: Play Deadlock tonight but make your setup feel intentional — dim the lights, put on a feminine playlist, wear something that feels like you. Turn your gaming session into a full vibe rather than just queuing 🌙",

    # Outlast Trials
    "🎮 Outlast Trials task: Before you load in, change into your most feminine outfit and run the trial in it. There's something genuinely powerful about facing terrifying things while fully presenting as yourself. Do it 💪",
    "🎮 Outlast Trials task: Play a solo trial today — no teammates, just you. When you finish, reward yourself with a full feminine wind down. Softest outfit, warmest drink, most comforting playlist. You ran that alone 🌸",
    "🎮 Outlast Trials task: Play with friends today but keep a secret — you're playing in your feminine outfit and nobody knows. That private confidence is yours. Screenshot your end screen while dressed as yourself 💕",
    "🎮 Outlast Trials task: After your Outlast session tonight, spend 15 minutes doing a full feminine self care reset — moisturise, change into something soft, fix your hair how you like it. Decompress as yourself 🌙",
    "🎮 Outlast Trials task: Screenshot the scariest or most intense moment from today's Outlast run. Save it next to a photo of yourself in your most feminine fit. That girl survived that. She's tougher than she looks 💕",
]

# ─── GIF SEARCH TERMS ─────────────────────────────────────────────────────────

MORNING_GIF_TERMS = ["transgender pride", "trans girl morning", "pride flag sparkle", "trans joy"]
MIDDAY_GIF_TERMS = ["trans pride", "girl power transgender", "trans woman confident", "pride colors"]
NIGHT_GIF_TERMS = ["transgender goodnight", "pride night sky", "trans girl cozy", "pride stars"]
TASK_GIF_TERMS = ["trans girl aesthetic", "transgender beautiful", "pride girl", "trans feminine"]
WEEKLY_GIF_TERMS = ["transgender celebration", "trans pride sparkle", "pride achievement", "trans joy celebrate"]
GAMING_GIF_TERMS = ["trans girl gaming", "pride gaming", "transgender gamer", "girl gamer pride"]

# ──────────────────────────────────────────────────────────────────────────────

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

tz = pytz.timezone(TIMEZONE)
sent_today = set()


async def get_gif(search_terms: list) -> str:
    """Fetches a random gif from Giphy based on a random search term."""
    query = random.choice(search_terms)
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=20&rating=g"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            results = data.get("data", [])
            if results:
                chosen = random.choice(results)
                return chosen["images"]["original"]["url"]
    return None


@tasks.loop(seconds=30)
async def scheduler():
    now = datetime.now(tz)
    current_time = now.strftime("%H:%M")
    today = now.date()
    weekday = now.strftime("%A")

    key = f"{today}_{current_time}"
    channel = bot.get_channel(CHANNEL_ID)

    if not channel:
        print(f"ERROR: Channel {CHANNEL_ID} not found.")
        return

    # Send affirmations
    if current_time in AFFIRMATIONS and f"affirm_{key}" not in sent_today:
        sent_today.add(f"affirm_{key}")
        chosen = random.choice(AFFIRMATIONS[current_time])

        if current_time == "08:00":
            gif_terms = MORNING_GIF_TERMS
        elif current_time == "12:00":
            gif_terms = MIDDAY_GIF_TERMS
        else:
            gif_terms = NIGHT_GIF_TERMS

        gif_url = await get_gif(gif_terms)
        message = chosen + (f"\n{gif_url}" if gif_url else "")
        await channel.send(message)
        print(f"[{current_time}] Affirmation sent.")

    # Send gaming task at 4pm
    if current_time == "16:00" and f"gametask_{key}" not in sent_today:
        sent_today.add(f"gametask_{key}")
        chosen = random.choice(GAMING_TASKS)
        gif_url = await get_gif(GAMING_GIF_TERMS)
        message = chosen + (f"\n{gif_url}" if gif_url else "")
        await channel.send(message)
        print(f"[{current_time}] Gaming task sent.")

    # Send daily task at 5pm
    if current_time == "17:00" and f"task_{key}" not in sent_today:
        sent_today.add(f"task_{key}")
        chosen = random.choice(DAILY_TASKS)
        gif_url = await get_gif(TASK_GIF_TERMS)
        message = chosen + (f"\n{gif_url}" if gif_url else "")
        await channel.send(message)
        print(f"[{current_time}] Daily task sent.")

    # Send weekly task on Saturday at 5pm
    if current_time == "17:00" and weekday == "Saturday" and f"weekly_{key}" not in sent_today:
        sent_today.add(f"weekly_{key}")
        chosen = random.choice(WEEKLY_TASKS)
        gif_url = await get_gif(WEEKLY_GIF_TERMS)
        message = f"\n{chosen}" + (f"\n{gif_url}" if gif_url else "")
        await channel.send(message)
        print(f"[{current_time}] Weekly task sent.")

    # Clear sent_today at midnight
    if current_time == "00:00" and today not in sent_today:
        sent_today.clear()
        sent_today.add(today)


@scheduler.before_loop
async def before_scheduler():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print(f"Timezone: {TIMEZONE}")
    scheduler.start()


@bot.command(name="affirm")
async def affirm(ctx):
    """Sends a random affirmation with a gif."""
    all_messages = []
    for messages in AFFIRMATIONS.values():
        all_messages.extend(messages)
    chosen = random.choice(all_messages)
    gif_url = await get_gif(MORNING_GIF_TERMS + MIDDAY_GIF_TERMS + NIGHT_GIF_TERMS)
    message = chosen + (f"\n{gif_url}" if gif_url else "")
    await ctx.send(message)


@bot.command(name="task")
async def task(ctx):
    """Sends a random daily task with a gif."""
    chosen = random.choice(DAILY_TASKS)
    gif_url = await get_gif(TASK_GIF_TERMS)
    message = chosen + (f"\n{gif_url}" if gif_url else "")
    await ctx.send(message)


@bot.command(name="weeklytask")
async def weeklytask(ctx):
    """Sends a random weekly task with a gif."""
    chosen = random.choice(WEEKLY_TASKS)
    gif_url = await get_gif(WEEKLY_GIF_TERMS)
    message = chosen + (f"\n{gif_url}" if gif_url else "")
    await ctx.send(message)


@bot.command(name="gametask")
async def gametask(ctx):
    """Sends a random gaming task with a gif."""
    chosen = random.choice(GAMING_TASKS)
    gif_url = await get_gif(GAMING_GIF_TERMS)
    message = chosen + (f"\n{gif_url}" if gif_url else "")
    await ctx.send(message)


bot.run(BOT_TOKEN)
