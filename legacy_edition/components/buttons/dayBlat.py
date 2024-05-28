from utils import *
from components.modals.dayBlat import ManageModal

class ManageButtons(disnake.ui.View):
    def __init__(self):
        self.db = UsersDataBase()
        super().__init__(timeout=None)

    @disnake.ui.button(label="Список", style=disnake.ButtonStyle.gray, custom_id="rank_logs_list")
    async def rank_logs_list(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await self.db.get_user(interaction.author)
        logs_list_get = await self.db.get_ranks_logs_list(user[4])
        logs_list = ''

        if not logs_list_get:
            logs_list = '`Список пуст...`'

        else:
            for i, log in enumerate(logs_list_get, 1):
                logs_list += f"`{i}. {log[2]} | {log[3]} | {log[4]} | {log[5]} {log[6]}`\n"

        logsListEmbed = disnake.Embed(
            title='Список записей',
            color=Color.main_color,
            description=f'{logs_list}'
        )
        await interaction.response.send_message(embed=logsListEmbed, ephemeral=True)
        
    @disnake.ui.button(label="Создать запись", style=disnake.ButtonStyle.green, custom_id="create_log")
    async def create_log(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await self.db.get_user(interaction.author)
        await interaction.response.send_modal(modal=ManageModal(1, user[4]))

    @disnake.ui.button(label="Удалить запись", style=disnake.ButtonStyle.red, custom_id="delete_log")
    async def delete_log(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await self.db.get_user(interaction.author)
        await interaction.response.send_modal(modal=ManageModal(2, user[4]))