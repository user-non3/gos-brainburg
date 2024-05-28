import disnake
from disnake.ext import commands, tasks

class StatPingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def update_bot_latency(self):
        guild_id = 1239614973345271848  # тут ид сервера
        channel_id = 1239619577735024734 # тут ид канала

        guild_get = self.bot.get_guild(guild_id)
        guilds = 0
        if guild_get:
            channel = guild_get.get_channel(channel_id)
            if channel and isinstance(channel, disnake.VoiceChannel): 
                for guild in self.bot.guilds:
                    guilds += 1

                await channel.edit(name=f'🌐 Всего серверов: {guilds}')

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_bot_latency.start()

def setup(bot):
    bot.add_cog(StatPingCog(bot))