from utils import *
from config import Settings

class Admins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл admins.py успешно загружен')

    @commands.slash_command(description='Посмотреть администрацию онлайн')
    async def admins(self, interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                with open('utils/json/admins.json', 'r', encoding='utf-8') as file:
                    data_json = json.load(file)
                    arr = []

                adminsString = ', '.join([f'"{admin["nick"]}"' for admin in data_json])
                arr = f'[{adminsString}]'

                response = requests.get(f'https://api.szx.su/players?server_id=5&nicknames={arr}', headers=header_vprikol)
                data = response.json()
                admins = ""
                count = 1
                online = 0

                for admin, info in data['data'].items():
                    # if admin == "Nevermore_Nightmare":
                    #     print('Работает')

                    if data['data'][admin] != None:
                        admins += f"{count}. {admin} [{info['ingameId']}] \n"
                        count += 1
                        online += 1

                infoEmbed = disnake.Embed(
                    timestamp=datetime.now(),
                    title=f'Администрация онлайн',
                    color=Color.main_color,
                    description=f':space_invader: Всего в сети: `{online}`\n```{admins}```\nПоследнее обновление: <t:{data["updatedAt"]}:R>'
                )
                await interaction.edit_original_response(embed=infoEmbed)

            except Exception as ex:
                await errorCreator(interaction, ex)
                logger.error(f'[admins] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])
            
def setup(bot):
    bot.add_cog(Admins(bot))