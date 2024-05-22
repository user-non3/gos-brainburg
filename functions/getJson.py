from utils import *

def get_json(type):
    if type == 1:
        with open('utils/json/commands.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            result_arizona = ""

            for i in data['arizona']:
                cmd = i['command']
                desc = i['description']
                result_arizona += f'`{cmd}` - {desc}\n'

            return result_arizona
            
    elif type == 2:
        with open('utils/json/fractions_id.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            result_fractions = ""
            
            for i in data:
                fid = i['fid']
                name = i['name']
                result_fractions += f'{name} - {fid}\n'

            return result_fractions
        
    elif type == 3:
        with open('utils/json/admins.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            result_admins = ""
            
            for i in data:
                nick = i['nick']
                lvl = i['lvl']
                result_admins += f'{nick} - {lvl}\n'

            return result_admins