import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(1256525986464268358)  # channel ID goes here
        await channel.send("Meow :3")

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
discord_token = os.getenv('DISCORD_TOKEN')
client.run(discord_token)