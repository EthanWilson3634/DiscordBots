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
        
        if message.content.lower() == "no clue":
            voice_channel = message.author.voice.channel
            if voice_channel is None:
                await message.channel.send("Enter a voice channel")
                return

            print(voice_channel)

            print("Playing...")
            await self.play_audio_in_channel(message.author.voice.channel, "./no_clue_what_they_are_doing.mp3")

    async def play_audio_in_channel(self, channel, audio):
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="/opt/homebrew/bin/ffmpeg", source=audio))
        while vc.is_playing():
            await asyncio.sleep(0.1)
        await vc.disconnect()
    
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('')