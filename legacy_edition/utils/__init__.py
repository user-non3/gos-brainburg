import disnake
import time
import asyncio
import random
import json
import aiosqlite
import time 
import os
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
from functions.addLog import add_log

access_list = [981132768509567057, 459997717595422745, 1163132956261494864, 283606560436125696]
logger.add("logs/debug.log", format='{time} {level} {message}', level='DEBUG', rotation='2 days', compression='zip')

vprikol = VprikolAPI(vprikol_token)

header = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

header_vprikol = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2NTQzZDlmOWI4OGQzYWY4YTM1ZjNiMSIsIm1ldGhvZHMiOlsibWVtYmVycyIsInJhdGluZyIsImZpbmQiLCJzdGF0dXMiLCJjaGVja3JwIiwicnBuaWNrIiwiaXAiLCJwbGF5ZXJzIiwiZXN0YXRlIl0sImFudGlmbG9vZF9ieXBhc3MiOmZhbHNlLCJhZG1pbl9hY2Nlc3MiOmZhbHNlLCJleHAiOjI0NzM2NjEwNzd9.QE7WOi4xQIUJ0brxC4X7KLR1aO0WhoQRaRFHvShUnHU'
}

EmbedsList = {
    'waitInfo': disnake.Embed(title='Ожидайте, собираю информацию... :hourglass:', color=disnake.Color.red()),
    'errorAccess': disnake.Embed(title='Временно доступ к этой команде не возможен! :x:', color=disnake.Colour.red()),
    'errorLevel': disnake.Embed(title='У вас нету прав для использования этой команды! :x:', color=disnake.Color.red()),
    'waitDo': disnake.Embed(title='Ожидайте, выполняю запрос... :hourglass:', color=disnake.Color.red()),
    'noResult': disnake.Embed(title='По вашему запросу ничего не найдено! :x:', color=disnake.Color.red()),
    'errorServer': disnake.Embed(title='Нельзя использовать на этом сервере! :x:', color=disnake.Color.red())
}

cookies = {
    "xf_user": "1863852%2Cj_NG0TiJW-VouZOE563-GjQD3f5id0sEtGqpliSn",
    "xf_tfa_trust": "eSngcTfyBus7dzMiDZJ9VSHhUj1NquSQ",
    "xf_session": "1SKH21VViZsDYWwkHgSowHv1MJsPOV1p"
}