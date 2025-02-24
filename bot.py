import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Load channel config
try:
    with open("channel_config.json", "r") as f:
        CHANNEL_CONFIG = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    CHANNEL_CONFIG = {}

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online: {bot.user.name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setchannel(ctx):
    CHANNEL_CONFIG[str(ctx.guild.id)] = ctx.channel.id
    with open("channel_config.json", "w") as f:
        json.dump(CHANNEL_CONFIG, f)
    await ctx.send(f"✅ Notification channel set to {ctx.channel.mention}!")

@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        guild_id = str(member.guild.id)
        if guild_id in CHANNEL_CONFIG:
            channel = bot.get_channel(CHANNEL_CONFIG[guild_id])
            if channel:
                await channel.send(f"📢 {member.mention} is now in **{after.channel.name}**!")

bot.run(BOT_TOKEN)
