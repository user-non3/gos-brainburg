from utils import *

class AddForum(disnake.ui.Modal):
    def __init__(self):
        self.db = UsersDataBase()

        components = [
            disnake.ui.TextInput(label="Введите никнейм", placeholder='Пример: Nevermore_Nightmare', custom_id="nickname", max_length=32)
        ]

        super().__init__(title="Добавление никнейма", components=components, custom_id="add_forum_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        nickname = interaction.text_values["nickname"]
        # try:
        #     nick = nickname.split('_')
        
        # except:
        #     await interaction.response.send_message('Введите ник в формате `Nick_Name` :x:', ephemeral=True)
        
        # if nickname != f"{nick[0]}_{nick[1]}":
        #     await interaction.response.send_message('Введите ник в формате `Nick_Name` :x:', ephemeral=True)

        # else:
        await self.db.add_forum(interaction.author.guild.id, nickname)
        await interaction.response.send_message(f"Вы успешно **добавили** никнейм `{nickname}` для поиска жалоб. :white_check_mark:", ephemeral=True)

class DeleteForum(disnake.ui.Modal):
    def __init__(self):
        self.db = UsersDataBase()

        components = [
            disnake.ui.TextInput(label="Введите слово 'Очистить'", placeholder='Пример: Nevermore_Nightmare', custom_id="nickname", max_length=32)
        ]

        super().__init__(title="Удаление никнейма", components=components, custom_id="delete_forum_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        nickname = interaction.text_values["nickname"]
        await interaction.response.send_message(f"Вы успешно **удалили** никнейм `{nickname}` из поиска жалоб. :white_check_mark:", ephemeral=True)
