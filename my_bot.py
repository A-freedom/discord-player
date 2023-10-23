import discord
from discord.ext import commands

import env
from ytdl_source import YTDLSource


class MyBot:
    def __init__(self, token, channel_id):
        self.songIndex = 0
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

            query = ' '.join(args).split('\n')
            for item in query:
                print(item)
                song = YTDLSource.search_yt(item)

                # TODO type(song) == type(True) is not cool find anther way
                # the check below will be ture if search_yt run through an Exception
                # if type(song) == type(True):
                #     return await ctx.send("can't find the song")
                await ctx.send('-> Song added to the queue : {}'.format(song['title']))
                self.music_queue.append(song)

                # if not self.is_playing:
                #     self.is_playing = True
                #     print("playing")
                await self.play_song(ctx)

            # query = ' '.join(args).split('\n')
            # await asyncio.gather(*(process_item(item) for item in query))

    # this function used to play the first time in the self.music_queue and nothing else
    async def play_song(self, ctx):
        voice_channel = ctx.message.guild.voice_client

        if not voice_channel.is_playing():
            async with ctx.typing():
                # Get the next song from the queue
                next_song = self.music_queue[0]
                path = YTDLSource.fetch(next_song['url'])

                await ctx.send('Now playing: {}'.format(next_song['title']))

                # Define a callback function for when the song finishes
                def after_playing(error):
                    if error:
                        print(f"Error while playing: {error}")
                    else:
                        # Remove the finished song from the queue
                        # self.music_queue.pop(0)

                        # Check if there are more songs in the queue
                        if self.music_queue:
                            # Get the next song
                            next_song_ = self.music_queue[self.songIndex]
                            self.songIndex = self.songIndex + 1
                            path_ = YTDLSource.fetch(next_song_['url'])

                            # Play the next song and set the callback again
                            voice_channel.play(discord.FFmpegPCMAudio(source=path_), after=after_playing)
                        else:
                            # If no more songs in the queue, you can leave the voice channel
                            voice_channel.stop()

                after_playing(False)

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
            if i == self.songIndex:
                retval += '--> ' + self.music_queue[i]['title'] + '\n\n'
            retval += '    ' + self.music_queue[i]['title'] + '\n\n'

        if retval != "":
            return await ctx.send(retval)

        return await ctx.send("No music in queue")

    async def clear(self, ctx):
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
        self.music_queue.clear()
        self.songIndex = 0
        return await ctx.send("Music queue cleared")

    async def skip(self, ctx):
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
        # try to play next in the queue if it exists
        self.songIndex = self.songIndex + 1
        return await self.play_song(ctx)

    def start(self):
        self.bot.run(self.token)
