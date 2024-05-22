from utils import *
from config import Settings
from components.buttons.getOnline import GetOnline

class Minister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл minister.py успешно загружен')

    @commands.slash_command(description='Информация о Министре')
    async def minister(self, interaction, fraction: int = commands.Param(name='фракция', description='ID Министерства')):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getMinister?token={Settings.token_api}&fraction={fraction}")
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
                        inActive = f'\n:exclamation: **Неактив до `{lastInactive}`**'
                    
                    ministerEmbed = disnake.Embed(
                        title=f'Информация о Министре на сервере {GetServerNameByID[5]} {GetServerIconByID[5]}',
                        description=f'{inActive}\n\n:crystal_ball: **Ник:** `{nickname}`\n:office: **Министерство:** `{GetFractionNameByID[fraction]}`\n\
                            :warning: **Предупреждения:** `{preds}`\n:no_entry_sign: **Выговоры:** `{vigs}`\n:gem: **Баллы:** `{balls}`\
                            \n:pushpin: **Способ постановления:** `{postreason}`\n:date: **Дата постановления:** `{postdate}`\n:calendar: **На должносте:** `{inactiveDays} дня(ей)`',
                        color=Color.main_color,
                        timestamp=datetime.now()
                    )
                    ministerEmbed.set_footer(text=interaction.author.id)
                    await asyncio.sleep(2)
                    await interaction.edit_original_response(embed=ministerEmbed, view=GetOnline(fraction, 3))
                    logger.info(f'[getMinister] {interaction.author.name} [{interaction.author.id}] | {nickname} [ID: {accid}] - {GetFractionNameByID[fraction]} [ID: {fraction}]')

                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    await interaction.edit_original_response(embed=errorEmbed)
                    logger.error(f"[getMinister] [type:SEND] {data['message']}")

            except Exception as ex:
                await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description=f'```{ex}```', color=Color.red))
                logger.error(f'[getMinister] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

def setup(bot):
    bot.add_cog(Minister(bot))