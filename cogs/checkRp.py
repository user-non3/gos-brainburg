from utils import *

class CheckRP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл online.py успешно загружен')

    
    @commands.slash_command(description='Проверить РПшность ника')
    async def checkrp(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name')):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
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

                await interaction.edit_original_response(embed=infoEmbed)

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[checkRP] [type:GET] {ex}')
        
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])
            
def setup(bot):
    bot.add_cog(CheckRP(bot))