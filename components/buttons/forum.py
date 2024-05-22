from utils import *
from config import Settings
from components.modals.forum import *

class ForumButtons(disnake.ui.View):
    def __init__(self) -> None:
        self.db = UsersDataBase()
        super().__init__(timeout=None)

    @disnake.ui.button(label="Посмотреть список", style=disnake.ButtonStyle.gray, custom_id="forum_list")
    async def forum_list(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            forum_list_get = await self.db.get_forum_list(interaction.author.guild.id)
            forum_list = ''
            

            if not forum_list_get :
                forum_list = '`Список пуст...`'

            else:
                for i, log in enumerate(forum_list_get, 1):
                    forum_list += f"`{i}. {log[1]}`\n"

            forumListEmbed = disnake.Embed(
                title='Список никнеймов',
                color=Color.main_color,
                description=f'{forum_list}'
            )
            await interaction.response.send_message(embed=forumListEmbed, ephemeral=True)
            
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])


    @disnake.ui.button(label="Добавить никнейм", style=disnake.ButtonStyle.green, custom_id="add_forum")
    async def add_forum(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_modal(modal=AddForum())
            
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

    @disnake.ui.button(label="Удалить никнейм", style=disnake.ButtonStyle.red, custom_id="delete_forum")
    async def delete_forum(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_modal(modal=DeleteForum())
            
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])