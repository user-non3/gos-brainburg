from utils import *

async def errorCreator(interaction: disnake.Interaction, message):
    embed = disnake.Embed(
        title='Ошибка при выполнение команды!',
        description=f'```{message}```',
        color=Color.red
    )
    return await interaction.edit_original_response(embed=embed)