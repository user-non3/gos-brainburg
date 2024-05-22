from utils import *

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл moderation.py успешно загружен')
    
    # @commands.slash_command(description="Заблокировать пользователя на сервере")
    # @commands.has_permissions(administrator=True)
    # async def ban(self, interaction, user: disnake.Member, *, reason=None):
    #     if reason == None:
    #         reason = 'Не указано'
        
    #     emb = disnake.Embed(
    #         title="Успешно ✅",
    #         color=Color.custom,
    #         description=f"Вы успешно забанили пользователя {user.mention}",
    #         timestamp=datetime.now()
    #     )
    #     emb.set_footer(text=f"Написал {interaction.author.name} | Arizona Bot")

    #     user_embed = disnake.Embed(
    #         title='Важно! 🛑',
    #         color=Color.red,
    #         description=f'Вы были забанены на нашем сервере по причине: {reason}\nАдминистратором: {interaction.author.mention}',
    #         timestamp=datetime.now()
    #     )

    #     user_embed.set_footer(text='')

    #     await interaction.guild.ban(user, reason=reason)
    #     await interaction.response.send_message(embed=emb)
    #     await interaction.response.user.send(embed=user_embed)

    # @commands.slash_command(description="Разблокировать пользователя на сервере")
    # @commands.has_permissions(administrator=True)
    # async def unban(self, interaction, user: disnake.Member):
    #     emb = disnake.Embed(
    #         title="Успешно ✅",
    #         color=disnake.Color.green(),
    #         description=f"Вы успешно разбанили пользователя {user.mention}"
    #         # timestamp=self.message.created_at
    #     )
    #     emb.set_footer(text=f"Написал {interaction.author.name} | Arizona Bot")

    #     user_embed = disnake.Embed(
    #         title='Важно! 🛑',
    #         color=Color.red,
    #         description=f'Вы были забанены на нашем сервере по причине: {reason}\nАдминистратором: {interaction.author.mention}\nЕсли вы не согласны с решением то оставьте жалобу на форуме!\n{Url.forum_url}'
    #     )

    #     user_embed.set_footer(text=footer)

    #     await interaction.guild.unban(user)
    #     await interaction.response.send_message(embed=emb)
    #     await interaction.response.user.send(embed=user_embed)

    @commands.slash_command(description="Замутить пользователя")
    @commands.has_permissions(administrator=True)
    async def mute(self, interaction, member: disnake.Member = commands.Param(name='пользователь', description='Выберите пользователя'),\
                      time: str = commands.Param(None, name='время', description='Время в минутах/секуднах'),\
                         reason = commands.Param(None, name='причина', description='Укажите причину')):
        if time == None:
            time = 10

        if reason == None:
            reason = 'Не указано'

        muteEmbed = disnake.Embed(
            title="Мут пользователя",
            color=Color.main_color,
            description=f"Администратор {interaction.author.mention} замутил пользователя {member.mention}\nВремя: `{time} минут` \nПричина: `{reason}`",
            timestamp=datetime.now()
        )
        muteEmbed.set_footer(text=f'{interaction.author.id}')
        await interaction.response.send_message(embed=muteEmbed)
        await member.timeout(reason=reason, duration=timedelta(minutes=int(time)))
        logger.info(f'Пользователь {interaction.author.name} [{interaction.author.id}] замутил пользователя {interaction.author.name} [{interaction.author.id}]')

    @commands.slash_command(description="Размутить пользователя")
    @commands.has_permissions(administrator=True)
    async def unmute(self, interaction, member: disnake.Member = commands.Param(name='пользователь', description='Выберите пользователя'),\
                        reason = commands.Param(None, name='причина', description='Напишите причину')):
        
        if reason == None:
            reason = 'Не указано'

        unMuteEmbed = disnake.Embed(
            title="Размут пользователя",
            color=Color.main_color,
            description=f"Администратор {interaction.author.mention} размутил пользователя {member.mention}\nПричина: `{reason}`",
            timestamp=datetime.now()
        )
        unMuteEmbed.set_footer(text=f'{interaction.author.id}')
        await interaction.response.send_message(embed=unMuteEmbed)
        await member.timeout(reason=reason, until=None)
        logger.info(f'Пользователь {interaction.author.name} [{interaction.author.id}] снял мут пользователю {interaction.author.name} [{interaction.author.id}]')

    @commands.slash_command(description="Очистить чат")
    @commands.has_permissions(administrator=True)
    async def clear(self, interaction, amount: int = commands.Param(None, name='количество', description='Укажите количество')):
        if amount == None:
            amount = 2

        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f'✅ Было очищено {amount} сообщений!')
        await asyncio.sleep(5)
        await interaction.channel.purge(limit=1)
        logger.info(f'Администратор {interaction.author.name} [{interaction.author.id}] очистил {amount} сообщений')

    # @commands.slash_command(description="Выдать WARN")
    # @commands.has_permissions(administrator=True)
    # async def warn(self, interaction, member: disnake.Member, amount: int):
    #     await self.db.create_table()
    #     if not member:
    #         member = interaction.author

    #     await self.db.add_user(member)
    #     await self.db.give_warn(member, amount)
    #     user = await self.db.get_user(member)

    #     embed = disnake.Embed(
    #         title="Выдача WARN",
    #         color=disnake.Color.yellow(),
    #         description=f"Администратор {interaction.author.mention} выдал WARN пользователю {member.mention}\nУ этого пользователя сейчас - {user[3]} WARN"
    #     )
    #     embed.set_footer(text=f'Отправитель @{interaction.author.name} | {Settings.username}')
    #     await interaction.response.send_message(embed=embed)

    # @commands.slash_command(description="Выдать WARN")
    # @commands.has_permissions(administrator=True)
    # async def unwarn(self, interaction, member: disnake.Member, amount: int):
    #     await self.db.create_table()
    #     if not member:
    #         member = interaction.author

    #     await self.db.add_user(member)
    #     await self.db.del_warn(member, amount)
    #     user = await self.db.get_user(member)

    #     embed = disnake.Embed(
    #         title="Снятие WARN'a",
    #         color=disnake.Color.yellow(),
    #         description=f"Администратор {interaction.author.mention} снял WARN пользователю {member.mention}\nУ этого пользователя сейчас - {user[3]} WARN"
    #     )
    #     embed.set_footer(text=f'Отправитель @{interaction.author.name} | {Settings.username}')
    #     await interaction.response.send_message(embed=embed)

    @commands.slash_command(description='Кикнуть пользователя')
    async def kick(self, interaction, member: disnake.Member = commands.Param(name='пользователь', description='Выберите пользователя'), reason = commands.Param(None, name='причина', description='Напишиту причину')):
        if reason == None:
            reason = 'Не указано'

        get_channel_id = await self.db.get_channel_id(7, interaction.author.guild)
        logs_channel = self.bot.get_channel(get_channel_id[0])

        kickEmbed = disnake.Embed(
            title='Кик пользователя',
            color=Color.main_color,
            description=f'Администратор {interaction.author.mention} кикнул пользователя {member.mention}\nПричина: `{reason}`',
            timestamp=datetime.now()
        )
        kickEmbed.set_footer(text=f'{interaction.author.id}')

        logEmbed = disnake.Embed(
            title='Кик пользователя',
            color=Color.red,
            description=f'**Администратор:** {interaction.author.mention}\n**Пользователь:** {member.mention}\n**Причина:** `{reason}`',
            timestamp=datetime.now()
        )
        logEmbed.set_footer(text='Members logs')

        if logs_channel == None:
            await member.kick(reason=reason)
            await interaction.response.send_message(embed=kickEmbed)
        
        else:
            await member.kick(reason=reason)
            await interaction.response.send_message(embed=kickEmbed)
            await logs_channel.send(embed=logEmbed)
            
        logger.info(f'Администратор {interaction.author.name} [{interaction.author.id}] кикнул пользователя {member.mention} [{member.id}] Причина: {reason}')

def setup(bot):
    bot.add_cog(Moderation(bot))