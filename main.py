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
        if message.author == self.user:
            return

        if message.content.lower() == "megatron help":
            await self.send_help(message)
        elif message.content.lower() == "megatron list audio commands":
            await self.list_audio_commands(message)
        elif message.content.lower().startswith("megatron save audio"):
            await self.save_audio_command(message)
        elif message.content.lower().startswith("megatron modify audio command"):
            await self.modify_audio_command_name(message)
        elif message.content.lower().startswith("megatron modify audio"):
            await self.modify_audio_command(message)
        elif message.content.lower().startswith("megatron delete audio"):
            await self.delete_audio_command(message)
        elif message.content.lower() in audio_command_map:
            await self.play_audio_command(message)
        elif message.content.lower() == "megatron hello":
            await self.send_hello(message)

    async def send_help(self, message):
        help_message = (
            "Here are the available commands:\n"
            "1. `megatron list audio commands`: Lists all saved audio commands.\n"
            "2. `megatron save audio <command_name>`: Saves an audio file for a specific command.\n"
            "3. `megatron modify audio <command_name>`: Modifies the audio for an existing command.\n"
            "4. `megatron modify audio command <old_command>:<new_command>`: Changes the command name for an existing audio.\n"
            "5. `megatron delete audio <command_name>`: Deletes an audio command and its associated file.\n"
            "6. `megatron hello`: Greets with the Megatron logo.\n"
        )
        await message.channel.send(help_message)

    async def list_audio_commands(self, message):
        if audio_command_map:
            command_list = "\n".join([f"• {command}" for command in audio_command_map])
            await message.channel.send(f"Here are the available audio commands:\n{command_list}")
        else:
            await message.channel.send("No audio commands have been saved yet.")

    async def save_audio_command(self, message):
        if len(message.attachments) == 1:
            audio_file = message.attachments[0]
        else:
            await message.channel.send("Please provide an MP3.")
            return

        if audio_file.filename.endswith(".mp3"):
            audio_path = f"./audio_files/{audio_file.filename}"
            await audio_file.save(audio_path)

            command = message.content.lower().replace("megatron save audio", "").strip()

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

    async def modify_audio_command(self, message):
        command = message.content.lower().replace("megatron modify audio", "").strip()

        if command in audio_command_map:
            if len(message.attachments) == 1:
                audio_file = message.attachments[0]
            else:
                await message.channel.send("Please provide an MP3 to modify the command.")
                return

            if audio_file.filename.endswith(".mp3"):
                audio_path = f"./audio_files/{audio_file.filename}"
                await audio_file.save(audio_path)

                audio_command_map[command] = audio_path
                save_audio_command_map()
                await message.channel.send(f"Audio for command '{command}' has been modified to '{audio_file.filename}'.")
            else:
                await message.channel.send("The file must be an MP3.")
                return
        else:
            await message.channel.send(f"Command '{command}' does not exist.")

    async def modify_audio_command_name(self, message):
        parts = message.content.lower().replace("megatron modify audio command", "").strip().split(':')

        if len(parts) != 2:
            await message.channel.send("Please provide both the old command and the new command.")
            return
        
        old_command, new_command = parts
        old_command = old_command.strip()
        new_command = new_command.strip()

        if old_command in audio_command_map:
            if new_command in audio_command_map:
                await message.channel.send(f"The new command '{new_command}' already exists. Choose another command name.")
                return
            
            audio_path = audio_command_map[old_command]

            del audio_command_map[old_command]

            audio_command_map[new_command] = audio_path
            save_audio_command_map()

            await message.channel.send(f"Command '{old_command}' has been successfully renamed to '{new_command}'.")

        else:
            await message.channel.send(f"Command '{old_command}' does not exist.")

    async def delete_audio_command(self, message):
        command = message.content.lower().replace("megatron delete audio", "").strip()

        if command in audio_command_map:
            audio_path = audio_command_map[command]
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    print(f"Deleted audio file: {audio_path}")
                else:
                    print(f"Audio file for command '{command}' not found.")
            except Exception as e:
                print(f"Error deleting audio file: {e}")

            del audio_command_map[command]
            save_audio_command_map()
            await message.channel.send(f"Audio command '{command}' and its associated file have been deleted.")
        else:
            await message.channel.send(f"Command '{command}' does not exist.")

    async def play_audio_command(self, message):
        global last_audio_playback_time
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

    async def send_hello(self, message):
        await message.channel.send(f'`{MEGATRON}`')

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
