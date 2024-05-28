from utils import *

log_channel_one = 1239618414163656775
log_channel_two = 1244928000684724316

async def add_log(bot, user, message, channel, cmd):
    logs_channel_one = bot.get_channel(log_channel_one)
    logs_channel_two = bot.get_channel(log_channel_two)
    date = f'{datetime.now()}'
    date_splited = date.split('.')
    await logs_channel_one.send(f'{date_splited[0]} | <@{user.id}> [{user.id}] {message} в канале <#{channel.id}> [{channel.id}] => `{cmd}`')
    await logs_channel_two.send(f'{date_splited[0]} | <@{user.id}> [{user.id}] {message} в канале <#{channel.id}> [{channel.id}] => `{cmd}`')