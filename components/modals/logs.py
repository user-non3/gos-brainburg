from utils import *

class LogsModal(disnake.ui.Modal):
    def __init__(self, type, now_id):
        self.type = type
        self.now_id = now_id
        self.db = UsersDataBase()

        if self.type == 10:
            components = [
                disnake.ui.TextInput(label="Введите слово 'Очистить'", placeholder='Очистить', custom_id="id", max_length=8)
            ]
        else:
            if self.now_id[0] == 0:
                now_id_text = 'Не установлен'
            
            else:
                now_id_text = f'Установлен на {self.now_id[0]}'

            components = [
                disnake.ui.TextInput(label="Введите ID канала", placeholder=now_id_text, custom_id="id")
            ]

        super().__init__(title="Настройка логов", components=components, custom_id="edit_logs_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        set_id = interaction.text_values["id"]
        if self.type == 10:
            if set_id == 'Очистить':
                await self.db.set_logs_channel(10, 0, interaction.guild.id)
                await interaction.response.send_message(f"Вы успешно очистили все каналы :white_check_mark:", ephemeral=True)
            else:
                await interaction.response.send_message("Введите не правильно ввели слово! :x:", ephemeral=True)

        else :
            if int(set_id):
                await self.db.set_logs_channel(self.type, set_id, interaction.guild.id)
                await interaction.response.send_message(f"Вы успешно изменили канал на <#{set_id}> :white_check_mark:", ephemeral=True)
            else:
                await interaction.response.send_message("Введите ID канала в числовом формате! :x:", ephemeral=True)