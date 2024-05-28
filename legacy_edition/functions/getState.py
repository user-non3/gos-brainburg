from utils import *
from components.buttons.PaginatorView import PaginatorView

async def getState(nickname: str, type: int, interaction: disnake.Interaction):
    if type == 1:
        try:
            response = requests.get(f'https://api.szx.su/estate?server_id=5&nickname={nickname}', headers=header_vprikol)
            data = response.json()

            embeds = []
            loop_count = 0
            n = 0
            text = ''
            for i in data['houses']:
                n += 1
                loop_count += 1
                text += f":id: ID: `{i['id']}`\n:pencil2: Имя: `{i['name']}`\n\n"
                if loop_count % 5 == 0 or loop_count - 1 == len(data['houses']) - 1:
                    embed = disnake.Embed(color=Color.main_color, title=f'Имущество {nickname}', timestamp=datetime.now())
                    embed.description = text
                    embeds.append(embed)
                    text = ''

            view = PaginatorView(embeds, interaction.author, True)
            return await interaction.edit_original_response(embed=embeds[0], view=view)

        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[admins] [type:GET] {ex}')
    else:
        return False