import discord
import asyncio
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

crazy_mode = True
last_target_id = None

base_lines = [
    "MY MOM IS KINDA HOMELESS",
    "I LIVE WITH MY DAD",
    "THIS IS REAL LIFE",
    "BRO IM SERIOUS",
    "IM JUST TRYING TO HELP MY MOM"
]

crazy_lines = [
    "PLS I NEED THIS",
    "STOP TYPING LMAO",
    "IM NOT ROLEPLAYING",
    "NAH THIS CRAZY",
    "BRO PLEASE",
    "WHY NOBODY LISTENING",
    "IM SHAKING RN",
    "PLEASE BRO PLEASE"
]

@client.event
async def on_ready():
    print("SPEED BOT READY")
    client.loop.create_task(crazy_loop())

async def crazy_loop():
    await client.wait_until_ready()
    global last_target_id
    while not client.is_closed():
        await asyncio.sleep(random.randint(60, 240))
        if not crazy_mode:
            continue
        channel = client.get_channel(CHANNEL_ID)
        if channel is None:
            continue
        members = [m for m in channel.guild.members if not m.bot]
        if not members:
            continue
        target = random.choice(members)
        last_target_id = target.id
        msg = (
            f"PLS {target.mention} I NEED THIS\n"
            f"I LIVE WITH MY DAD\n"
            f"MY MOM IS KINDA HOMELESS\n"
            f"{random.choice(base_lines)}"
        )
        await channel.send(msg)

@client.event
async def on_message(message):
    global crazy_mode
    if message.author.bot:
        return

    text = message.content.lower()

    if text == "!alive":
        await message.channel.send("THIS IS SPEED BOT IM ALIVE")
        return

    if text == "!start":
        crazy_mode = True
        await message.channel.send("SPEED MODE ON 🔥😭")
        return

    if text == "!stop":
        crazy_mode = False
        await message.channel.send("SPEED MODE OFF 😐")
        return

    if last_target_id and message.author.id == last_target_id:
        if text in ["no", "stop", "shut up", "wtf"]:
            msg = (
                f"PLS {message.author.mention} I NEED THIS\n"
                f"THIS IS REAL LIFE\n"
                f"MY MOM IS KINDA HOMELESS\n"
                f"BRO IM SERIOUS\n"
                f"{random.choice(crazy_lines)}"
            )
            await message.channel.send(msg)

client.run(TOKEN)

