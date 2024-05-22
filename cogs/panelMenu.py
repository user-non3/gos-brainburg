from utils import *
from components.buttons.dayBlat import ManageButtons

class ChoiceButtons(disnake.ui.View):
    def __init__(self, user_access):
        self.db = UsersDataBase()
        self.access = user_access
        super().__init__(timeout=None)

    @disnake.ui.button(label="День блата", style=disnake.ButtonStyle.gray, custom_id="day_blat")
    async def day_blat(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.access > 1:
            embedInfo = disnake.Embed(
                title='Меню управления дня блата',
                color=Color.main_color,
                description='Выберите кнопку',
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=embedInfo, view=ManageButtons(), ephemeral=True)
        
        else:
            await interaction.response.send_message('У вас нету доступа к этому разделу!', ephemeral=True)

    @disnake.ui.button(label="Состав", style=disnake.ButtonStyle.gray, custom_id="team")
    async def team(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await self.db.get_user(interaction.author)
        team_list_get = await self.db.get_team_list(user[4])
        team_list = ''

        if not team_list_get:
            team_list = '`Список пуст...`'

        else:
            for i, team in enumerate(team_list_get, 1):
                if team[4] == 0:
                    team_list = '`Не найдено следящих в данной фракции!`'

                else:
                    team_list += f"`{i}. {team[3]} | {GetJobNameByID[team[5]]} | Доступ: {team[6]} LVL`\n"

        teamListEmbed = disnake.Embed(
            title='Состав следящих',
            color=Color.main_color,
            description=f'{team_list}'
        )
        await interaction.response.send_message(embed=teamListEmbed, ephemeral=True)

    @disnake.ui.button(label="Лидеры", style=disnake.ButtonStyle.gray, custom_id="leader", disabled=True)
    async def leader(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        pass

    @disnake.ui.button(label="Заместители", style=disnake.ButtonStyle.gray, custom_id="zams", disabled=True)
    async def zams(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        pass

class PanelMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл panelMenu.py успешно загружен')

    
    @commands.slash_command(name='panel', description='Панель следящих')
    async def panel_menu(self, interaction):
        user = await getUser(interaction.author)

        if user[6] > 1 or user[6] != 0 or interaction.author.id in access_list: 
            embedInfo = disnake.Embed(
                color=Color.main_color,
                description=f'Добро пожаловать в панель **{user[3]}! [{user[6]} LVL]**\n',
                timestamp=datetime.now()
            )
            embedInfo.set_author(name=f'Панель следящих {GetFullFractionNameByID[user[4]]}', icon_url=interaction.author.guild.icon)
            embedInfo.set_image(url='https://images-ext-2.discordapp.net/external/_xP3aYiyMM6cHa6-yAo_QAUm8IMwyJ6Y9m6rP19WH0g/https/images-ext-2.discordapp.net/external/0AmbBsPa4GWh0kIPtCWje6z8IFI38cc43W8YbGHldhU/https/images-ext-2.discordapp.net/external/z96taxZ7kvTVwGuR4lXY4MwRJO9KnvZzzDd7kTq59sY/https/support.discordapp.com/hc/en-us/article_attachments/206303208/eJwVyksOwiAQANC7sJfp8Ke7Lt15A0MoUpJWGmZcGe-ubl_eW7zGLmaxMZ80A6yNch-rJO4j1SJr73Uv6Wwkcz8gMae8HeXJBOjC5NEap42dokUX_4SotI8GVfBaYYDldr3n3y_jomRtD_H5ArCeI9g.zGz1JSL-9DXgpkX_SkmMDM8NWGg.gif')
            await interaction.response.send_message(embed=embedInfo, view=ChoiceButtons(user[6]))
            await asyncio.sleep(30)
            await interaction.delete_original_message()

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

def setup(bot):
    bot.add_cog(PanelMenu(bot))