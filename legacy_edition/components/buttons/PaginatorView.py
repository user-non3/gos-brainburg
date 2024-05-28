from utils import *

class PaginatorView(disnake.ui.View):
    def __init__(self, embeds, author, footer: bool, timeout=30.0):
        self.embeds = embeds  # Список эмбедов для отображения.
        self.author = author  # Автор сообщения.
        self.footer = footer  # Флаг для отображения подвала с номером страницы.
        self.timeout = timeout  # Время ожидания в секундах для автоматической очистки интерфейса.
        self.page = 0  # Текущая страница (индекс) из списка эмбедов.
        super().__init__(timeout=self.timeout)

        if self.footer:
            for emb in self.embeds:
                emb.set_footer(text=f'Страница {self.embeds.index(emb) + 1} из {len(self.embeds)}')

    @disnake.ui.button(label='◀️', style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == 0:
                self.page = len(self.embeds) - 1
            else:
                self.page -= 1
        else:
            return

        await self.button_callback(interaction)

    @disnake.ui.button(label='▶️', style=disnake.ButtonStyle.grey)
    async def next(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == len(self.embeds) - 1:
                self.page = 0
            else:
                self.page += 1
        else:
            return

        await self.button_callback(interaction)

    async def button_callback(self, interaction):
        if self.author.id == interaction.author.id:
            await interaction.response.edit_message(embed=self.embeds[self.page])
        else:
            return await interaction.response.send_message('Вы не можете использовать эту кнопку!', ephemeral=True)