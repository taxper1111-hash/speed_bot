import discord
from discord.ext import commands
import random
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 123456789012345678

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

running = False

CORE_LINES = [
    "MY MOM IS KINDA HOMELESS",
    "I LIVE WITH MY DAD",
    "I JUST WANNA HELP MY MOM",
    "THIS IS REAL LIFE",
    "IM NOT ROLEPLAYING",
    "BRO IM SERIOUS"
]

REJECTED_LINES = [
    "OKAY MAYBE I SHOULDNT HAVE SAID ANYTHING",
    "YALL DONT CARE ANYWAY",
    "IM ACTUALLY STUPID FOR SAYING THIS",
    "WHY DO I EVEN TALK",
    "NEVER MIND BRO",
    "IM DONE TALKING"
]

CHAOS_LINES = [
    "WHY YALL LAUGHING",
    "STOP TYPING LMAO",
    "BROOOOO",
    "THIS CHAT IS EVIL",
    "NAH THIS CRAZY"
]

EMOJIS = ["😭", "💀", "🤡", "😔", "😡"]

def build_message(name):
    lines = []
    lines.append(f"PLS @{name} I NEED THIS")
    for _ in range(random.randint(2, 4)):
        lines.append(random.choice(CORE_LINES))
    if random.random() < 0.4:
        lines.append(random.choice(REJECTED_LINES))
    else:
        lines.append(random.choice(CHAOS_LINES))
    lines.append(random.choice(EMOJIS) * random.randint(2, 5))
    return "\n".join(lines)

async def speed_loop():
    global running
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        return
    while running:
        members = [
            m for m in channel.guild.members
            if not m.bot and m.status != discord.Status.offline
        ]
        if members:
            target = random.choice(members)
            await channel.send(build_message(target.display_name))
        await asyncio.sleep(random.randint(1, 4) * 60)

@bot.command()
async def start(ctx):
    global running
    if running:
        await ctx.send("ALREADY RUNNING BRO")
        return
    running = True
    bot.loop.create_task(speed_loop())
    await ctx.send("SPEED MODE ON")

@bot.command()
async def stop(ctx):
    global running
    running = False
    await ctx.send("SPEED MODE OFF")

@bot.command()
async def ping(ctx):
    await ctx.send("IM ALIVE BRO")

@bot.event
async def on_ready():
    print(f"LOGIN OK {bot.user}")

bot.run(TOKEN)

