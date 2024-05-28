from utils import *

class Button(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='📢', style=disnake.ButtonStyle.grey, custom_id='news_bot')
    async def news_bot(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        role = interaction.guild.get_role(1236240341363982336)
        if role in interaction.author.roles:
            await interaction.author.remove_roles(role)
            await interaction.response.send_message(f'Вы успешно сняли роль {role.mention} :white_check_mark:', ephemeral=True)

        else:
            await interaction.author.add_roles(role)
            await interaction.response.send_message(f'Вы успешно добавили роль {role.mention} :white_check_mark:', ephemeral=True)

    @disnake.ui.button(label='🌐', style=disnake.ButtonStyle.grey, custom_id='news_site')
    async def news_site(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        role = interaction.guild.get_role(1236271282497261568)
        if role in interaction.author.roles:
            await interaction.author.remove_roles(role)
            await interaction.response.send_message(f'Вы успешно сняли роль {role.mention} :white_check_mark:', ephemeral=True)

        else:
            await interaction.author.add_roles(role)
            await interaction.response.send_message(f'Вы успешно добавили роль {role.mention} :white_check_mark:', ephemeral=True)
        
class ButtonRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command()
    async def role(self, ctx):
        if ctx.author.id in access_list:
            role_bot = ctx.guild.get_role(1236240341363982336)
            role_site = ctx.guild.get_role(1236271282497261568)
            infoEmbed = disnake.Embed(
                title='Роли на сервере',
                description=f'{role_bot.mention} — Уведомления об обновлениях Бота\n{role_site.mention} — Уведомления об обновлениях Сайта',
                color=Color.main_color
            )
            await ctx.send(embed=infoEmbed, view=Button())

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return
        
        self.bot.add_view(Button(), message_id=1236245271604629564)
    
def setup(bot):
    bot.add_cog(ButtonRole(bot))