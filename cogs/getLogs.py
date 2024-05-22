from utils import *
from config import Settings

class GetLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл getLogs.py успешно загружен')
    
    @commands.slash_command(description='Посмотреть логи')
    async def logs(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name'), limit: int = commands.Param(None, name='лимит', description='По умолчанию 15 строк')):
        user = await getUser(interaction.author)
        if user[6] > 2 or user[6] == 2:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'], ephemeral=True)
            try:
                if limit == None:
                    limit = 15

                request = requests.get(f"https://gos-brainburg.online/api/bot/getLogs?token={Settings.token_api}&leader={nick}&limit={limit}")
                data = request.json()

                if data['success']:
                    result = ""
                    for line in data['message']:
                        result += f"`{line}`\n"
                    
                    logsEmbed = disnake.Embed(
                        title=f'Просмотр логов — {nick}',
                        description=result,
                        color=Color.main_color,
                    )
                    await interaction.edit_original_response(embed=logsEmbed)
                    
                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    await interaction.response.send_message(embed=errorEmbed)
                    logger.error(f"[getLogs][CMD] [type:GET][SEND] {data['message']}")

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[getOnline][CMD] [type:GET] {ex}')
        
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])
            
def setup(bot):
    bot.add_cog(GetLogs(bot))