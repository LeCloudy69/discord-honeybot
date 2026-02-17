import discord
from discord.ext import tasks, commands
from datetime import time
import pytz # This handles timezones so "Noon" is actually Noon for you

# --- CONFIGURATION ---
TOKEN = '' # Was an old exposed hardcoded Token
CHANNEL_ID = 1326298906438668434  # Channel ID (Integer, no quotes)
STICKER_ID = 1424930331752009801  # Sticker ID (Integer, no quotes)
YOUR_TIMEZONE = 'America/New_York' #  timezone


# Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# sets the time to 12:00 PM (Noon) in your timezone
target_time = time(hour=12, minute=0, tzinfo=pytz.timezone(YOUR_TIMEZONE))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    # Start the daily loop if it isn't already running
    if not daily_dog.is_running():
        daily_dog.start()

# This is the loop that runs once a day at the target time
@tasks.loop(time=target_time)
async def daily_dog():
    channel = bot.get_channel(CHANNEL_ID)
    
    # Try to fetch the sticker
    try:
        sticker = await bot.fetch_sticker(STICKER_ID)
        await channel.send(stickers=[sticker])
        print("Dog deployed.")
    except Exception as e:
        print(f"Failed to send sticker: {e}")
        # Fallback if sticker ID is wrong
        await channel.send("It is noon. Imagine a dog here. (Error: Sticker ID invalid)")

# HELPER COMMAND: If you don't know the sticker ID, type !getsticker in chat
# while replying to a message that has the sticker.
@bot.command()
async def getsticker(ctx):
    if ctx.message.reference:
        original_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if original_message.stickers:
            sticker = original_message.stickers[0]
            await ctx.send(f"The ID for sticker '{sticker.name}' is: `{sticker.id}`")
        else:
            await ctx.send("That message doesn't have a sticker!")
    else:
        await ctx.send("Reply to a message with a sticker and use this command.")

@bot.command()
async def testdog(ctx):
    try:
        # Fetch the sticker using the ID you hardcoded at the top
        sticker = await bot.fetch_sticker(STICKER_ID)
        
        # Send the sticker to the channel where you typed the command
        await ctx.send(stickers=[sticker])
        await ctx.send("If you see the sticker above, the ID is correct!")
        
    except Exception as e:
        # This will tell you exactly what is wrong if it fails
        await ctx.send(f"Test failed. Error: {e}")

bot.run(TOKEN)
