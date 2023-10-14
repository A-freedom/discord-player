import asyncio
from pathlib import Path

import discord
import yt_dlp

# Define the output folder for downloaded files
output_folder = Path("downloaded/youtube")

# Create the output folder if it doesn't exist
output_folder.mkdir(parents=True, exist_ok=True)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'outtmpl': str(output_folder / "%(id)s.%(ext)s"),  # Use the video ID as the filename
}

# Initialize yt_dlp instance
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def fetch(cls, item, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(item, download=not stream))
            if 'entries' in data:
                data = data['entries'][0]
            filename = data['id'] if stream else ytdl.prepare_filename(data)
        except Exception:
            # TODO log the error
            return False

        return filename

    @classmethod
    async def search_yt(cls, item, loop=None):
        loop = loop or asyncio.get_event_loop()
        # noinspection PyBroadException
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{item}", download=False))
            if 'entries' in data:
                data = data['entries'][0]
        except Exception:
            # TODO log the error
            return False

        return {'url': data['original_url'], 'title': data['title']}
