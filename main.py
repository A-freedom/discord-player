import env
from my_bot import MyBot
import threading
import sys

if __name__ == "__main__":
    my_bots = env.list_of_bots

    if not sys.gettrace() is not None:
        thread_list = []
        for bot_info in my_bots:
            bot = MyBot(bot_info['token'], bot_info['channel_id'])
            thread = threading.Thread(target=bot.start, name=bot_info['token'])
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()
    else:
        print('you are in debug mode')
        # this for dug
        bot_info = my_bots[0]
        bot = MyBot(bot_info['token'], bot_info['channel_id'])
        bot.start()
