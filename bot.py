import discord
from discord.ext import commands
import random
import asyncio

TOKEN = "MTQ2NzkzMTc4MTM0NDAwMjEwOQ.GZSpeC.D1uv9MGpguAcN2OaAG5WbdUO12_91g-VjNbjUE"
CHANNEL_ID = 1467932891962150982

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
    "I'M NOT ROLEPLAYING",
    "BRO I'M SERIOUS"
]

REJECTED_LINES = [
    "OKAY MAYBE I SHOULDN'T HAVE SAID ANYTHING",
    "YALL DON'T CARE ANYWAY",
    "I'M ACTUALLY STUPID FOR SAYING THIS",
    "WHY DO I EVEN TALK",
    "NEVER MIND BRO",
    "I'M DONE TALKING"
]

CHAOS_LINES = [
    "WHY YALL LAUGHING???",
    "STOP TYPING LMAO",
    "BROOOOO",
    "THIS CHAT IS EVIL",
    "NAH THIS CRAZY"
]

EMOJIS = ["😭", "💀", "😔", "😡"]

def build_message(name):
    lines = []
    lines.append(f"PLS @{name} I NEED THIS")

    for _ in range(random.randint(2, 4)):
        lines.append(random.choice(CORE_LINES))

    # 40% 機率進入「被拒絕後」悲傷模式
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
        print("❌ 找不到頻道，請檢查 CHANNEL_ID")
        return

    while running:
        members = [
            m for m in channel.guild.members
            if not m.bot and m.status != discord.Status.offline
        ]

        if members:
            target = random.choice(members)
            msg = build_message(target.display_name)
            await channel.send(msg)

        wait_minutes = random.randint(1, 4)
        await asyncio.sleep(wait_minutes * 60)

@bot.command()
async def start(ctx):
    global running
    if running:
        await ctx.send("⚠️ 已經在跑了 BRO")
        return

    running = True
    bot.loop.create_task(speed_loop())
    await ctx.send("🔥 SPEED MODE 啟動")

@bot.command()
async def stop(ctx):
    global running
    running = False
    await ctx.send("🛑 SPEED MODE 停止")

@bot.event
async def on_ready():
    print(f"✅ 已登入為 {bot.user}")

bot.run(TOKEN)
