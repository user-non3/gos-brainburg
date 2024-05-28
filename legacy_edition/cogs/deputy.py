from utils import *
from config import *


class Deputy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл deputy.py успешно загружен')

    @commands.slash_command(name='deputy', description='Информация о Заместителе')
    async def deputy(self, interaction, fraction: int = commands.Param(name='фракция', description='ID Фракции')):
        await interaction.response.send_message(embed=EmbedsList['waitInfo'])
        try:
            r = requests.get(f"{api_url}/getDeputy?token={api_token}&fraction={fraction}")
            data = r.json()

            if data['success']:
                players = data['data']['players']
                result = ""
                for i in players:
                    
                    if i['lastinactive'] == None:
                        inActive = '\n'
                    
                    # else:
                    #     inActive = f'\n:exclamation: **Неактив до `{i['lastinactive']}`**\n'
                    
                    result += f"{inActive}:bust_in_silhouette: **Ник:** `{i['nickname']} [ID: {i['userID']}]`\n\
                    :pencil2: **Объяснительные:** `{i['vigs']}`\n:date: **Дата постановления:** `{i['postdate']}`\n:calendar: **На должносте:** `{i['alldays']} дня(ей)`\n"
                
                deputyEmbed = disnake.Embed(
                    title=f'Информация о заместителях фракции {GetFractionNameByID[fraction]}:',
                    description=f'{result}\nПросмотр онлайна: `/online Nick_Name`',
                    color=Color.main_color,
                    timestamp=datetime.now()
                )
                deputyEmbed.set_footer(text=f'{interaction.author.id}')
                await asyncio.sleep(2)
                await interaction.edit_original_response(embed=deputyEmbed)
                await add_log(self.bot, interaction.author, 0, f'[{interaction.author.id}]', f'/deputy FID:{fraction}')

                logger.info(f'[getDeputy] Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /deputy')
                
            else:
                errorEmbed = disnake.Embed(
                    title=f"{data['message']} :x:",
                    color=Color.red
                )
                await interaction.edit_original_response(embed=errorEmbed)
                logger.error(f"[getDeputy] [type:SEND] {data['message']}")
                
        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[getDeputy] [type:GET] {ex}')


def setup(bot):
    bot.add_cog(Deputy(bot))