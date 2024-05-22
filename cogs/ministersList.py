from utils import *
from config import Settings

class MinistersList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл ministersList.py успешно загружен')

    @commands.slash_command(description='Список министров на сервере')
    async def ministerslist(self, interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getMinisterList?token={Settings.token_api}")
                data = r.json()

                if data['success']:
                    count = data['data']['count']
                    players = data['data']['players']
                    
                    result = ""
                    for i in players:
                        result += f"Ник: {i['nickname']} | Фракция: {GetFractionNameByID[i['fraction']]}\n"
                        
                    ministersList = disnake.Embed(
                        title=f'Список заместителей на {GetServerNameByID[5]} {GetServerIconByID[5]}',
                        description=f':bust_in_silhouette: Всего министров - `{count}`\n```{result}```',
                        color=Color.main_color,
                        timestamp=datetime.now()
                    )
                    
                    ministersList.set_footer(text=f'{interaction.author.id}')
                    await asyncio.sleep(2)
                    await interaction.edit_original_response(embed=ministersList)
                    logger.info(f'[getMinistersList] Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /ministerslist')

                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    logger.error(f"[getMinistersList] [type:SEND] {data['message']}")
                    await interaction.edit_original_response(embed=errorEmbed)

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[getMinistersList] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

def setup(bot):
    bot.add_cog(MinistersList(bot))