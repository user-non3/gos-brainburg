from utils import *

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.Cog.listener()    
    async def on_ready(self):
        logger.debug('Файл events.py успешно загружен')
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logger.info(f"[ON_GUILD_JOIN] Бот был добавлен на сервер '{guild.name}' [{guild.id}]")
        log_channel_id = 1239618414163656775
        
        logEmbed = disnake.Embed(
            title='Добавление сервера',
            description=f'Имя сервера: `{guild.name} (ID: {guild.id})`\nВладелец: `{guild.owner} (ID: {guild.owner.id})`\nКоличество участников: `{len(guild.members)}`\
                \nКоличество ролей: `{len(guild.roles)}`',
            timestamp=datetime.now(),
            color=Color.gray
        )
        logEmbed.set_footer(text=f'GID: {guild.id}')
        log_channel = self.bot.get_channel(log_channel_id)
        await log_channel.send(embed=logEmbed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logger.info(f"[ON_GUILD_REMOVE] Бот был удален с сервера '{guild.name}' [{guild.id}]")
        log_channel_id = 1239618414163656775

        logEmbed = disnake.Embed(
            title='Удаление сервера',
            description=f'Имя сервера: `{guild.name} (ID: {guild.id})`\nВладелец: `{guild.owner} (ID: {guild.owner.id})`\nКоличество участников: `{len(guild.members)}`\
                \nКоличество ролей: `{len(guild.roles)}`',
            timestamp=datetime.now(),
            color=Color.gray)
        
        logEmbed.set_footer(text=f'GID: {guild.id}')
        log_channel = self.bot.get_channel(log_channel_id)
        await log_channel.send(embed=logEmbed)

def setup(bot):
    bot.add_cog(Events(bot))