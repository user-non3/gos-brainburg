from utils import *
import locale

class Find(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл find.py успешно загружен')

    @commands.slash_command(description='Информация об игроке')
    async def find(self, interaction, nick: str = commands.Param(name='никнейм', description='Формат Nick_Name')):
        await interaction.response.send_message(embed=EmbedsList['waitInfo'])
        try:
            result = await vprikol.get_player_information(5, nick)

            individual_account = "Нет" if result.individual_account == None else result.individual_account
            account_id = "Неизвестно" if result.account_id is None else result.account_id

            all_money = "{:,}".format(result.total_money)
            cash = "{:,}".format(result.cash)
            bank = "{:,}".format(result.bank)
            deposit = "{:,}".format(result.deposit)

            status = ":no_entry: Состояние: `Не в сети`" if result.is_online == False else f":white_check_mark: Состояние: `В сети [{result.is_online}]`"

            findEmbed = disnake.Embed(
                title=f'Информация о {nick}',
                description=f':gear: ID аккаунта: `{account_id}`\n:floppy_disk: Уровень: `{result.lvl}`\n\
                    :crown: Уровень VIP: `{result.vip_label}`\n:mobile_phone: Номер телефона: `{result.phone_number}`\n{status}\n\n\
                    :moneybag: Всего денег: `{all_money}$`\n:dollar: Наличные: `{cash}$`\n:bank: Деньги в банке: `{bank}$`\n\
                    :credit_card: Депозит: `{deposit}$`\n:money_with_wings: Личный счет: `{individual_account}`\n\n:office: Работа: `{result.job_label}`\n\
                    :briefcase: Организация: `{result.org_label}`\n:busts_in_silhouette: Должность: `{result.rank_label} [{result.rank_number}]`\n\n:hourglass: Обновлено: <t:{result.updated_at}:R>',
                color=Color.main_color,
                timestamp=datetime.now()
            )
            findEmbed.set_footer(text=interaction.author.id)
            await interaction.edit_original_response(embed=findEmbed)

        except Exception as ex:
            await errorCreator(interaction, ex)
            logger.error(f'[find] [type:GET] {ex}')

def setup(bot):
    bot.add_cog(Find(bot))