import discord
import os
import time
import json
from datetime import datetime, timedelta
from event_card import create_image_with_text
from calendar_builder import generate_month
from faerun_today import get_todays_messages

KIEDY_KURDE_SESJA_CHANNEL_ID = 1256702886717427856
TEST_ASDASDASD_CHANNEL_ID = 1256525986464268358
CALENDAR_CHANNEL_ID=1256702886717427856
CALENDAR_DATA_CHANNEL_ID=1256713139592892509
FAERUN_TODAY_CHANNEL_ID=1257059747509567488

DRY_RUN = False

start_time = time.time()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        print("--- %s : on_ready ---" % (time.time() - start_time))

        # channel = self.get_channel(TEST_ASDASDASD_CHANNEL_ID)  # channel ID goes here
        # await channel.send("Meow :3")

        channel = self.get_channel(CALENDAR_DATA_CHANNEL_ID)
        send_channel = self.get_channel(CALENDAR_CHANNEL_ID)
        faerun_today_channel = self.get_channel(FAERUN_TODAY_CHANNEL_ID)
        test_channel = self.get_channel(TEST_ASDASDASD_CHANNEL_ID)

        # current hour
        current_time = datetime.now()

        if DRY_RUN:
            return

        await load_events_from_channel(channel, send_channel)
        if 6 <= current_time.hour < 7:
            await update_faerun_today(faerun_today_channel)

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content == 'ping':
            await message.channel.send('pong')

async def send_on_channel(message, channel):
    await channel.send(message)

async def update_faerun_today(faerun_today_channel):
    message, image_path = get_todays_messages()
    await send_on_channel(message, faerun_today_channel)
    if image_path != None:
        await faerun_today_channel.send(file=discord.File(image_path))

async def load_events_from_channel(channel, send_channel):
        messages = [message async for message in channel.history(limit=123)]
        for message in messages:
            mini_dict = convert_to_dict(message.content)
            events_by_date[mini_dict['date']] = mini_dict
        # Get the current date
        current_date = datetime.now()
        current_date_str = current_date.strftime("%Y-%m-%d")
        # Extract month from datetime object
        today_month = current_date.month
        month_index = today_month - 1
        # Format the date as "yyyy-mm-dd"
        await send_channel.purge(limit=100)
        for month_offset in [-1, 0, 1]:
        # Calculate the date for the target month
            checked_month = today_month+month_offset
            if 1 <= checked_month <= 9:
                month_str =  f"0{checked_month}"
            else:
                month_str= str(checked_month)
            new_event_dict = {}
            for day in range(1, 31):
                date_str = f"{current_date.year}-{month_str}-{day:02}"
                if date_str in events_by_date.keys():
                    new_event_dict[date_str] = events_by_date[date_str]
            print(new_event_dict)
            generate_month(month_index+month_offset, current_date_str, new_event_dict)
            await send_channel.send(file=discord.File("calendar_with_events.png"))
            


        # take 3 months from 1 before to 1 after
        # for each month extract from events_by_date all months of this date and place them to new dict
        # generate data
        print("--- %s : finished messages send ---" % (time.time() - start_time))

# Function to convert mini-JSON string to dictionary
def convert_to_dict(json_string):
    data_dict = json.loads(json_string)
    return data_dict

def load_from_file():
    pass

def generate_calendar():
    pass

events_by_date = {}

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
discord_token = os.getenv('DISCORD_TOKEN')
client.run(discord_token)