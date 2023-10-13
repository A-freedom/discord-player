import discord
from discord.ext import commands

import env
from ytdl_source import YTDLSource


class MyBot:
    def __init__(self, token, channel_id):
        self.channel_id = channel_id
        self.token = token
        self.intents = discord.Intents().all()
        self.bot = commands.Bot(command_prefix=env.command_prefix, intents=discord.Intents().all())

        @self.bot.command(name='join', help='Tells the bot to join the voice channel')
        async def join(ctx):
            await self.join(ctx)

        @self.bot.command(name='leave', help='To make the bot leave the voice channel')
        async def leave(ctx):
            await self.leave(ctx)

        @self.bot.command(name='play', help='To play song')
        async def play_song(ctx, url):
            await self.play_song(ctx, url)

        @self.bot.command(name='pause', help='This command pauses the song')
        async def pause(ctx):
            await self.pause(ctx)

        @self.bot.command(name='resume', help='Resumes the song')
        async def resume(ctx):
            await self.resume(ctx)

        @self.bot.command(name='stop', help='Stops the song')
        async def stop(ctx):
            await self.stop(ctx)

        @self.bot.event
        async def on_ready():
            await self.bot.get_channel(self.channel_id).connect()

        @self.bot.event
        async def on_message(message):
            # Your custom logic here
            if message.author == self.bot.user:
                return  # Don't respond to ourselves

            if message.channel.id != self.channel_id:
                return  # Respond only in the channel the bot is in

            ctx = await self.bot.get_context(message)  # Create a context for the message

            if message.content.startswith(my_secret.command_prefix):
                return await self.bot.process_commands(message)
            # if is_valid_youtube_url(message.content):
            return await play_song(ctx, message.content)
            # await self.search(ctx,message.content)

    def run(self):
        self.bot.run(self.token)

    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()
        return self

    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")
        return self

    async def play_song(self, ctx, url):
        # try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            data = await YTDLSource.fetch_from_url(url, loop=self.bot.loop)
            filename = data[0]
            voice_channel.play(discord.FFmpegPCMAudio(source=filename))
        await ctx.send('**Now playing:** {}'.format(data[1]))
        # except:
        #     await ctx.send("The bot is not connected to a voice channel.")
        # return self



    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        return self


    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")
        return self


    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        return self


def run(self):
    self.bot.run(self.token)
