from utils import *
from config import Settings
from functions.changeBalls import changeBalls
from functions.changeVigs import changeVigs
from functions.changePreds import changePreds
from functions.getUser import getUser

class SetStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл setStats.py успешно загружен')

    @commands.slash_command(name='set')
    async def set_command(self, interaction):
        pass
    
    @set_command.sub_command(description='Установить количество баллов')
    async def balls(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name'), 
        value: int = commands.Param(name='количество', description='Укажите количество баллов'), 
        reason: str = commands.Param(name='причина', description='Укажите причину'), option=commands.Param(name='действие', choices=['Выдать', 'Снять'])):
        user = await getUser(interaction.author)
        if user[6] > 2:
            await interaction.response.send_message(embed=EmbedsList['waitDo'])
            await getUser(interaction.author)
            infoEmbed = disnake.Embed(
                title='Изменение баллов',
                description=f'{GetJobNameByID[user[5]]} **{user[3]}** изменил количество баллов лидеру **{nick}**.\n`Количество: {value}` `Причина: {reason}`',
                color=Color.main_color,
                timestamp=datetime.now()
            )
            infoEmbed.set_footer(text=interaction.author.id)
            try:
                if option == 'Выдать':
                    changeBalls(interaction.author.id, nick, f'+{value}', reason)
                    await interaction.edit_original_response(embed=infoEmbed)
                    logger.info(f'[setStats][BALLS] {interaction.author.name} [{interaction.author.id}] выдал баллы игроку {nick} | ARG: +{value} | {reason}')

                elif option == 'Снять':
                    changeBalls(interaction.author.id, nick, f'-{value}', reason)
                    await interaction.edit_original_response(embed=infoEmbed)
                    logger.info(f'[setStats][BALLS] {interaction.author.name} [{interaction.author.id}] забрал баллы у игрока {nick} | ARG: -{value} | {reason}')

            except Exception as ex:
                await interaction.response.send_message(f'{interaction.author.mention} ошибка при выполнение команды, обратитесь к разработчику!\n```{ex}```')
                logger.error(f'[setStats:BALLS] [type:POST] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

    @set_command.sub_command(description='Установить количество выговоров')
    async def vigs(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name'), 
        value: int = commands.Param(name='количество', description='Укажите количество выговоров'), 
        reason: str = commands.Param(name='причина', description='Укажите причину'), option=commands.Param(name='действие', choices=['Выдать', 'Снять'])):
        user = await getUser(interaction.author)
        if user[6] > 2:
            await interaction.response.send_message(embed=EmbedsList['waitDo'])
            infoEmbed = disnake.Embed(
                title='Изменение выговоров',
                description=f'{GetJobNameByID[user[5]]} {user[3]} изменил количество выговоров лидеру **{nick}**.\n`Количество: {value}` `Причина: {reason}`',
                color=Color.main_color,
                timestamp=datetime.now()
            )
            infoEmbed.set_footer(text=interaction.author.id)
            try:
                if option == 'Выдать':
                    changeVigs(interaction.author.id, nick, f'+{value}', reason)
                    await interaction.edit_original_response(embed=infoEmbed)
                    logger.info(f'[setStats][VIGS] {interaction.author.name} [{interaction.author.id}] выдал выговор игроку {nick} | ARG: -{value} | {reason}')

                elif option == 'Снять':
                    changeVigs(interaction.author.id, nick, f'-{value}', reason)
                    await interaction.edit_original_response(embed=infoEmbed)
                    logger.info(f'[setStats][VIGS] {interaction.author.name} [{interaction.author.id}] снял выговор игроку {nick} | ARG: -{value} | {reason}')
                    
            except Exception as ex:
                await interaction.response.send_message(f'{interaction.author.mention} ошибка при выполнение команды, обратитесь к разработчику!\n```{ex}```')
                logger.error(f'[setStats:VIGS] [type:POST] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

    @set_command.sub_command(description='Установить количество предупреждений')
    async def preds(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name'), 
        value: int = commands.Param(name='количество', description='Укажите количество предупреждений'), 
        reason: str = commands.Param(name='причина', description='Укажите причину'), option=commands.Param(name='действие', choices=['Выдать', 'Снять'])):
        user = await getUser(interaction.author)
        if user[6] > 2:
            await interaction.response.send_message(embed=EmbedsList['waitDo'])
            infoEmbed = disnake.Embed(
                title='Изменение предупреждений',
                description=f'{GetJobNameByID[user[5]]} {user[3]} изменил количество предупреждений лидеру **{nick}**.\n`Количество: {value}` `Причина: {reason}`',
                color=Color.main_color,
                timestamp=datetime.now()
            )
            infoEmbed.set_footer(text=interaction.author.id)
            try:
                if option == 'Выдать':
                    changePreds(interaction.author.id, nick, f'+{value}', reason)
                    await interaction.edit_original_response(embed=infoEmbed)
                    logger.info(f'[setStats][PREDS] {interaction.author.name} [{interaction.author.id}] выдал пред-ие {nick} | ARG: +{value} | {reason}')


                elif option == 'Снять':
                    changePreds(interaction.author.id, nick, f'-{value}', reason)
                    await interaction.edit_original_response(embed=infoEmbed)
                    logger.info(f'[setStats][PREDS] {interaction.author.name} [{interaction.author.id}] снял пред-ие {nick} | ARG: -{value} | {reason}')

            except Exception as ex:
                await interaction.response.send_message(f'{interaction.author.mention} ошибка при выполнение команды, обратитесь к разработчику!\n```{ex}```')
                logger.error(f'[setStats:PRED] [type:POST] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])
            
def setup(bot):
    bot.add_cog(SetStats(bot))