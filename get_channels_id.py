import discord

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
import env

TOKEN = env.list_of_bots[0]['token']

intents = discord.Intents().all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

    for guild in client.guilds:
        print(f'Channels in Guild "{guild.name}":')
        for channel in guild.channels:
            print(f'Name: {channel.name}, ID: {channel.id}, Type: {channel.type}')


@client.event
async def on_error(event, *args, **kwargs):
    print(f'Error in event {event}: {args[0]}')


client.run(TOKEN)
