from functions.getJson import get_json
from utils import *

class ViewMenu(disnake.ui.View):
    def __init__(self, author):
        super().__init__(timeout = None)
        self.author = author
        self.add_item(disnake.ui.Button(label="Поддержка", style=disnake.ButtonStyle.link, url='https://discord.gg/Jb65ZVyJZW'))
        self.add_item(disnake.ui.Button(label="Gos Brainburg", style=disnake.ButtonStyle.link, url='https://gos-brainburg.ru'))
        
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл utils.py успешно загружен')

    @commands.slash_command(description="Получить список команд")
    async def help(self, interaction):
        helpEmbed = disnake.Embed(
            description=f'### Разработчики\n`nedust` - Web/API Разработчик\n`user.none` - Discord Разработчик\n### Команды\n{get_json(1)}',
            color=Color.main_color,
            timestamp=datetime.now()
        )
        helpEmbed.set_footer(text=f'{interaction.author.id}')
        await interaction.response.send_message(embed=helpEmbed, ephemeral=True, view=ViewMenu(interaction.author))

    @commands.slash_command(name='ip', description='Информация об IP')
    async def __ip(self, interaction, address: str = commands.Param(name='адрес', description='Формат 127.0.0.1') ):
        ip_request = requests.get(f'http://ip-api.com/json/{address}')
        data = ip_request.json()

        if data['status'] == 'success':
            ipEmbed = disnake.Embed(
                title='Информация об IP',
                timestamp=datetime.now(),
                color=Color.main_color
            )
            ipEmbed.add_field(name='Страна (Код)', value=f"{data['country']} ({data['countryCode']})")
            ipEmbed.add_field(name='Регион (Имя)', value=f"{data['region']} ({data['regionName']})")
            ipEmbed.add_field(name='Город', value=data['city'])
            ipEmbed.add_field(name='Lat', value=data['lat'])
            ipEmbed.add_field(name='Lon', value=data['lon'])
            ipEmbed.add_field(name='Google Map', value=f"[Открыть](https://maps.google.com/?q={data['lat']},{data['lon']})")

            ipEmbed.set_footer(text=f'{interaction.author.id}')
            await interaction.response.send_message(embed=ipEmbed, ephemeral=True)
            await add_log(self.bot, interaction.author, 0, f'[{interaction.author.id}]', f'/ip {address}')
            logger.info(f'Пользователь {interaction.author.name} [{interaction.author.id}] использовал команду /ip [{address}]')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorAccess'], ephemeral=True)

    @commands.slash_command(name='servers', description='Статус серверов')
    async def __servers(self, interaction, game=commands.Param(name='проект', description='Выберите проект', choices=['Arizona RP', 'Arizona Mobile'])):
        await interaction.response.send_message(embed=EmbedsList['waitInfo'], ephemeral=True)

        try:
            request_one = requests.get(f"https://api2.gerstlix.com/v1/server.getStatus/?token={gerstlix_token}")
            data = request_one.json() 

            if data['success']:
                arz = data['data']['Arizona RP']
                arzMobile = data['data']['Arizona Mobile']
                result = ""
                all_online = 0
                if game == 'Arizona RP':
                    for i in arz:
                        serverName = i['serverName']
                        online = i['online']
                        maxPlayers = i['maxPlayers']
                        vkGroup = i['vkGroup']
                        access = ':white_check_mark:' if online > 0 else ':x'
                        all_online += online

                        result += f"{access} [{serverName}]({vkGroup}) - Онлайн: `{online}` из `{maxPlayers}`\n"
                        
                elif game =='Arizona Mobile':
                    for i in arzMobile:
                        serverName = i['serverName']
                        online = i['online']
                        maxPlayers = i['maxPlayers']
                        vkGroup = i['vkGroup']
                        access = ':white_check_mark:' if online > 0 else ':x'
                        all_online += online
                            
                        result += f"{access} [{serverName}]({vkGroup}) - Онлайн: `{online}` из `{maxPlayers}`\n"
                    
                serverEmbed = disnake.Embed(
                    title=f'Статус серверов {game}',
                    description=f'{result}\n:dizzy: **Общий онлайн:** `{all_online}`',
                    timestamp=datetime.now(),
                    color=Color.green
                )
                serverEmbed.set_footer(text=f'{interaction.author.id}')
                await add_log(self.bot, interaction.author, 0, f'[{interaction.author.id}]', f'/servers PROJECT:{game}')

                await interaction.edit_original_response(embed=serverEmbed)
            
        except Exception as ex:
            await errorCreator(interaction, ex)
            print(Fore.RED + f'[ERROR] In utils.py > /servers: {ex}')

    @commands.slash_command(name='fractions', description='ID Фракций')
    @commands.guild_only()
    async def __fractions(self, interaction):
        fractionEmbed = disnake.Embed(
            title=f"ID Фракций",
            color=disnake.Color.light_grey(),
            timestamp=datetime.now(),
            description=f'```{get_json(2)}```'
        )
        fractionEmbed.set_footer(text=f'{interaction.author.id}')
        await add_log(self.bot, interaction.author, 0, f'[{interaction.author.id}]', f'/fractions')
        await interaction.response.send_message(embed=fractionEmbed, ephemeral=True)

def setup(bot):
    bot.add_cog(Utils(bot))