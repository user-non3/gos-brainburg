from utils import *
from config import *

class GetLogs(disnake.ui.View):
    def __init__(self, leader) -> None:
        self.leader = leader
        super().__init__(timeout=None)

    @disnake.ui.button(label="Посмотреть логи", style=disnake.ButtonStyle.grey, custom_id="check_logs")
    async def check_logs(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            try:
                request = requests.get(f"{api_url}/getLogs?token={api_token}&leader={self.leader}&limit=15")
                data = request.json()

                if data['success']:
                    result = ""
                    for line in data['message']:
                        result += f"`{line}`\n"
                    
                    logsEmbed = disnake.Embed(
                        title=f'Просмотр логов — {self.leader}',
                        description=result,
                        color=Color.main_color,
                        timestamp=datetime.now()
                    )
                    logsEmbed.set_footer(text=interaction.author.id)
                    await interaction.response.send_message(embed=logsEmbed, ephemeral=True)
                    
                else:
                    errorEmbed = disnake.Embed(
                        title=f"{data['message']} :x:",
                        color=Color.red
                    )
                    await interaction.response.send_message(embed=errorEmbed)
                    logger.error(f"[getLogs] [type:GET][SEND] {data['message']}")

            except Exception as ex:
                logger.error(f'[getLogs] [type:GET][BUTTON] {ex}')
            
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])