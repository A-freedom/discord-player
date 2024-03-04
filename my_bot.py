import asyncio
import threading

import discord
from discord.ext import commands

import env
from ytdl_source import YTDLSource


class MyBot:
    def __init__(self, token, channel_id):
        self.songIndex = 0
        self.music_queue = []
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
            await self.play_command(ctx, *args)

        @self.bot.command(name='pause', help='This command pauses the song')
        async def pause(ctx):
            await self.pause_command(ctx)

        @self.bot.command(name='resume', help='Resumes the song')
        async def resume(ctx):
            await self.resume_command(ctx)

        @self.bot.command(name='stop', help='Stops the song')
        async def stop(ctx):
            await self.stop_command(ctx)

        @self.bot.command(name='skip', help='Stops the song')
        async def skip(ctx):
            await self.skip_command(ctx)

        @self.bot.command(name='clear', help='Stops the song')
        async def clear(ctx):
            await self.clear_command(ctx)

        @self.bot.command(name='queue', help='Stops the song')
        async def queue(ctx):
            await self.queue_command(ctx)

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

            return await play(ctx, message.content)

    # this function is used to hand the passing of new song to the bot
    async def play_command(self, ctx, *args):
        if self.is_paused:
            return await self.resume_command(ctx)

        async with ctx.typing():
            query = ' '.join(args).split('\n')
            # add the first song the play list
            first_song_info = YTDLSource.search_yt(query[0])
            self.music_queue.append(first_song_info)
            await ctx.send('-> Song added to the queue : {}'.format(first_song_info['title']))

            voice_channel = ctx.message.guild.voice_client
            if not voice_channel.is_playing():
                self.play_next(error=None, go_next=False, ctx=ctx)

            async def process_item(item_):
                song_info = YTDLSource.search_yt(item_)
                # the check below will be ture if search_yt run through an Exception
                if not song_info:
                    return await ctx.send("can't find the song")

                await ctx.send('-> Song added to the queue : {}'.format(song_info['title']))
                self.music_queue.append(song_info)

            await asyncio.gather(*(process_item(item) for item in query[1:-1]))




    def play_next(self, error, go_next, ctx):
        if error:
            return print(f"Error while playing: {error}")
        if self.is_paused:
            return

        voice_channel = ctx.message.guild.voice_client
        voice_channel.stop()

        # Check if there are more songs in the queue
        if self.music_queue:
            # Get the next song
            if go_next and self.songIndex + 1 < len(self.music_queue):
                self.songIndex = self.songIndex + 1
            next_song_ = self.music_queue[self.songIndex]
            return self.play(next_song_, ctx)

    def play(self, next_song_, ctx):
        voice_channel = ctx.message.guild.voice_client
        path_ = YTDLSource.fetch(next_song_['url'])
        # Play the next song and set the callback again
        return voice_channel.play(discord.FFmpegPCMAudio(source=path_),
                                  after=lambda e: (self.play_next(error=e, go_next=True, ctx=ctx)))

    async def pause_command(self, ctx):
        self.is_paused = True
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause_command()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
        return self

    async def resume_command(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if not self.music_queue:
            return await ctx.send("The bot was not playing anything before this. Use play_song command")

        if self.is_paused:
            self.is_paused = False
            return voice_client.resume()

    async def stop_command(self, ctx):
        self.is_paused = True
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            return await ctx.send("The bot is not playing anything at the moment.")

    async def queue_command(self, ctx):
        retval = ""
        # TODO fix this not clear loop
        for i in range(0, len(self.music_queue)):
            if i == self.songIndex:
                retval += '--> ' + self.music_queue[i]['title'] + '\n\n'
                continue
            retval += '    ' + self.music_queue[i]['title'] + '\n\n'

        if retval != "":
            return await ctx.send(retval)

        return await ctx.send("No music in queue")

    async def clear_command(self, ctx):
        self.is_paused = False
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        self.music_queue.clear()
        self.songIndex = 0
        return await ctx.send("Music queue cleared")

    async def skip_command(self, ctx):
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
        # try to play next in the queue if it exists
        return self.play_next(error=None, ctx=ctx, go_next=True)

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

    def start(self):
        self.bot.run(self.token)
