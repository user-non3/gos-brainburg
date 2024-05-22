from utils import *
from components.buttons.logs import LogsButtons
        
class ChoiceButtons(disnake.ui.View):
    def __init__(self):
        self.db = UsersDataBase()
        super().__init__(timeout=None)

    @disnake.ui.button(label="Настройка логов", style=disnake.ButtonStyle.gray, custom_id="logs_settings")
    async def logs_settings(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        embedInfo = disnake.Embed(
            title='Панель настроек логов',
            color=Color.main_color,
            description='Выберите кнопку что бы изменить настройки\n\n**Что бы получить ID канала нужно включить режим Разработчика\nНастройки > Расширенные > Режим Разработчика**',
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embedInfo, view=LogsButtons(), ephemeral=True)

class ServerSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл serverSettings.py успешно загружен')

    @commands.slash_command(name='settings', description='Панель настроек сервера')
    async def server_settings(self, interaction):
        if interaction.author.id == interaction.guild.owner.id or interaction.author.id in access_list: 
            embedInfo = disnake.Embed(
                color=Color.main_color,
                description='Выберите кнопку что бы открыть меню настроек\n',
                timestamp=datetime.now()
            )
            embedInfo.set_author(name=f'Панель настроек сервера {interaction.author.guild.name}', icon_url=interaction.author.guild.icon)
            embedInfo.set_image(url='https://images-ext-2.discordapp.net/external/_xP3aYiyMM6cHa6-yAo_QAUm8IMwyJ6Y9m6rP19WH0g/https/images-ext-2.discordapp.net/external/0AmbBsPa4GWh0kIPtCWje6z8IFI38cc43W8YbGHldhU/https/images-ext-2.discordapp.net/external/z96taxZ7kvTVwGuR4lXY4MwRJO9KnvZzzDd7kTq59sY/https/support.discordapp.com/hc/en-us/article_attachments/206303208/eJwVyksOwiAQANC7sJfp8Ke7Lt15A0MoUpJWGmZcGe-ubl_eW7zGLmaxMZ80A6yNch-rJO4j1SJr73Uv6Wwkcz8gMae8HeXJBOjC5NEap42dokUX_4SotI8GVfBaYYDldr3n3y_jomRtD_H5ArCeI9g.zGz1JSL-9DXgpkX_SkmMDM8NWGg.gif')
            await interaction.response.send_message(embed=embedInfo, view=ChoiceButtons(), ephemeral=True)
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'], ephemeral=True)

def setup(bot):
    bot.add_cog(ServerSettings(bot))