from utils import *
from config import *
from functions.getState import getState

class Estate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл admins.py успешно загружен')

    @commands.slash_command(name='estate', description='Посмотреть имущество')
    async def __estate(self, interaction, nick: str = commands.Param(name='никнейм', description='Формат Nick_Name'), params=commands.Param(name='тип', choices=['Дома', 'Бизнесы'])):
        await interaction.response.send_message(embed=EmbedsList['waitInfo'])
        try:
            type_choice = 1 if params == 'Дома' else 2
            await getState(nickname=nick, type=type_choice, interaction=interaction)
            await add_log(self.bot, interaction.author, 0, f'[{interaction.author.id}]', f'/estate {nick} TYPE:{params}')


        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[estate] [type:GET] {ex}')

            
def setup(bot):
    bot.add_cog(Estate(bot))