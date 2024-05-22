from utils import *
from config import Settings

class LeadersList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл leadersList.py успешно загружен')

    @commands.slash_command(name='leaderslist', description='Список лидеров на сервере')
    async def get_leaders(self, interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getLeaderList?token={Settings.token_api}")
                data = r.json()

                if data['success']:
                    count = data['data']['count']
                    players = data['data']['players']
                    
                    result = ""
                    for i in players:
                        fraction = i['fraction']
                        result += f"Ник: {i['nickname']} | Фракция: {GetFractionNameByID[fraction]}\n"
                        
                    deputyList = disnake.Embed(
                        title=f'Список лидеров {GetServerNameByID[5]} {GetServerIconByID[5]}',
                        description=f':bust_in_silhouette: Всего лидеров - `{count}`\n```{result}```',
                        color=Color.main_color,
                        timestamp=datetime.now()
                    )
                    
                    deputyList.set_footer(text=f'{interaction.author.id}')
                    await asyncio.sleep(2)
                    await interaction.edit_original_response(embed=deputyList)
                    logger.info(f'[getLeaderList] Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /leaderslist')

                    
                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    await interaction.edit_original_response(embed=errorEmbed)
                    logger.error(f"[getLeaderList] [type:SEND] {data['message']}")

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[getLeaderList] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

def setup(bot):
    bot.add_cog(LeadersList(bot))