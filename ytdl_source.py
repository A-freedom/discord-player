import discord
import yt_dlp
import asyncio
import os

# Define the output folder for downloaded files
output_folder = ".\data\youtube"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

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
    'outtmpl': f'{output_folder}\%(title)s.%(ext)s',  # Use video title as the filename
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
    async def fetch_from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take the first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        full_file_path = filename
        print(full_file_path)
        return [full_file_path,data['title']]
