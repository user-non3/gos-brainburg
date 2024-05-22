#Code by Sqeezi aka Qenqy
from . import *

from colorama import init, Fore, Back, Style

#--Настройки
nick = 'Kellai_LaMonte' #Вам ник-нейм
page = 35 #Сколько страниц нужно парсить
#Это куки, их можно получить во вкладке Network
cookie = "_gid=GA1.2.1682696427.1714663213; xf_notice_dismiss=-1; xf_tfa_trust=eSngcTfyBus7dzMiDZJ9VSHhUj1NquSQ; _ga_KQRCJL2214=deleted; _ym_uid=1714749169898989024; _ym_d=1714749169; R3ACTLAB-ARZ1=ae0d90fc6e0647564838191444632ebb; xf_user=1863852%2CuW6BKnFnAAC-kyzMdUWG3lr6-VH1UHhGmyFaBGhG; xf_csrf=QLYh9VbBekx4gd8i; xf_session=krJhVw3XFh2xLMTqNNWRyW188tNC8Ga-; _gat_gtag_UA_175660820_1=1; _ga_KQRCJL2214=GS1.1.1715766071.230.1.1715767357.0.0.0; _ga=GA1.1.2125727052.1714663213"
#А это user-agent, его тоже можно получить во вкладке Network
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"

#Это просто ссылки на разделы жалоб
opg = "https://forum.arizona-rp.com/forums/1138/"	#Жб на банды
gos = "https://forum.arizona-rp.com/forums/1135/"	#Жб на госс
bomj = "https://forum.arizona-rp.com/forums/1136/"	#Жб на просто игроки без орги
mafia = "https://forum.arizona-rp.com/forums/1137/"	#Жб на мафия
admins = "https://forum.arizona-rp.com/forums/1219/"#Жб на админов

api = arz_api.ArizonaAPI(user_agent=user_agent, cookie=cookie)
init(autoreset=True)
#-----------

#Что-то типо интерфейса
def start():
	os.system('cls') 
	print(f'{Fore.YELLOW}{Style.BRIGHT}Code by Sqeezi aka Qenqy{Style.RESET_ALL}\n\n{Fore.CYAN}   1) Жалобы на гос.\n   2) Жалобы на бандитов\n   3) Жалобы на не сост. в гос.\n   4) Мафия\n   5) На админов')
	inp_jb = input(': ')

	if inp_jb == '1':
		main(page, gos, nick)
	elif inp_jb == '2':
		main(page, opg, nick)
	elif inp_jb == '3':
		main(page, bomj, nick)
	elif inp_jb == '4':
		main(page, mafia, nick)
	elif inp_jb == '5':
		main(page, admins, nick)

#Сам алгоритм. По моему мнению он не идиален, но не гКод
def main(page, url, nickname):
	os.system('cls') 
	cout = 1
	while cout < page:
		for elem in api.get_threads(f'{url}page-{cout}'):
			if nickname in elem['title']:
				os.system('cls')
				message = f"Найдена жалоба! - {elem['link']}\n{elem['title']}\n"
				print(f'{Fore.YELLOW}{Style.BRIGHT}Найдена жалоба! - {Fore.GREEN}{Style.BRIGHT}'+elem['link'])
				print('\n'+Fore.CYAN+Style.BRIGHT+elem['title'])	
				
				with open(nickname, 'a', encoding='utf-8') as file:
					file.write(message)

				ans = input('\nПродолжить? Y/Ctrl+c :) : ')


		print(f'{Fore.YELLOW}Страница - {str(cout)}')
		cout += 1
start()