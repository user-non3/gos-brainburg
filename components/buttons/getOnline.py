from utils import *
from config import Settings
from components.modals.dayBlat import ManageModal

class GetOnline(disnake.ui.View):
    def __init__(self, fraction_id, type) -> None:
        self.fraction_id = fraction_id
        self.type = type
        super().__init__(timeout=None)

    @disnake.ui.button(label="Посмотреть онлайн за 7 дней", style=disnake.ButtonStyle.grey, custom_id="check_online")
    async def check_online(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            if self.type == 1:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getLeader?token={Settings.api_token}&fraction={self.fraction_id}")
            
            elif self.type == 2:    
                r = requests.get(f"https://gos-brainburg.online/api/bot/getDeputy?token={Settings.api_token}&fraction={self.fraction_id}")
                
            elif self.type == 3:
                r = requests.get(f"https://gos-brainburg.online/api/bot/getMinister?token={Settings.api_token}&fraction={self.fraction_id}")
            
            data = r.json()

            if data['success']:
                online = data['data']['online']
                allOnline = data['data']['onlineAll']
                
                result = ""
                for date, value in online.items():
                    new = date.split('-')
                    result += f"{new[2]}.{new[1]}.{new[0]} - {value}\n"
                
                onlineEmbed = disnake.Embed(
                    title=f'Просмотр онлайна',
                    description=f':clock4: **Общий онлайн:** `{allOnline}`\n```{result}```',
                    color=Color.main_color,
                    timestamp=datetime.now()
                )
                onlineEmbed.set_footer(text=f'{interaction.author.name}')
                await interaction.response.send_message(embed=onlineEmbed, ephemeral=True)
                
            else:
                errorEmbed = disnake.Embed(
                    title=f"{data['message']} :x:",
                    color=Color.red
                )
                await interaction.response.send_message(embed=errorEmbed)
                logger.error(f"[getOnline] [type:GET][BUTTON] {data['message']}")

        except Exception as ex:
            logger.error(f'[getOnline] [type:GET][BUTTON] {ex}')