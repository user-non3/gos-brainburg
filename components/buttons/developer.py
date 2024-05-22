from utils import *
from config import Settings

class DevButtons(disnake.ui.View):
    def __init__(self, user) -> None:
        self.user = user
        self.db = UsersDataBase()
        super().__init__(timeout=None)

    @disnake.ui.button(label="Посмотреть логи", style=disnake.ButtonStyle.grey, custom_id="check_logs")
    async def check_logs(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.author.id in access_list:
            try:
                logs = await self.db.get_logs(self.user)
                logs_list = ''

                if not logs:
                    logs_list = '`Список пуст...`'

                else:
                    for i, log in enumerate(logs, 1):
                        logs_list += f"`{log[2]} {log[4]} [{log[5].split('.')[0]}]`\n"

                logsEmbed = disnake.Embed(
                    title=f'Просмотр логов',
                    color=Color.main_color,
                    timestamp=datetime.now(),
                    description=f'{logs_list}'
                )
                await interaction.response.send_message(embed=logsEmbed, ephemeral=True)

            except Exception as ex:
                logger.error(f'[getUserLogs] [type:GET][BUTTON] {ex}')
            
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])