from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

user_id1 = os.environ["USER_ID1"]
city1 = os.environ['CITY1']
birthday1 = os.environ['BIRTHDAY1']

user_id2 = os.environ["USER_ID2"]
city2 = os.environ['CITY2']
birthday2 = os.environ['BIRTHDAY2']


today = datetime.now()
start_date = os.environ['START_DATE']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather(city):
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(birthday):
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

birthday_left1 = get_birthday(birthday1)
birthday_left2 = get_birthday(birthday2)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea1, temperature1 = get_weather(city1)
wea2, temperature2 = get_weather(city2)
data = {"city1":{"value":city1},"weather1":{"value":wea1},"temperature1":{"value":temperature1},"city2":{"value":city2},"weather2":{"value":wea2},"temperature2":{"value":temperature2},"love_days":{"value":get_count()},"birthday_left1":{"value":birthday_left1},"birthday_left2":{"value":birthday_left2},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id1, template_id, data)
res = wm.send_template(user_id2, template_id, data)
print(res)


