import env

import unittest
from unittest.mock import Mock
from my_bot import MyBot  # Import your bot class from my_bot.py

class TestMyBot(unittest.TestCase):
    def setUp(self):
        # Initialize your bot instance with mock data (replace with your actual token and channel ID)
        self.bot = MyBot(token=env.list_of_bots[0]['token'], channel_id=env.list_of_bots[0]['channel_id'])

    def test_play_command(self):
        # Create a mock context with a fake message content
        ctx = Mock()
        ctx.send = Mock()
        ctx.message.guild.voice_client.is_playing.return_value = False  # Simulate not playing

        # Call the play command with the mock context and some example arguments
        self.bot.play_command(ctx, "believer")

        # Assert that the bot responded correctly (you may need to adjust this depending on your bot's behavior)
        ctx.send.assert_called_once_with('-> Song added to the queue : YourSongTitle')

if __name__ == '__main__':
    unittest.main()