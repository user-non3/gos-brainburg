from utils import *
import zipfile
import psutil
from functions.addLog import add_log

def get_discord_timestamp():
    return f"<t:{int(time.time())}:R>"

def get_ram_usage():
    ram = psutil.virtual_memory()
    used = round(ram.used / (1024 ** 3), 2)
    total = round(ram.total / (1024 ** 3), 2)
    return f"`{used}GB/{total}GB`"

def get_cpu_usage():
    return f"`{psutil.cpu_percent()}%`"

def get_storage_usage():
    total = round(psutil.disk_usage("/").total / (1024 ** 3), 2)
    used = round(psutil.disk_usage("/").used / (1024 ** 3), 2)
    return f"`{used}GB/{total}GB`"


class GetUser(disnake.ui.Modal):
    def __init__(self):
        self.db = UsersDataBase()

        components = [
            disnake.ui.TextInput(label="Введите ID/Username", custom_id="player", required=True)
        ]

        super().__init__(title="Панель разработчика", components=components, custom_id="developer_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        player = interaction.text_values["player"]
        try:
            if float(player):
                user = await self.db.get_user_dev(player)
        
        except:
                user = await self.db.get_user_by_name(player)

        if user is None:
            await interaction.response.send_message(embed=EmbedsList['noResult'], ephemeral=True)

        else:
            infoEmbed = disnake.Embed(
                title='Информация о пользователе',
                description=f'**Информация Discord**\n> Ник: `{user[1]}`\n> ID: `{user[2]}`\n\n\
                    **Информация игры**\n> Никнейм: `{user[3]}`\n> Фракция: `{GetFullFractionNameByID[user[4]]}`\n\
                        > Должность: `{GetJobNameByID[user[5]]}`\n> Уровень доступа: `{user[6]}`',
                color=Color.main_color
            )
            await interaction.response.send_message(embed=infoEmbed, ephemeral=True)

class EditUser(disnake.ui.Modal):
    def __init__(self):
        self.db = UsersDataBase()

        components = [
            disnake.ui.TextInput(label="Введите ID пользователя", custom_id="userid", required=True),
            disnake.ui.TextInput(label="Введите Никнейм", custom_id="nickname", required=False),
            disnake.ui.TextInput(label="Введите ID Фракции", custom_id="fraction", required=False),
            disnake.ui.TextInput(label="Введите ID Должности", custom_id="job", required=False),
            disnake.ui.TextInput(label="Введите Уровень доступа", custom_id="access", required=True)
        ]

        super().__init__(title="Изменение пользователя", components=components, custom_id="developer_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        userid = interaction.text_values["userid"]
        nickname = interaction.text_values["nickname"]
        fraction = interaction.text_values["fraction"]
        job = interaction.text_values["job"]
        access = interaction.text_values["access"]

        if len(nickname) == 0:
            pass
        
        else:
            await self.db.set_user_stats(1, nickname, userid)
        
        if len(fraction) == 0:
            pass
            
        else:
            await self.db.set_user_stats(2, fraction, userid)
            
        if len(job) == 0:
            pass

        else:
            await self.db.set_user_stats(3, job, userid)

        await self.db.set_user_stats(4, access, userid)
        await interaction.response.send_message(f'Вы успешно изменили статистику пользователя :white_check_mark:\nПараметры: `{nickname}` | `{fraction}` | `{job}` | `{access}`', ephemeral=True)

class AddUser(disnake.ui.Modal):
    def __init__(self):
        self.db = UsersDataBase()

        components = [
            disnake.ui.TextInput(label="Введите ID пользователя", custom_id="userid", required=True),
            disnake.ui.TextInput(label="Введите Никнейм", custom_id="nickname", required=True),
            disnake.ui.TextInput(label="Введите ID Фракции", custom_id="fraction", required=True),
            disnake.ui.TextInput(label="Введите ID Должности", custom_id="job", required=True),
            disnake.ui.TextInput(label="Введите Уровень доступа", custom_id="access", required=True)
        ]

        super().__init__(title="Создание пользователя", components=components, custom_id="developer_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        userid = interaction.text_values["userid"]
        nickname = interaction.text_values["nickname"]
        fraction = interaction.text_values["fraction"]
        job = interaction.text_values["job"]
        access = interaction.text_values["access"]

        await self.db.set_user_stats(1, nickname, userid)
        await self.db.set_user_stats(2, fraction, userid)
        await self.db.set_user_stats(3, job, userid)
        await self.db.set_user_stats(4, access, userid)
        await interaction.response.send_message(f'Вы успешно создали пользователя! :white_check_mark:\nПараметры: `{nickname}` | `{fraction}` | `{job}` | `{access}`', ephemeral=True)
        logger.info(f'[ADD_USER] Создан пользователь [{userid}] параметры | {nickname} | {fraction} | {job} | {access}')

class DeleteUser(disnake.ui.Modal):
    def __init__(self):
        self.db = UsersDataBase()

        components = [
            disnake.ui.TextInput(label="Введите ID", custom_id="player", required=True)
        ]

        super().__init__(title="Удаление пользователя", components=components, custom_id="developer_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        player = interaction.text_values["player"]
        await self.db.delete_user(player)
        await interaction.response.send_message(f'Вы успешно удалили пользователя с ID: `{player}`', ephemeral=True)

class SendButton(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label='Отправить лог', style=disnake.ButtonStyle.grey, custom_id='send_log')
    async def send_log(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        file_path = os.path.getsize('./logs/debug.log')
        file_size = file_path / 1024
        file_split = str(file_size)
        await interaction.response.send_message(f'**Размер файла:** `{file_split.split(".")[0]} кб`', file=disnake.File('./logs/debug.log'), ephemeral=True)

    @disnake.ui.button(label='Отправить папку логов', style=disnake.ButtonStyle.grey, custom_id='send_directory_log')
    async def send_directory_log(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        with zipfile.ZipFile('./logs/logs.zip', 'w') as zip_file:
            files = os.listdir('./logs')

            for file in files:
                zip_file.write(os.path.join('./logs'), file)
        
        file_path = os.path.getsize('./logs/logs.zip')
        await interaction.response.send_message(f'**Общий размер:** `{file_path} кб`\n**Общее количество файлов:** `{len(files)}`', file=disnake.File('./logs/logs.zip'), ephemeral=True)

class ManageButtons(disnake.ui.View):
    def __init__(self, bot):
        self.db = UsersDataBase()
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Статистика", style=disnake.ButtonStyle.grey, custom_id="statistic")
    async def statistic(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        guilds = len(self.bot.guilds)
        users = await self.db.get_users_count()
        files = os.listdir('./logs')
        
        infoEmbed = disnake.Embed(
            description=f'CPU Usage: {get_cpu_usage()}\nRAM Usage: {get_ram_usage()}\nStorage: {get_storage_usage()}\n\nКол-во пользователей: `{users[0]}`\nКол-во серверов: `{guilds}`\nКол-во файлов логов: `{len(files)}`\n\nОбновлено: {get_discord_timestamp()}',
            color=Color.main_color
        )
        infoEmbed.set_author(name='Статистика бота', icon_url='https://mr-zv.ru/img/discord/avatar.png')

        await interaction.response.send_message(embed=infoEmbed, ephemeral=True, view=SendButton(self.bot))

    @disnake.ui.button(label='Поиск', style=disnake.ButtonStyle.grey, custom_id='find')
    async def find(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=GetUser())

    @disnake.ui.button(label='Изменение', style=disnake.ButtonStyle.grey, custom_id='edit_user')
    async def edit_user(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=EditUser())

    @disnake.ui.button(label='Добавить', style=disnake.ButtonStyle.green, custom_id='add_user')
    async def add_user(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=AddUser())

    @disnake.ui.button(label='Удалить', style=disnake.ButtonStyle.red, custom_id='delete_user')
    async def delete_user(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.send_modal(modal=DeleteUser())

class DeveloperPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Файл developer.py успешно загружен')

    @commands.slash_command(name='dev', description='Секрет')
    async def __dev(self, interaction):
        if interaction.author.id in access_list:
            devEmbed = disnake.Embed(
                title='Панель разработчика',
                description='Добро пожаловать в панель разработчика!',
                color=Color.main_color,
                timestamp=datetime.now()
            )
            devEmbed.set_footer(text=interaction.author.id)
            await interaction.response.send_message(embed=devEmbed, view=ManageButtons(self.bot), ephemeral=True)
            await add_log(interaction.author, 0, '', '/dev')
        else:
            await interaction.response.send_message(embed=EmbedsList['errorLevel'], ephemeral=True)

def setup(bot):
    bot.add_cog(DeveloperPanel(bot))