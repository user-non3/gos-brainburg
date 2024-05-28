from utils import *

class CheckRP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл online.py успешно загружен')

    
    @commands.slash_command(name='checkrp', description='Проверить РПшность ника')
    async def __checkrp(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name')):
        await interaction.response.send_message(embed=EmbedsList['waitInfo'])
        try:
            response = await vprikol.check_rp_nickname(nick)
            nickname = nick.split('_')
            images = [response.name.graph, response.surname.graph]
            
            if response.name.rp:
                name = f':white_check_mark: Имя «{nickname[0]}» существует в реальной жизни.'

            else:
                name = f':closed_book:  Имя «{nickname[0]}» не существует в реальной жизни.'

            if response.surname.rp:
                surname = f':white_check_mark: Фамилия «{nickname[1]}» существует в реальной жизни.'

            else:
                surname = f':closed_book:  Фамилия «{nickname[1]}» не существует в реальной жизни.'

            infoEmbed = disnake.Embed(
                title='Проверка ника',
                color=Color.main_color,
                timestamp=datetime.now(),
                description=f'{name}\n{surname}'
            )
            infoEmbed.set_image(url=random.choice(images))
            infoEmbed.set_footer(text=interaction.author.id)
            await add_log(self.bot, interaction.author, 'использовал команду', interaction.channel, f'/checkrp NICK:{nick}')

            await interaction.edit_original_response(embed=infoEmbed)

        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[checkRP] [type:GET] {ex}')
            
def setup(bot):
    bot.add_cog(CheckRP(bot))