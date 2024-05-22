from . import *

api = arz_api.ArizonaAPI(user_agent=bypass.user_agent, cookie=cookies)
threads = api.get_threads(354)

async def forum(type, content):
    await bypass.bypass_async()
    user = api.current_member
    logger.info(f'Успешный запрос под пользователем [{user.username}:{user.id}]')
    
    if type == 1:
        member = api.get_member(content)
        return member
    
    if type == 2:
        thread = api.get_thread(content)
        return thread
    
