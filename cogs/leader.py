from utils import *
from config import Settings
from components.buttons.getLogs import GetLogs
from components.buttons.getOnline import GetOnline
from functions.getUser import getUser

class Leader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл leader.py успешно загружен')

    @commands.slash_command(name='leader', description='Информация о лидере')
    async def get_leader(self, interaction, fraction: int = commands.Param(name='фракция', description='ID Фракции')):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getLeader?token={Settings.token_api}&fraction={fraction}")
                data = r.json()

                if data['success']:
                    accid = data['data']['userID']
                    nickname = data['data']['nickname']
                    postdate = data['data']['postdate']
                    postreason = data['data']['postreason']
                    preds = data['data']['preds']
                    vigs = data['data']['vigs']
                    balls = data['data']['balls']
                    inactiveDays = data['data']['alldays']
                    lastInactive = data['data']['lastinactive']
                    
                    if data['data']['lastinactive'] == None:
                        inActive = '\n'
                    
                    else:
                        inActive = f'\n:exclamation: **Неактив до** `{lastInactive}`'
                    
                    leaderEmbed = disnake.Embed(
                        title=f'Информация о Лидере на сервере {GetServerNameByID[5]} {GetServerIconByID[5]}',
                            description=f'{inActive}\n\n:crystal_ball: **Ник:** `{nickname}`\n:briefcase: **Фракция:** `{GetFractionNameByID[fraction]}`\n\
                            :warning: **Предупреждения:** `{preds}`\n:no_entry_sign: **Выговоры:** `{vigs}`\n:gem: **Баллы:** `{balls}`\
                            \n:pushpin: **Способ постановления:** `{postreason}`\n:date: **Дата постановления:** `{postdate}`\n:calendar: **На должносте:** `{inactiveDays} дня(ей)`',
                        color=Color.main_color,
                        timestamp=datetime.now()
                    )
                    leaderEmbed.set_footer(text=f'{interaction.author.id}')
                    await asyncio.sleep(2)
                    await interaction.edit_original_response(embed=leaderEmbed, view=GetLogs(nickname))
                    logger.info(f'[getLeader] {interaction.author.name} [{interaction.author.id}] | {nickname} [ID: {accid}] - {GetFractionNameByID[fraction]} [ID: {fraction}]')

                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    await interaction.edit_original_response(embed=errorEmbed)
                    logger.error(f"[getLeader] [type:SEND] {data['message']}")

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[getLeader] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

def setup(bot):
    bot.add_cog(Leader(bot))