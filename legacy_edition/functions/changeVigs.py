from utils import *

def changeVigs(user, leader, value, reason):
    params = {
        'userid': user, 
        'leader': leader, 
        'operation': 'vig', 
        'value': f'{value}', 
        'reason': reason
    }

    try:
        requests.post(f'{api_url}/changeLeader?token={api_token}', headers=header, data=params)

    except Exception as ex:
        logger.error(f'[changeVig] {ex}')