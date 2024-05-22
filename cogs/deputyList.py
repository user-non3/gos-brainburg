from utils import *
from config import Settings

class DeputyList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл deputyList.py успешно загружен')

    @commands.slash_command(description='Список заместителей на сервере')
    async def deputylist(self, interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getDeputyList?token={Settings.token_api}")
                data = r.json()

                if data['success']:
                    count = data['data']['count']
                    players = data['data']['players']
                    
                    result = ""
                    for i in players:
                        result += f"Ник: {i['nickname']} [ID: {i['leaderID']}] Фракция: {i['fraction']}\n"
                        
                    deputyList = disnake.Embed(
                        title=f'Список заместителей на {GetServerNameByID[5]} {GetServerIconByID[5]}',
                        description=f':bust_in_silhouette: Всего заместителей - `{count}`\n```{result}```',
                        color=Color.main_color,
                        timestamp=datetime.now()
                    )
                    
                    deputyList.set_footer(text=f'{interaction.author.id}')
                    await asyncio.sleep(2)
                    await interaction.edit_original_response(embed=deputyList)
                    logger.info(f'[getDeputyList] Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /deputylist')

                    
                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    await interaction.edit_original_response(embed=errorEmbed)
                    logger.error(f"[getDeputyList] [type:SEND] {data['message']}")

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[getDeputyList] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

def setup(bot):
    bot.add_cog(DeputyList(bot))