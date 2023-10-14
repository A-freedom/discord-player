import asyncio

import discord
from discord.ext import commands

import env
from ytdl_source import YTDLSource


class MyBot:
    def __init__(self, token, channel_id):
        self.music_queue = []
        # self.is_playing = False
        self.is_paused = False

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
        async def play(ctx, *args):
            await self.play(ctx, *args)

        @self.bot.command(name='pause', help='This command pauses the song')
        async def pause(ctx):
            await self.pause(ctx)

        @self.bot.command(name='resume', help='Resumes the song')
        async def resume(ctx):
            await self.resume(ctx)

        @self.bot.command(name='stop', help='Stops the song')
        async def stop(ctx):
            await self.stop(ctx)

        @self.bot.command(name='skip', help='Stops the song')
        async def skip(ctx):
            await self.skip(ctx)

        @self.bot.command(name='clear', help='Stops the song')
        async def clear(ctx):
            await self.clear(ctx)

        @self.bot.command(name='queue', help='Stops the song')
        async def queue(ctx):
            await self.queue(ctx)

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

            if message.content.startswith(env.command_prefix):
                return await self.bot.process_commands(message)
            # if is_valid_youtube_url(message.content):
            return await play(ctx, message.content)
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

    # this function is used to hand the passing of new song to the bot
    async def play(self, ctx, *args):
        async with ctx.typing():
            if self.is_paused:
                return await self.resume(ctx)

            async def process_item(item):
                song = await YTDLSource.search_yt(item, loop=self.bot.loop)

                # TODO type(song) == type(True) is not cool find anther way
                # the check below will be ture if search_yt run through an Exception
                if type(song) == type(True):
                    return await ctx.send("can't find the song")
                await ctx.send('-> Song added to the queue : {}'.format(song['title']))
                self.music_queue.append(song)
                return await self.play_song(ctx)

            query = ' '.join(args).split('\n')
            await asyncio.gather(*(process_item(item) for item in query))

    # this function used to play the first time in the self.music_queue and nothing else
    async def play_song(self, ctx):
        # noinspection PyBroadException
        # try:
        voice_channel = ctx.message.guild.voice_client
        if not voice_channel.is_playing():
            async with ctx.typing():
                next_song = self.music_queue[0]
                path = await YTDLSource.fetch(next_song['url'], loop=self.bot.loop)
                await ctx.send('-> Now playing : {}'.format(next_song['title']))

                # move to the next song on the list
                # loop = asyncio.get_event_loop()
                voice_channel.play(discord.FFmpegPCMAudio(source=path),
                                   # after=lambda e: (loop.run_until_complete(self.skip(ctx)), loop.close())
                                   )

                # except Exception:
                #     # TODO log the error
                #     await ctx.send("somthing bad happened")
                # return self

    async def pause(self, ctx):
        self.is_paused = True
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        return self

    async def resume(self, ctx):
        self.is_paused = False
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            return await ctx.send("The bot was not playing anything before this. Use play_song command")

    async def stop(self, ctx):
        self.is_paused = True
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            return await ctx.send("The bot is not playing anything at the moment.")

    async def queue(self, ctx):
        retval = ""
        # TODO fix this not clear loop
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            # if i > 4: break
            retval += self.music_queue[i]['title'] + "\n\n"

        if retval != "":
            return await ctx.send(retval)

        return await ctx.send("No music in queue")

    async def clear(self, ctx):
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
        self.music_queue.clear()
        return await ctx.send("Music queue cleared")

    async def skip(self, ctx):
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
        # try to play next in the queue if it exists
        self.music_queue.pop(0)
        return await self.play_song(ctx)

    def start(self):
        self.bot.run(self.token)
