from utils import *

class UsersDataBase:
    def __init__(self):
        self.name = './database.db'

    async def create_users_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY,
                Name TEXT,
                UserID INTEGER,
                NickName TEXT,
                FractionID INTEGER, 
                Job INTEGER,
                AccessLvl INTEGER,
                ServerID INTEGER
            )'''
            await cursor.execute(query)
            await db.commit()

    async def create_guilds_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS servers (
                ID INTEGER PRIMARY KEY,
                Name TEXT,
                MembersJoinChannel INTEGER,
                MembersLeaveChannel INTEGER,
                MessagesEditChannel INTEGER,
                MessagesDeleteChannel INTEGER,
                MembersBanChannel INTEGER,
                MembersUnbanChannel INTEGER,
                MembersKickChannel INTEGER,
                MembersRolesChannel INTEGER,
                Banned BOOLEAN,
                Premium INTEGER,
                PremiumDate INTEGER
            )'''
            await cursor.execute(query)
            await db.commit()
    
    async def create_members_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS members (
                ID INTEGER PRIMARY KEY,
                LeaderNick TEXT,
                MemberNick TEXT,
                Fraction TEXT,
                Rank INTEGER,
                Date TEXT,
                DateTime TEXT,
                Reason TEXT,
                FractionID INTEGER
            )'''
            await cursor.execute(query)
            await db.commit()
    
    async def create_logs_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS logs (
                ID INTEGER PRIMARY KEY,
                UserID INTEGER,
                UserName TEXT,
                Type INTEGER,
                Message TEXT,
                Date TEXT,
                Cmd TEXT
            )'''
            await cursor.execute(query)
            await db.commit()
            
    async def create_forum_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS forum (
                ServerID INTEGER,
                NickName TEXT PRIMARY KEY
            )'''
            await cursor.execute(query)
            await db.commit()


    async def get_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM users WHERE UserID = ?'
            await cursor.execute(query, (user.id,))
            return await cursor.fetchone()
        
    async def get_user_dev(self, user):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM users WHERE UserID = ?'
            await cursor.execute(query, (user,))
            return await cursor.fetchone()
        
    async def get_user_by_name(self, name):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM users WHERE Name = ?'
            await cursor.execute(query, (name,))
            return await cursor.fetchone()
        
    async def get_guild(self, server: disnake.Guild):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM servers WHERE ID = ?'
            await cursor.execute(query, (server.id,))
            return await cursor.fetchone()
        
    async def get_logs(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM logs WHERE UserID = ?'
            await cursor.execute(query, (user,))
            return await cursor.fetchall()
        
    async def add_log(self, user: disnake.Member, log_type, message, date, cmd):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'INSERT INTO logs (UserID, UserName, Type, Message, Date, Cmd) VALUES (?, ?, ?, ?, ?, ?)'
            await cursor.execute(query, (user.id, user.name, log_type, message, date, cmd))
            await db.commit()

    async def add_forum(self, server, nickname):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'INSERT INTO forum (ServerID, NickName) VALUES (?, ?)'
            await cursor.execute(query, (server, nickname))
            await db.commit()

    async def add_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_user(user):
                cursor = await db.cursor()
                query = 'INSERT INTO users (Name, UserID, NickName, FractionID, Job, AccessLvl, ServerID) VALUES (?, ?, ?, ?, ?, ?, ?)'
                await cursor.execute(query, (user.name, user.id, 'Не установлен', 0, 0, 0, user.guild.id))
                await db.commit()

    async def add_guild(self, guild: disnake.Guild):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_guild(guild):
                cursor = await db.cursor()
                query = 'INSERT INTO servers (ID, Name, MembersJoinChannel, MembersLeaveChannel, MessagesEditChannel,\
                    MessagesDeleteChannel, MembersBanChannel, MembersUnbanChannel, MembersKickChannel, MembersRolesChannel, Banned, Premium, PremiumDate) VALUES (?, ?, ?, ?,\
                    ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                await cursor.execute(query, (guild.id, guild.name, 0, 0, 0, 0, 0, 0, 0, 0, False, 0, 0))
                await db.commit()

    async def get_channel_id(self, type: int, server: disnake.Guild):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            if type == 1:
                query = 'SELECT MembersJoinChannel FROM servers WHERE ID = ?'

            elif type == 2:
                query = 'SELECT MembersLeaveChannel FROM servers WHERE ID = ?'

            elif type == 3:
                query = 'SELECT MessagesEditChannel FROM servers WHERE ID = ?'
            
            elif type == 4:
                query = 'SELECT MessagesDeleteChannel FROM servers WHERE ID = ?'

            elif type == 5:
                query = 'SELECT MembersBanChannel FROM servers WHERE ID = ?'

            elif type == 6:
                query = 'SELECT MembersUnbanChannel FROM servers WHERE ID = ?'

            elif type == 7:
                query = 'SELECT MembersKickChannel FROM servers WHERE ID = ?'

            elif type == 8:
                query = 'SELECT MembersRolesChannel FROM servers WHERE ID = ?'

            await cursor.execute(query, (server.id,))
            return await cursor.fetchone()

    async def set_logs_channel(self, type, channel, server_id):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            if type == 1:
                query = 'UPDATE servers SET MembersJoinChannel = ? WHERE ID = ?'

            elif type == 2:
                query = 'UPDATE servers SET MembersLeaveChannel = ? WHERE ID = ?'

            elif type == 3:
                query = 'UPDATE servers SET MessagesEditChannel = ? WHERE ID = ?'
            
            elif type == 4:
                query = 'UPDATE servers SET MessagesDeleteChannel = ? WHERE ID = ?'

            elif type == 5:
                query = 'UPDATE servers SET MembersBanChannel = ? WHERE ID = ?'

            elif type == 6:
                query = 'UPDATE servers SET MembersUnbanChannel = ? WHERE ID = ?'

            elif type == 7:
                query = 'UPDATE servers SET MembersKickChannel = ? WHERE ID = ?'

            elif type == 8:
                query = 'UPDATE servers SET MembersRolesChannel = ? WHERE ID = ?'

            
            elif type == 10: 
                query = 'UPDATE servers SET MembersJoinChannel = 0, MembersLeaveChannel = 0, MessagesEditChannel = 0, \
                    MessagesDeleteChannel = 0, MembersBanChannel = 0, MembersUnbanChannel = 0, \
                    MembersKickChannel = 0, MembersRolesChannel = ? WHERE ID = ?'
            await cursor.execute(query, (channel, server_id))
            await db.commit()

    async def set_user_stats(self, type, data, user):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            if type == 1:
                query = 'UPDATE users SET NickName = ? WHERE UserID = ?'

            elif type == 2:
                query = 'UPDATE users SET FractionID = ? WHERE UserID = ?'

            elif type == 3:
                query = 'UPDATE users SET Job = ? WHERE UserID = ?'
            
            elif type == 4:
                query = 'UPDATE users SET AccessLvl = ? WHERE UserID = ?'

            elif type == 5:
                query = 'UPDATE users SET NickName = ? WHERE ID = ?'

            await cursor.execute(query, (data, user))
            await db.commit()

    async def get_ranks_logs_list(self, fraction):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM members WHERE FractionID = ?'
            await cursor.execute(query, (fraction,))
            return await cursor.fetchall()
        
    async def get_forum_list(self, server):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM forum WHERE ServerID = ?'
            await cursor.execute(query, (server,))
            return await cursor.fetchall()
        
    async def create_ranks_log(self, leader_nick, member_nick, fraction, rank, date, datetime, reason, fractionid):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'INSERT INTO members (LeaderNick, MemberNick, Fraction, Rank, Date, DateTime, Reason, FractionID)\
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            await cursor.execute(query, (leader_nick, member_nick, fraction, rank, date, datetime, reason, fractionid,))
            await db.commit()

    async def delete_ranks_log(self, member_nick, fraction):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'DELETE FROM members WHERE MemberNick = ? AND FractionID = ?'
            await cursor.execute(query, (member_nick, fraction,))
            await db.commit()

    async def get_users_count(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT COUNT(*) FROM users'
            await cursor.execute(query)
            return await cursor.fetchone()
        
    async def delete_user(self, user):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'DELETE FROM users WHERE UserID = ?'
            await cursor.execute(query, (user,))
            await db.commit()

    async def get_team_list(self, fraction):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM users WHERE FractionID = ? ORDER BY Job'
            await cursor.execute(query, (fraction,))
            return await cursor.fetchall()
        
    async def give_premium(self, guild):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'UPDATE servers SET Premium = 1, PremiumDate = 1721349590 WHERE ID = ?'
            await cursor.execute(query, (guild.id,))
            await db.commit()
            return True