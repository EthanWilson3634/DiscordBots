import discord
import asyncio
import os
import pyfiglet
import json
import time

MEGATRON = pyfiglet.figlet_format("MEGATRON")

AUDIO_COMMAND_MAP_FILE = "audio_command_map.json"

audio_command_map = {}

# Timestamp to track last audio playback
last_audio_playback_time = 0

# Time threshold in seconds
AUDIO_PLAYBACK_THRESHOLD = 10

def load_audio_command_map():
    global audio_command_map
    if os.path.exists(AUDIO_COMMAND_MAP_FILE):
        with open(AUDIO_COMMAND_MAP_FILE, "r") as file:
            try:
                audio_command_map = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding JSON, resetting the audio command map.")
                audio_command_map = {}

def save_audio_command_map():
    with open(AUDIO_COMMAND_MAP_FILE, "w") as file:
        json.dump(audio_command_map, file, indent=4)

class Client(discord.Client):
    async def on_ready(self):
        print(f'\nLogged in as {self.user}!\n')
        print(MEGATRON)
        print()

    async def on_message(self, message):
        global last_audio_playback_time

        if message.author == self.user:
            return

        if message.content.lower().startswith("save audio"):
            if len(message.attachments) == 1:
                audio_file = message.attachments[0]
            else:
                await message.channel.send("Please provide an MP3.")
                return
                
            if audio_file.filename.endswith(".mp3"):
                audio_path = f"./audio_files/{audio_file.filename}"
                await audio_file.save(audio_path)
                
                command = message.content.lower().replace("save audio", "").strip()
                
                if command:
                    audio_command_map[command] = audio_path
                    save_audio_command_map()
                    await message.channel.send(f"Audio saved for command '{command}' as '{audio_file.filename}'.")
                else:
                    await message.channel.send("Please provide a command name after 'save audio'.")
                    return
            else:
                await message.channel.send("The file must be an MP3.")
                return
        
        elif message.content.lower() in audio_command_map:
            current_time = time.time()

            if current_time - last_audio_playback_time < AUDIO_PLAYBACK_THRESHOLD:
                await message.channel.send(f"Please wait {AUDIO_PLAYBACK_THRESHOLD - (current_time - last_audio_playback_time):.1f} seconds before playing more audio.")
                return

            if message.author.voice is None:
                await message.channel.send("Enter a voice channel to play audio")
                return
            
            voice_channel = message.author.voice.channel
            await self.play_audio_in_channel(voice_channel, audio_command_map[message.content.lower()])
            
            last_audio_playback_time = time.time()
        
        ####################################################MEGATRON#####################################################
        if message.content.lower() == "hello megatron":
            await message.channel.send('`' + MEGATRON + '`')
        #################################################################################################################

    async def play_audio_in_channel(self, channel, audio):
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="/opt/homebrew/bin/ffmpeg", source=audio))
        while vc.is_playing():
            await asyncio.sleep(0.1)
        await vc.disconnect()

intents = discord.Intents.default()
intents.message_content = True

with open("botkey.txt", "r") as file:
    bot_token = file.read().strip()

load_audio_command_map()

client = Client(intents=intents)
client.run(bot_token)
