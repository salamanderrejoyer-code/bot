import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
import pytz
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────────

BOT_TOKEN = os.getenv("DISCORD_TOKEN")

TIMEZONE = "America/Toronto"

# ─── SCHEDULED MESSAGES ───────────────────────────────────────────────────────

SCHEDULED_MESSAGES = {
    "08:00": (1493732007421804606, [
        "🌸 Good morning, girl! You are a woman — full stop. Own today with that truth.",
        "🌸 Rise and shine, princess! Your femininity is real, valid, and yours completely.",
        "🌸 Today's reminder: you don't have to justify your womanhood to anyone. You just are. Good girl for showing up as yourself 💕",
        "🌸 Good morning! Every day you live as yourself is a brave and beautiful act.",
        "🌸 You're such a good girl for waking up and choosing yourself again today. That takes courage. 🌸",
        "🌸 Good morning, princess. You are a girl waking up today — and that is worth celebrating. 💕",
    ]),
    "12:00": (1493732007421804606, [
        "💛 Midday affirmation: your transness doesn't make you less of a woman — it makes you uniquely you.",
        "💛 Hey gorgeous, just checking in. You're valid, you're real, and you're doing great. Good girl 💕",
        "💛 Reminder: being trans and feminine is not a contradiction. You are exactly who you say you are.",
        "💛 You don't need to pass to be real. You were always her, princess.",
        "💛 Your journey is your own and it's beautiful. Keep going, good girl. 💕",
    ]),
    "17:00": (1493732007421804606, [
        "✨ Afternoon reminder: the girl you dreamed of being? That's you. You made it, princess.",
        "✨ You are allowed to take up space as a woman. Fully, unapologetically, always.",
        "✨ Your femininity belongs to you — no one gets to define it but you. Good girl for owning that.",
        "✨ Being yourself in a world that didn't always make room for you takes strength. You have it, princess.",
        "✨ Every version of womanhood is valid — including yours, exactly as it is right now.",
    ]),
    "21:00": (1493732007421804606, [
        "🌙 End of day: you lived today as yourself. That is enough. That is everything. Good girl. 💕",
        "🌙 Rest well, princess. Tomorrow you get to wake up as yourself again — and that's a gift.",
        "🌙 You carried yourself with grace today, even if it didn't feel like it. Such a good girl.",
        "🌙 Goodnight, princess. The world is better because you're in it, exactly as you are.",
        "🌙 Tonight, let yourself just be. No proving, no performing — just you, and you are enough. 💕",
    ]),
}

# ──────────────────────────────────────────────────────────────────────────────

intents = discord.Intents.all()  # Enable all intents including message content
bot = commands.Bot(command_prefix="!", intents=intents)

tz = pytz.timezone(TIMEZONE)
sent_today = set()


@tasks.loop(seconds=30)
async def scheduler():
    now = datetime.now(tz)
    current_time = now.strftime("%H:%M")
    today = now.date()

    key = f"{today}_{current_time}"

    if current_time in SCHEDULED_MESSAGES and key not in sent_today:
        sent_today.add(key)
        channel_id, messages = SCHEDULED_MESSAGES[current_time]

        chosen = random.choice(messages)

        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(chosen)
            print(f"[{current_time}] Sent to #{channel.name}: {chosen}")
        else:
            print(f"[{current_time}] ERROR: Channel {channel_id} not found.")

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
    print(f"Scheduled slots loaded: {len(SCHEDULED_MESSAGES)}")
    scheduler.start()


@bot.command(name="affirm")
async def affirm(ctx):
    """Sends a random affirmation on demand."""
    all_messages = []
    for _, messages in SCHEDULED_MESSAGES.values():
        all_messages.extend(messages)
    await ctx.send(random.choice(all_messages))


@bot.command(name="schedule")
@commands.has_permissions(administrator=True)
async def show_schedule(ctx):
    if not SCHEDULED_MESSAGES:
        await ctx.send("No scheduled messages configured.")
        return

    lines = ["**Scheduled Affirmation Times:**"]
    for time, (channel_id, messages) in sorted(SCHEDULED_MESSAGES.items()):
        channel = bot.get_channel(channel_id)
        ch_name = f"#{channel.name}" if channel else f"Unknown ({channel_id})"
        lines.append(f"- `{time}` → {ch_name} ({len(messages)} possible messages)")

    await ctx.send("\n".join(lines))


@bot.command(name="preview")
@commands.has_permissions(administrator=True)
async def preview_messages(ctx, time: str):
    """Preview all affirmations for a given time slot. Usage: !preview 08:00"""
    if time not in SCHEDULED_MESSAGES:
        await ctx.send(f"No schedule found for `{time}`.")
        return

    _, messages = SCHEDULED_MESSAGES[time]
    lines = [f"**Affirmations for `{time}`:**"]
    for i, msg in enumerate(messages, 1):
        lines.append(f"{i}. {msg}")

    await ctx.send("\n".join(lines))


bot.run(BOT_TOKEN)
