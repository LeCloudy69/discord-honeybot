import discord
from discord.ext import tasks, commands
from datetime import time, datetime
import pytz # This handles timezones so "Noon" is actually Noon for me
import random # so we can random between the different stickers
import asyncio # needed for the sleep timer

# CONFIG
with open("token.txt", "r") as f:
    TOKEN = f.read().strip() #pulling instead of hardcoding for better security
CHANNEL_IDS = [ # Channel ID (Integer, no quotes)
    1326298906438668434, # Goober Central
    1505618899192774726  # Luna's server
]
STICKER_OPTIONS = [
    1424930331752009801, #HoneySmile
    1439690907250069555, #HoneyWhimsy
    1439692662260240497  #HoneyRizz
]
YOUR_TIMEZONE = 'America/New_York' #  timezone


# Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) #all commands start with command_prefix

# sets the time to 12:00 PM (Noon) in your timezone
target_time = time(hour=12, minute=0, tzinfo=pytz.timezone(YOUR_TIMEZONE))

#startup event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    # Start the daily loop if it isn't already running
    if not daily_dog.is_running():
        daily_dog.start()

# This is the loop that runs once a day at the target time
@tasks.loop(minutes=1)
async def daily_dog():
    # Get time
    now = datetime.now(pytz.timezone(YOUR_TIMEZONE))

    # Check if hour is 12:00, no seconds
    if now.hour == 12 and now.minute == 0:

        # Try to fetch the sticker
        random_honey_choice = random.choice(STICKER_OPTIONS) # Pick random Honey
        try:
            sticker = await bot.fetch_sticker(random_honey_choice)


        except Exception as e:
            print(f"Failed to send sticker: {e}")
            return # no sticker, no send

        for channel_id in CHANNEL_IDS:
            channel = bot.get_channel(channel_id)
            if channel is None:
                print(f"Failed to find channel with ID: {channel_id}")
                continue # move to next channel in list
            try:
                # check history for dead channel
                latest_message = [message async for message in channel.history(limit=1)]
                if len(latest_message) > 0 and latest_message[0].author == bot.user:
                    print(f"[{now}] Skipped {channel_id}: Nobody talked.")
                    continue # move to next channel in list

                await channel.send(stickers=[sticker])
                print(f"[{now}] Dog deployed to {channel_id}. ID used: {random_honey_choice}")

            except Exception as e:
                print(f"Failed to send sticker to channel {channel_id}: {e}")
        
        await asyncio.sleep(60) # Sleep for 60 seconds to prevent multiple sends in the same minute

@bot.command()
async def testdog(ctx):
    try:
        # get sticker
        random_honey_choice = random.choice(STICKER_OPTIONS) # Pick random Honey
        sticker = await bot.fetch_sticker(random_honey_choice)

        # Send the sticker to the channel where you typed the command
        await ctx.send(stickers=[sticker])
        await ctx.send("If you see the sticker above, the ID is correct!")

    except Exception as e:
        # This will tell you exactly what is wrong if it fails
        await ctx.send(f"Test failed. Error: {e}")

@bot.event
async def on_message(message):
    #check who sent the message
    if message.author == bot.user:
        return
    msg = message.content
    if msg.lower().startswith("honey"): #can be expanded with multiple if's
        random_honey_choice = random.choice(STICKER_OPTIONS) # Pick random Honey
        sticker = await bot.fetch_sticker(random_honey_choice)
        await message.channel.send("Woof", stickers = [sticker])
    bot.process_commands(message) # check if the message is a command since post honey checking

bot.run(TOKEN)

