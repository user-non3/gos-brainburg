from utils import *
from disnake.ext import tasks

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())
db = UsersDataBase()

@bot.event
async def on_ready():
    bot.remove_command('help')
    # activity = disnake.Activity(type=disnake.ActivityType.custom, name='Main Activity', state='Arizona Role Play')
    # await bot.change_presence(status=disnake.Status.online, activity=activity)
    logger.success(f"Бот успешно запущен | {bot.user.display_name}#{bot.user.discriminator} | ID: {bot.user.id}")
    await db.create_users_table()
    await db.create_members_table()
    await db.create_logs_table()
    members = 0
    for guild in bot.guilds:
        for member in guild.members:
            members += 1
            await db.add_user(member)

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == '__main__':
    asyncio.run(bot.run('MTIyODczMDU0ODI4MTgwMjg0Mw.GC-EYz.Jg6EUl8CLYK43XU_2VLHU0DLB2GCpHSgXcBdzE'))
