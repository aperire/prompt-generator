import discord
import ai
from dotenv import load_dotenv
from asyncer import asyncify
import os

load_dotenv()

async def send_message(message, user_msg):
    print("this?")
    try:
        response = await asyncify(ai.process)(user_msg)
        await message.channel.send(response)
    except Exception as e:
        print(e)



def run_discord_bot():
    DISCORD_TOKEN=os.environ.get("DISCORD_TOKEN")
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        await client.wait_until_ready()
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 
        
        username = str(message.author)
        user_msg = str(message.content)
        channel = str(message.channel)
        print(f"{username} {user_msg} => {channel}")
        if "<@&1086881213316341862>" in message.content:
            print(user_msg)
            await send_message(message, user_msg.replace("<@&1086881213316341862>", ""))

    client.run(DISCORD_TOKEN)

run_discord_bot()