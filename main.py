from utils import *
from disnake.ext import tasks

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())
db = UsersDataBase()

@bot.event
async def on_ready():
    bot.remove_command('help')
    activity = disnake.Activity(type=disnake.ActivityType.custom, name='Main Activity', state='Arizona Role Play')
    await bot.change_presence(status=disnake.Status.online, activity=activity)
    logger.success(f"Бот успешно запущен | {bot.user.display_name}#{bot.user.discriminator} | ID: {bot.user.id}")
    await db.create_users_table()
    await db.create_guilds_table()
    await db.create_members_table()
    await db.create_logs_table()
    await db.create_forum_table()
    members = 0
    for guild in bot.guilds:
        for member in guild.members:
            members += 1
            await db.add_user(member)
        await db.add_guild(guild)

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == '__main__':
    try:
        asyncio.run(bot.run('MTIxMzE3ODkzOTk1MDc2NDA5Mg.GxWNOf.urHxc3bK1vVt7HF6OgLH00VRcLyLDMIvFz8Y_Q'))

    except Exception as ex:
        logger.critical(f"Бот не смог запуститься | {bot.user.display_name} | {bot.user.id}\nОшибка: {ex}")