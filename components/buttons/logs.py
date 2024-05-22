from utils import *
from components.modals.logs import LogsModal

class LogsButtons(disnake.ui.View):
    def __init__(self):
        self.db = UsersDataBase()
        super().__init__(timeout=None)

    @disnake.ui.button(label="Входы", style=disnake.ButtonStyle.gray, custom_id="members_join")
    async def members_join(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(1, interaction.guild)
        await interaction.response.send_modal(LogsModal(1, channel_id))
        
    @disnake.ui.button(label="Выходы", style=disnake.ButtonStyle.gray, custom_id="members_leave")
    async def members_leave(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(2, interaction.guild)
        await interaction.response.send_modal(LogsModal(2, channel_id))

    @disnake.ui.button(label="Изменение сообщений", style=disnake.ButtonStyle.gray, custom_id="messages_edit")
    async def messages_delete(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(3, interaction.guild)
        await interaction.response.send_modal(LogsModal(3, channel_id))

    @disnake.ui.button(label="Удаление сообщений", style=disnake.ButtonStyle.gray, custom_id="messages_delete")
    async def messages_edit(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(4, interaction.guild)
        await interaction.response.send_modal(LogsModal(4, channel_id))

    @disnake.ui.button(label="Баны", style=disnake.ButtonStyle.gray, custom_id="members_ban")
    async def members_ban(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(5, interaction.guild)
        await interaction.response.send_modal(LogsModal(5, channel_id))

    @disnake.ui.button(label="Разбаны", style=disnake.ButtonStyle.gray, custom_id="members_unban")
    async def members_unban(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(6, interaction.guild)
        await interaction.response.send_modal(LogsModal(6, channel_id))

    @disnake.ui.button(label="Кик", style=disnake.ButtonStyle.gray, custom_id="members_kick")
    async def members_kick(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(7, interaction.guild)
        await interaction.response.send_modal(LogsModal(7, channel_id))

    @disnake.ui.button(label="Роли", style=disnake.ButtonStyle.gray, custom_id="members_roles")
    async def members_roles(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        channel_id = await self.db.get_channel_id(8, interaction.guild)
        await interaction.response.send_modal(LogsModal(8, channel_id))

    @disnake.ui.button(label="Очистить все", style=disnake.ButtonStyle.red, custom_id="clear_all")
    async def clear_all(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(LogsModal(10, 1))