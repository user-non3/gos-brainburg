from utils import *

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False
        self.db = UsersDataBase()

    @commands.Cog.listener()    
    async def on_ready(self):
        logger.debug('Файл ивентов успешно загружен')
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logger.info(f"[ON_GUILD_JOIN] Бот был добавлен на сервер '{guild.name}' [{guild.id}]")
        log_channel_id = 1217135396618506280
        
        logEmbed = disnake.Embed(
            title='Добавление сервера',
            description=f'Имя сервера: `{guild.name} (ID: {guild.id})`\nВладелец: `{guild.owner} (ID: {guild.owner.id})`\nКоличество участников: `{len(guild.members)}`\
                \nКоличество ролей: `{len(guild.roles)}`',
            timestamp=datetime.now(),
            color=Color.gray
        )
        logEmbed.set_footer(text=f'{guild.id}')
        log_channel = self.bot.get_channel(log_channel_id)
        await log_channel.send(embed=logEmbed)
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            logs_channel_id = await self.db.get_channel_id(1, member.guild)
            logs_channel = self.bot.get_channel(logs_channel_id[0])
            info_channel = self.bot.get_channel(1206269623893233765)
            admin_role = member.guild.get_role(1215250562497388604)
            user = await self.db.get_user(member)
            
            if member.guild.id == 1042503919290548264:
                role = disnake.utils.get(member.guild.roles, id=1206972883096567859)
                await member.add_roles(role)

            else:
                if logs_channel == None:
                    pass

                else:
                    logger.info(f'Пользователь {member} [{member.id}] присоеденился на сервер {member.guild.name} [{member.guild.id}]')
                    

                    logEmbed = disnake.Embed(
                        title='Логгирование входов',
                        color=Color.red,
                        timestamp=datetime.now(),
                        description=f'**Пользователь:** {member.name}\n**ID:** {member.id}'
                    )
                    await logs_channel.send(embed=logEmbed)
            
            if user is not None and user[3] != 'Не установлен':
                await member.edit(nick=user[3])

                if admin_role not in member.roles:
                    await member.add_roles(1215250562497388604)

            infoEmbed = disnake.Embed(
                title='Новый пользователь',
                description=f'Добро пожаловать на сервер, {member.mention} :wave:',
                color=Color.main_color,
                timestamp=datetime.now()
            )
            infoEmbed.set_footer(text=member.id)
            await info_channel.send(embed=infoEmbed)

            
        except Exception as ex:
            logger.error(f'[ON_MEMBER_JOIN] {ex}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            logs_channel_id = await self.db.get_channel_id(2, member.guild)
            logs_channel = self.bot.get_channel(logs_channel_id[0])
            if logs_channel == None:
                pass

            else:
                logger.info(f'Пользователь {member} [{member.id}] вышел из сервера {member.guild.name} [{member.guild.id}]')
                logEmbed = disnake.Embed(
                    title='Логгирование выходов',
                    color=Color.red,
                    timestamp=datetime.now(),
                    description=f'**Пользователь:** {member.name}\n**ID:** {member.id}'
                )
                await logs_channel.send(embed=logEmbed)
            
        except Exception as ex:
            logger.error(f'[ON_MEMBER_REMOVE] {ex}')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            logs_channel_id = await self.db.get_channel_id(8, before.guild)
            logs_channel = self.bot.get_channel(logs_channel_id[0])
            
            if logs_channel == None:
                pass

            else:
                if len(before.roles) > len(after.roles):
                    role = next(role for role in before.roles if role not in after.roles)
                    logEmbed = disnake.Embed(
                        title='Логгирование ролей',
                        color=Color.red,
                        timestamp=datetime.now(),
                        description=f"Пользователю {before.mention} снята роль {role.mention}"
                    )
                    logEmbed.set_footer(text='Roles logs')
                    await logs_channel.send(embed=logEmbed)

                elif len(after.roles) > len(before.roles):
                    role = next(role for role in after.roles if role not in before.roles)
                    logEmbed = disnake.Embed(
                        title='Логгирование ролей',
                        color=Color.red,
                        timestamp=datetime.now(),
                        description=f"Пользователю {before.mention} добавлена роль {role.mention}"
                    )
                    logEmbed.set_footer(text='Roles logs')
                    await logs_channel.send(embed=logEmbed)

        except Exception as ex:
            logger.error(f'[ON_MEMBER_UPDATE] {ex}')


    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.author.bot or message_after.author.bot:
            pass

        else:
            try:
                get_channel_id = await self.db.get_channel_id(3, message_before.author.guild)
                logs_channel = self.bot.get_channel(get_channel_id[0])
                if logs_channel == None:
                    pass

                else:
                    logEmbed = disnake.Embed(
                        title='Изменение сообщения',
                        color=Color.red,
                        timestamp=datetime.now(),
                        description=f'**Пользователь:** {message_before.author.name}\n**UserID:** `{message_before.author.id}`\n\
                            **Сообщение до:** `{message_before.content}`\n**Сообщение после:** `{message_after.content}`'
                    )
                    logEmbed.set_footer(text='Chat logs')
                    await logs_channel.send(embed=logEmbed)
            
            except Exception as ex:
                logger.error(f'[ON_MESSAGE_EDIT] {ex}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or message.author.bot:
            pass

        else:
            try:
                get_channel_id = await self.db.get_channel_id(4, message.author.guild)
                logs_channel = self.bot.get_channel(get_channel_id[0])
                if logs_channel == None:
                    pass
                
                else:
                    logEmbed = disnake.Embed(
                        title='Удаление сообщения',
                        color=Color.red,
                        timestamp=datetime.now(),
                        description=f'**Пользователь:** {message.author.name}\n**UserID:** `{message.author.id}`\n\
                            **Сообщение:** `{message.content}`'
                    )
                    logEmbed.set_footer(text='Chat logs')
                    await logs_channel.send(embed=logEmbed)
            
            except Exception as ex:
                logger.error(f'[ON_MESSAGE_DELETE] {ex}')
    
def setup(bot):
    bot.add_cog(Events(bot))