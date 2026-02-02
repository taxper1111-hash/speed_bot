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

normal_lines = [
    "MY MOM IS KINDA HOMELESS",
    "I LIVE WITH MY DAD",
    "IM TRYING TO HELP MY MOM",
    "THIS IS REAL LIFE",
    "BRO IM SERIOUS"
]

crazy_lines = [
    "PLS I NEED THIS",
    "STOP TYPING LMAO",
    "IM NOT ROLEPLAYING",
    "NAH THIS CRAZY",
    "BRO PLEASE",
    "THIS IS REAL LIFE",
    "IM SHAKING RN",
    "WHY NOBODY HELPING",
    "IM DEAD SERIOUS",
    "PLEASE BRO PLEASE"
]

@client.event
async def on_ready():
    print("BOT READY")
    client.loop.create_task(loop_task())

async def loop_task():
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
        mention = target.mention
        msg = f"PLS {mention} I NEED THIS\n"
        msg += "I LIVE WITH MY DAD\n"
        msg += "MY MOM IS KINDA HOMELESS\n"
        msg += random.choice(normal_lines)
        await channel.send(msg)

@client.event
async def on_message(message):
    global crazy_mode
    if message.author.bot:
        return

    if message.content.lower() == "!alive":
        await message.channel.send("THIS IS SPEED BOT IM ALIVE")
        return

    if message.content.lower() == "!crazy on":
        crazy_mode = True
        await message.channel.send("CRAZY MODE ON 😭🔥")
        return

    if message.content.lower() == "!crazy off":
        crazy_mode = False
        await message.channel.send("CRAZY MODE OFF 😐")
        return

    if last_target_id and message.author.id == last_target_id:
        if message.content.lower() in ["no", "stop", "shut up", "wtf"]:
            mention = message.author.mention
            spam = f"PLS {mention} I NEED THIS\n"
            spam += "THIS IS REAL LIFE\n"
            spam += "MY MOM IS KINDA HOMELESS\n"
            spam += "BRO IM SERIOUS\n"
            spam += random.choice(crazy_lines)
            await message.channel.send(spam)

client.run(TOKEN)



