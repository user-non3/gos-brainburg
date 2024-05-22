from utils import *
from utils.forum_module import forum
from components.buttons.forum import ForumButtons
import re

class ViewMenu(disnake.ui.View):
    def __init__(self, author, id):
        super().__init__(timeout = None)
        self.author = author
        self.id = id
        self.add_item(disnake.ui.Button(label="Перейти к жалобе", style=disnake.ButtonStyle.link, url=f'https://forum.arizona-rp.com/threads/{self.id}/'))

api = arz_api.ArizonaAPI(user_agent=bypass.user_agent, cookie=cookies)

class Forum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл forumPanel.py успешно загружен')

    @commands.slash_command()
    async def forum(self, interaction):
        user = await getUser(interaction.author)
        server = await self.db.get_guild(interaction.author.guild)
        if user[6] > 1 or user[6] == 1:
            if server[11]:
                forumEmbed = disnake.Embed(
                    title='Панель форума',
                    color=Color.main_color,
                    description='Добро пожаловать в панель настройки Форума!'
                )
                await interaction.response.send_message(embed=forumEmbed, view=ForumButtons())

            else:
                await interaction.response.send_message(embed=EmbedsList['noPremium'])

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])

def setup(bot):
    bot.add_cog(Forum(bot))