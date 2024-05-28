from utils import *
from config import *

class DeputyList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл deputyList.py успешно загружен')

    @commands.slash_command(name='deputylist', description='Список заместителей на сервере')
    async def __deputylist(self, interaction):
        await interaction.response.send_message(embed=EmbedsList['waitInfo'])
        try:
            r = requests.get(f"{api_url}/getDeputyList?token={api_token}")
            data = r.json()

            if data['success']:
                count = data['data']['count']
                players = data['data']['players']
                
                result = ""
                for i in players:
                    result += f"Ник: {i['nickname']} [ID: {i['leaderID']}] Фракция: {i['fraction']}\n"
                    
                deputyList = disnake.Embed(
                    title=f'Список заместителей',
                    description=f':bust_in_silhouette: Всего заместителей - `{count}`\n```{result}```',
                    color=Color.main_color,
                    timestamp=datetime.now()
                )
                
                deputyList.set_footer(text=f'{interaction.author.id}')
                await asyncio.sleep(2)
                await interaction.edit_original_response(embed=deputyList)
                await add_log(self.bot, interaction.author, 'использовал команду', interaction.channel, f'/deputylist')


                logger.info(f'[getDeputyList] Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /deputylist')

                
            else:
                errorEmbed = disnake.Embed(
                    title=f"{data['message']} :x:",
                    color=Color.red
                )
                await interaction.edit_original_response(embed=errorEmbed)
                logger.error(f"[getDeputyList] [type:SEND] {data['message']}")

        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[getDeputyList] [type:GET] {ex}')


def setup(bot):
    bot.add_cog(DeputyList(bot))