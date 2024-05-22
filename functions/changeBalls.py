from utils import *

def changeBalls(user, leader, value, reason):
    params = {
        'userid': user, 
        'leader': leader, 
        'operation': 'balls', 
        'value': f'{value}', 
        'reason': reason
    }

    try:
        response = requests.post(f'https://gos-brainburg.online/api/bot/changeLeader?token={Settings.token_api}', headers=header, data=params)
        data = response.json()
        print(data['success'])

    except Exception as ex:
        logger.error(f'[changeBalls] {ex}')