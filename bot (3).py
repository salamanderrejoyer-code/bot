import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
import pytz
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────────

BOT_TOKEN = os.getenv("DISCORD_TOKEN")

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
    "🎀 Today's task: Practice a soft, feminine smile in the mirror. Notice how it changes how you carry yourself.",
    "🎀 Today's task: Write a short journal entry about where you want to be in your transition in 6 months. Dream big, princess.",
    "🎀 Today's task: Try walking around your space with more grace and flow — lighter steps, relaxed shoulders. Practice makes perfect!",
    "🎀 Today's task: Pick your favourite feminine outfit and put together a full look — accessories, hair, everything. Even if you don't go anywhere, dress up for yourself.",
    "🎀 Today's task: Look in the mirror and say out loud: 'I am a girl and I am enough.' Say it 5 times and mean it a little more each time. 💕",
    "🎀 Today's task: Moisturise your face and hands today if you have lotion around. Skincare doesn't have to be complicated to be a start!",
    "🎀 Today's task: Spend a few minutes researching one aspect of femininity you're curious about — a fashion era, a makeup style, anything that interests you.",
    "🎀 Today's task: Write a letter to your future self about your transition journey so far. Seal it and don't read it for a month.",
]

# ─── WEEKLY TASKS (sent Saturday at 5pm) ──────────────────────────────────────

WEEKLY_TASKS = [
    "🌟 This week's big task: Do a full outfit photoshoot just for yourself. Try on everything feminine you own, mix and match, and take photos. You don't have to share them — this is just for you to see yourself. 💕",
    "🌟 This week's big task: Create a femininity mood board. Use Pinterest, a journal, or even just saved photos on your phone. Collect images, aesthetics, styles and vibes that feel like the woman you're becoming.",
    "🌟 This week's big task: Spend an evening doing a full self care night — moisturise, do your hair, put on your favourite outfit, light a candle if you have one, and just be a girl in your space for a few hours.",
    "🌟 This week's big task: Write a detailed journal entry about your gender journey — where it started, where you are now, and where you want to go. Be as honest and open with yourself as you can.",
    "🌟 This week's big task: Practice feminine movement for 30 minutes. Look up some videos on feminine posture, walking, and gestures and try them out in front of your mirror. Have fun with it!",
    "🌟 This week's big task: Put together 3 full outfits from what you own that feel the most authentically you. Name each one — like a vibe or aesthetic — and write about how each one makes you feel.",
    "🌟 This week's big task: Make a wishlist of feminine items you'd love to get in the future — clothes, accessories, makeup, skincare. Dream without limits and write down why each thing excites you.",
    "🌟 This week's big task: Spend some time this week connecting with the trans community online — whether that's Reddit, Discord servers, or just reading other girls' stories. You're not alone in this journey. 💕",
]

# ──────────────────────────────────────────────────────────────────────────────

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

tz = pytz.timezone(TIMEZONE)
sent_today = set()


@tasks.loop(seconds=30)
async def scheduler():
    now = datetime.now(tz)
    current_time = now.strftime("%H:%M")
    today = now.date()
    weekday = now.strftime("%A")  # Monday, Tuesday, etc.

    key = f"{today}_{current_time}"
    channel = bot.get_channel(CHANNEL_ID)

    if not channel:
        print(f"ERROR: Channel {CHANNEL_ID} not found.")
        return

    # Send affirmations
    if current_time in AFFIRMATIONS and f"affirm_{key}" not in sent_today:
        sent_today.add(f"affirm_{key}")
        chosen = random.choice(AFFIRMATIONS[current_time])
        await channel.send(chosen)
        print(f"[{current_time}] Affirmation sent.")

    # Send daily task at 5pm
    if current_time == "17:00" and f"task_{key}" not in sent_today:
        sent_today.add(f"task_{key}")
        chosen = random.choice(DAILY_TASKS)
        await channel.send(chosen)
        print(f"[{current_time}] Daily task sent.")

    # Send weekly task on Saturday at 5pm
    if current_time == "17:00" and weekday == "Saturday" and f"weekly_{key}" not in sent_today:
        sent_today.add(f"weekly_{key}")
        chosen = random.choice(WEEKLY_TASKS)
        await channel.send(f"\n{chosen}")
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
    """Sends a random affirmation on demand."""
    all_messages = []
    for messages in AFFIRMATIONS.values():
        all_messages.extend(messages)
    await ctx.send(random.choice(all_messages))


@bot.command(name="task")
async def task(ctx):
    """Sends a random daily task on demand."""
    await ctx.send(random.choice(DAILY_TASKS))


@bot.command(name="weeklytask")
async def weeklytask(ctx):
    """Sends a random weekly task on demand."""
    await ctx.send(random.choice(WEEKLY_TASKS))


bot.run(BOT_TOKEN)
