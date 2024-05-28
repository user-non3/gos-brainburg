from utils import *
from config import *

class GetServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл getServer.py успешно загружен')
    
    @commands.slash_command(name='server', description='Посмотреть инфо о сервере')
    async def __server(self, interaction, server: int = commands.Param(name='сервер', description='От 1 до 29')):
        if server > 30:
            return await interaction.response.send_message('Укажите сервер не более 30!', ephemeral=True)
        
        await interaction.response.send_message(embed=EmbedsList['waitInfo'], ephemeral=True)

        try:
            response = requests.get('https://arizona-ping.react.group/desktop/ping/Arizona/ping.json')
            data = response.json()
            online = ''
            count = 1
            for obj in data['query']:
                if obj['number'] == server:

                    for i in (obj['plotPoints']):
                        online += f"{count}) {datetime.fromtimestamp(i['time']).strftime('%H:%M:%S')} - {i['online']} \n"
                        count += 1
            
            if obj['password']:
                password = 'Установлен'

            else:
                password = 'Не установлен'

            if obj['online'] < 0:
                online_server = 'Сервер выключен! ❌'

            else:
                online_server = f"{obj['online']}/1000"

            infoEmbed = disnake.Embed(
                title=f'Информация о сервере {GetServerNameByID[server]} {GetServerIconByID[server]}',
                color=Color.main_color,
                timestamp=datetime.now(),
                description=f"**Онлайн:** `{online_server}`\n**Пароль:** `{password}`\n**Адресс:** `{obj['ip']}:{obj['port']}`\n**Паблик VK:** [Перейти]({obj['vk']})\n\n```История онлайна:\n\n{online}```"
            )
            await add_log(self.bot, interaction.author, 'использовал команду', interaction.channel, f'/server ID:{server}')


            await interaction.edit_original_response(embed=infoEmbed)

        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[getServer] [type:GET] {ex}')
            
def setup(bot):
    bot.add_cog(GetServer(bot))