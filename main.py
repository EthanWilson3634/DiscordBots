import discord
import asyncio
import pyfiglet

MEGATRON = pyfiglet.figlet_format("MEGATRON")

class Client(discord.Client):
    async def on_ready(self):
        print(f'\nLogged in as {self.user}!\n')
        print(MEGATRON)
        print()
        
    async def on_message(self, message):
        if message.content.lower() == 'hello megatron':
            await message.channel.send('`' + MEGATRON + '`')
        #################################################################################################################
        if message.content.lower() == "discord troll":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return
            await self.play_audio_in_channel(message.author.voice.channel, "./audio_files/mikejebait-3.mp3")
        #################################################################################################################
        if message.content.lower() == "no clue":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return
            await self.play_audio_in_channel(message.author.voice.channel, "./audio_files/no_clue.mp3")
        ################################################################################################################
        if message.content.lower() == "lack of a father figure":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return
            await self.play_audio_in_channel(message.author.voice.channel, "./audio_files/lack-of-a-father-figure.mp3")
        #################################################################################################################
        if message.content.lower() == "goku":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return
            await self.play_audio_in_channel(message.author.voice.channel, "./audio_files/drip-goku-meme-song-original-dragon-ball-super-music-clash-of-gods-in-description.mp3")
        #################################################################################################################
        if message.content.lower() == "deja vu":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return
            await self.play_audio_in_channel(message.author.voice.channel, "./audio_files/deja-vu-fade.mp3")
        #################################################################################################################
        if message.content.lower() == "gay song":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return
            await self.play_audio_in_channel(message.author.voice.channel, "./audio_files/tower-of-gayyyyyyyy.mp3")
        #################################################################################################################
        if message.content.lower() == "ha gay":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return
            await self.play_audio_in_channel(message.author.voice.channel, "./audio_files/ha-gay.mp3")
        #################################################################################################################
    async def play_audio_in_channel(self, channel, audio):
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="/opt/homebrew/bin/ffmpeg", source=audio))
        while vc.is_playing():
            await asyncio.sleep(0.1)
        await vc.disconnect()

        # async def save_audio_file(self, ):
        #     if str(message.attachments) == "[]": # Checks if there is an attachment on the message
        #         return
        #     else: # If there is it gets the filename from message.attachments
        #         split_v1 = str(message.attachments).split("filename='")[1]
        #         filename = str(split_v1).split("' ")[0]
        #         if filename.endswith(".csv"): # Checks if it is a .csv file
        #             await message.attachments[0].save(fp="CsvFiles/{}".format(filename)) # saves the file

    
intents = discord.Intents.default()
intents.message_content = True

with open("botkey.txt", "r") as file:
    bot_token = file.read().strip()

client = Client(intents=intents)
client.run(bot_token)
