import my_secret
from my_bot import MyBot
import threading

if __name__ == "__main__":
    my_bots = my_secret.list_of_bots

    thread_list = []
    for bot_info in my_bots:
        bot = MyBot(bot_info['token'], bot_info['channel_id'])
        thread = threading.Thread(target=bot.run, name=bot_info['token'])
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    # this for dug
    # bot_info = my_bots[0]
    # bot = MyBot(bot_info['token'], bot_info['channel_id'])
    # bot.run()
