# Discord Player
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-518065.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

A simple Python-based Discord bot manager for playing music in Discord channels. This README will guide you through the setup and usage of the Discord Music Bot Manager.

## Prerequisites

Before you start using this bot manager, make sure you have the following prerequisites in place:

- Docker (optional, for containerized deployment if you used docker you will not need to install the other Prerequisites ).
- Python 3.9 installed.
- FFmpeg installed. You can download it from  [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and set the path in your system.

## Setup

1. Clone this repository to your local machine:

    ```shell
    git clone https://github.com/A-freedom/discord_music_bot
    ```

2. Create a file named `env.py` in the project root directory with the following content:

    ```python
    # [list_of_bots] is used to define the bots in your channel. Each item in the list is a dictionary with two parameters:
    # {'token': 'your bot token', 'channel_id': 'the ID of the channel where the bot will run'}

    # You can run as many or as few bots as you wish.
    # Note: You can get your channel IDs by running
    #   => pip3 install discord.py
    #   => python3 ./get_channels_id.py

    list_of_bots = [
        {'token': 'your_token', 'channel_id': channel_id_should_be_int},
        {'token': 'your_token', 'channel_id': channel_id_should_be_int},
        {'token': 'your_token', 'channel_id': channel_id_should_be_int},
    ]

    # This is the prefix that all your commands will start with.
    command_prefix = '!'
    ```

    Replace `'your_token'` with your bot tokens and `channel_id_should_be_int` with the corresponding channel IDs.

3. If you're using Docker (recommended for easier setup), build and run the Docker container with the following commands:

    ```shell
    docker build -t my-app-image .
    docker run -p 8080:3000 my-app-image
    ```

   You can use any port you prefer.

4. If you choose not to use Docker, install the required Python packages and run the bot with the following commands:

    ```shell
    pip3 install -r requirements.txt
    python3 main.py
    ```

## Usage

- Once the bot is running, you can invite it to your Discord server by creating an OAuth2 URL in the Discord Developer Portal. Give it the appropriate permissions to read and send messages and connect to voice channels.

- You can just type the name or Lyric or past the [youtube_URL] and listen to the song. 

- Use the defined command prefix (default: `!`) to interact with the bot. For example, `!play [youtube_URL]`, `!skip`, `!pause`, `!resume`, etc.

- Enjoy playing music in your Discord channels!

## Missing Features

- **Playlist and Queue Management**: The bot currently lacks the ability to create and manage playlists or queues. This feature is planned for the next version.

- **Cleanup Function**: Downloaded files are not cleaned up, which may lead to storage issues over time. This will be addressed in a future release.

- **Stability and Testing**: The application is stable for basic usage, but some known issues still exist. It has not been thoroughly tested under heavy usage.

Feel free to contribute to this project and help us improve it!

If you encounter any issues or have suggestions, please [open an issue](https://github.com/A-freedom/discord_music_bot/issues).

Happy music playing! 🎶
