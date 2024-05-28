from utils import *
from config import *

class Online(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл online.py успешно загружен')

    
    @commands.slash_command(name='online', description='Посмотреть недельный онлайн')
    async def __online(self, interaction, nick: str = commands.Param(name='ник', description='Формат Nick_Name')):
        await interaction.response.send_message(embed=EmbedsList['waitInfo'])
        try:
            r = requests.get(f"{api_url}/getOnline?token={api_token}&nick={nick}")
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
                await add_log(self.bot, interaction.author, 0, f'[{interaction.author.id}]', f'/online N:{nick}')
                logger.info(f'[getOnline] Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /online | ARG: {nick}')
                
            else:
                errorEmbed = disnake.Embed(
                    title=f"{data['message']} :x:",
                    color=Color.red
                )
                await interaction.edit_original_response(embed=errorEmbed)
                logger.error(f"[getOnline] [type:SEND] {data['message']}")

        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[getOnline] [type:GET] {ex}')
            
def setup(bot):
    bot.add_cog(Online(bot))