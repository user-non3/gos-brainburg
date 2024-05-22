import disnake
import time
import asyncio
import random
import json
import aiosqlite
import time 
import os
import requests
import requests
import arz_api
from disnake.ext import commands, tasks
from disnake.interactions import MessageInteraction
from disnake import TextInputStyle
from config import *
from datetime import datetime, timedelta
from vprikol_api import VprikolAPI
from colorama import Fore
from gerstlix_python import *
from utils.database import UsersDataBase
from loguru import logger
from functions.getUser import getUser
from .objects import *
from functions.embedCreator import errorCreator
from . import bypass

gx = gerstlixAPI(token=Settings.token_gerstlix)
access_list = [981132768509567057, 459997717595422745, 1163132956261494864]
logger.add("logs/debug.log", format='{time} {level} {message}', level='DEBUG', rotation='2 days', compression='zip')


vprikol = VprikolAPI(Settings.token_vprikol)

header = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

header_vprikol = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MzdmNjcxYWFhMDk2YmRjNmNhMWM3ZCIsIm1ldGhvZHMiOlsibWVtYmVycyIsInJhdGluZyIsImZpbmQiLCJzdGF0dXMiLCJnaGV0dG8iLCJjaGVja3JwIiwicnBuaWNrIiwiZm9ydW0iLCJwbGF5ZXJzIiwib25saW5lIl0sImFudGlmbG9vZF9ieXBhc3MiOmZhbHNlLCJhZG1pbl9hY2Nlc3MiOmZhbHNlLCJleHAiOjI0NzE4MDg1OTl9.2Hd90-AAGBWbXnrpAIf3UPieqY-kdCsSoHT5r2yqyoY'
}

EmbedsList = {
    'waitInfo': disnake.Embed(title='Ожидайте, собираю информацию... :hourglass:', color=disnake.Color.red()),
    'errorAccess': disnake.Embed(title='Временно доступ к этой команде не возможен! :x:', color=disnake.Colour.red()),
    'errorLevel': disnake.Embed(title='У вас нету прав для использования этой команды! :x:', color=disnake.Color.red()),
    'waitDo': disnake.Embed(title='Ожидайте, выполняю запрос... :hourglass:', color=disnake.Color.red()),
    'noResult': disnake.Embed(title='По вашему запросу ничего не найдено! :x:', color=disnake.Color.red()),
    'noPremium': disnake.Embed(title='У сервера нету Premium статуса! :x:' , color=disnake.Color.red())
}

cookies = {
    "xf_user": "1863852%2Cj_NG0TiJW-VouZOE563-GjQD3f5id0sEtGqpliSn",
    "xf_tfa_trust": "eSngcTfyBus7dzMiDZJ9VSHhUj1NquSQ",
    "xf_session": "1SKH21VViZsDYWwkHgSowHv1MJsPOV1p"
}