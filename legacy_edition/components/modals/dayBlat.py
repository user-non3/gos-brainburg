from utils import *

class ManageModal(disnake.ui.Modal):
    def __init__(self, type, fraction):
        self.type = type
        self.fraction = fraction
        self.db = UsersDataBase()

        if self.type == 2:
            components = [
                disnake.ui.TextInput(label="Введите ник игрока", placeholder='Пример Carl_Johnson', custom_id="player_nick", required=True)
            ]
        else:
            components = [
                disnake.ui.TextInput(label="Введите ник лидера", placeholder='Пример Nevermore_Nightmare', custom_id="leader_nick", required=True, value=None),
                disnake.ui.TextInput(label="Введите ник игрока", placeholder='Пример Carl_Johnson', custom_id="player_nick", required=True),
                disnake.ui.TextInput(label="Введите фракцию", placeholder='Пример LSFM, LSMC', custom_id="fraction", required=True),
                disnake.ui.TextInput(label="Введите ранг", placeholder='Пример 5-6, 7-8', custom_id="rank", required=True, max_length=3),
                disnake.ui.TextInput(label="Введите дату", placeholder='Пример 24.04.2024 13:37', custom_id="date", required=True, max_length=16)
            ]

        super().__init__(title="Создание записи", components=components, custom_id="edit_logs_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        if self.type == 1:
            leader_nick = interaction.text_values["leader_nick"]
            player_nick = interaction.text_values["player_nick"]
            fraction = interaction.text_values["fraction"]
            rank = interaction.text_values["rank"]
            date_time = interaction.text_values["date"]
            date = date_time.split(' ')
            
            await self.db.create_ranks_log(leader_nick, player_nick, fraction, rank, date[0], date[1], 'День блата', self.fraction)
            await interaction.response.send_message(f'Вы успешно создали запись с ником `{player_nick}`! :white_check_mark:', ephemeral=True)

        elif self.type == 2:
            player_nick = interaction.text_values["player_nick"]
            logs_list_get = await self.db.get_ranks_logs_list(self.fraction)
            if player_nick == logs_list_get[0][2]:
                await self.db.delete_ranks_log(player_nick, self.fraction)
                await interaction.response.send_message(f'Запись с ником `{player_nick}` была удалена! :white_check_mark:', ephemeral=True)

            else:
                await interaction.response.send_message('Такой записи с ником не нашлось! :x:', ephemeral=True)