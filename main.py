import discord

class Client(discord.Client):
    async def on_ready(self):
        print("""
                            _                   
                           | |                  
 _ __ ___   ___  __ _  __ _| |_ _ __ ___  _ __  
| '_ ` _ \\ / _ \\/ _` |/ _` | __| '__/ _ \\| '_ \\ 
| | | | | |  __/ (_| | (_| | |_| | | (_) | | | |
|_| |_| |_|\\___|\\__, |\\__,_|\\__|_|  \\___/|_| |_|
                 __/ |                          
                |___/                           
    """)
    
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('')