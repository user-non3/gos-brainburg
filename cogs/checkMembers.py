from utils import *
from functions.embedCreator import errorCreator

class checkMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл checkMembers.py успешно загружен')
    
    @commands.slash_command(description='Посмотреть онлайн фракции')
    async def members(self, interaction, fraction: int = commands.Param(name='фракция', description='Введите ID фракции')):
        user = await getUser(interaction.author)
        if user[6] > 1 or user[6] == 1:
            await interaction.response.send_message(embed=EmbedsList['waitInfo'])
            try:
                response = await vprikol.get_members(5, fraction)
                message = ''
                for frac_id, players_info in response.items():
                    if players_info.is_leader_online:
                        for player in players_info.players:
                            if player.rank == 10:
                                message += f':crown: **Лидер организации:** `{players_info.leader_nickname} [ID: {player.ingame_id}]`\n' if players_info.leader_nickname != None else f':crown: **Лидер организации:** `Отсутствует `\n'
                    else:
                        message += f':crown: **Лидер организации:** `{players_info.leader_nickname}` [Не в сети]\n' if players_info.leader_nickname != None else f':crown: **Лидер организации:** `Отсутствует`\n'
                    
                    message += f":alien: **Всего в организации:** `{len(players_info.players)}` человек\n"
                    
                    online_players_count = sum(1 for player in players_info.players if player.is_online and player.username)
                    message += f"\n:busts_in_silhouette: **В данный момент в сети:** `{online_players_count}` человек"
                    count = 1
                    for player in players_info.players:
                        if player.is_online and player.username and player.username != 'GerstlixBot':
                            if player.color == -33752043:
                                message+=(f"\n **{count})** `{player.username}({player.ingame_id}) | Не в форме 🚫 | {player.rank_label} [{player.rank}]`")
                                count += 1

                            else:
                                message+=(f"\n **{count})** `{player.username}({player.ingame_id}) | В форме ✅ | {player.rank_label} [{player.rank}]`")
                                count += 1

                    timestamp_onl = players_info.online_updated_at
                    message += f"\n\n⏳ Последнее обновление: <t:{timestamp_onl}:R>"

                membersEmbed = disnake.Embed(
                    title=f'Онлайн фракции {GetFractionNameByID[fraction]} на сервере {GetServerNameByID[5]} {GetServerIconByID[5]}',
                    color=Color.main_color,
                    timestamp=datetime.now(),
                    description=message
                )
                membersEmbed.set_footer(text=interaction.author.id)
                await interaction.edit_original_response(embed=membersEmbed)
                logger.info(f'[checkMembers] {interaction.author.name} [{interaction.author.id}] посмотрел онлайн фракции {GetFractionNameByID[fraction]}')


            except Exception as ex:
                await errorCreator(interaction, ex)
                # await interaction.edit_original_response(embed=disnake.Embed(title='Ошибка при выполнение команды!', description='```{ex}```', color=Color.red))
                logger.error(f'[getMembers] [type:GET] {ex}')

        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'])
            
def setup(bot):
    bot.add_cog(checkMembers(bot))