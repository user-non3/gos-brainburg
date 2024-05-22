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
        response = requests.post(f'https://gos-brainburg.online/api/bot/changeLeader?token={Settings.token_api}', headers=header, data=params)
        print(response.text)

    except Exception as ex:
        logger.error(f'[changeVig] {ex}')