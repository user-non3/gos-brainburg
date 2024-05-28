from utils import *

db = UsersDataBase()

async def getUser(id):
    return await db.get_user(id)