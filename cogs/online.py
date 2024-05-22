from utils import *
from config import Settings

class Online(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл online.py успешно загружен')

    
    @commands.slash_command(description='Посмотреть недельный онлайн')
    async def online(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name')):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getOnline?token={Settings.token_api}&nick={nick}")
                data = r.json()

                if data['success']:
                    online = data['data']['online']
                    allOnline = data['data']['onlineAll']
                    
                    result = ""
                    for date, value in online.items():
                        new = date.split('-')
                        result += f"{new[2]}.{new[1]}.{new[0]} - {value}\n"
                    
                    onlineEmbed = disnake.Embed(
                        title=f'Просмотр онлайна {nick}',
                        description=f':clock4: **Общий онлайн:** `{allOnline}`\n```{result}```',
                        color=Color.main_color,
                        timestamp=datetime.now()
                    )
                    onlineEmbed.set_footer(text=f'{interaction.author.id}')
                    await interaction.edit_original_response(embed=onlineEmbed)
                    logger.info(f'[getOnline] Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /online | ARG: {nick}')
                    
                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    await interaction.edit_original_response(embed=errorEmbed)
                    logger.error(f"[getOnline] [type:SEND] {data['message']}")

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[getOnline] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])
            
def setup(bot):
    bot.add_cog(Online(bot))