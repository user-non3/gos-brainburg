from utils import *

def changePreds(user, leader, value, reason):
    params = {
        'userid': user, 
        'leader': leader, 
        'operation': 'pred', 
        'value': f'{value}', 
        'reason': reason
    }

    try:
        requests.post(f'{api_url}/changeLeader?token={api_token}', headers=header, data=params)

    except Exception as ex:
        logger.error(f'[changePred] {ex}')