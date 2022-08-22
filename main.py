from datetime import date, datetime,time
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today =str(datetime.datetime.now().date())
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']),math.floor(weather['low']),math.floor(weather['high']),weather['humidity'],weather['wind'],math.floor(weather['pm25'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
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


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,low,high,humidity,wind,pm25= get_weather()
data = {"weather":{"value":wea,"color":get_random_color()},"date":{"value":today,"color":get_random_color()},"city":{"value":city,"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"words":{"value":get_words(),"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"humidity": {"value":humidity,"color":get_random_color()},"wind": {"value":wind,"color":get_random_color()},"pm25": {"value":pm25,"color":get_random_color()},"min_temperature":{"value":low, "color":get_random_color()},"max_temperature":{"value":high, "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)


# print("发送了" + str(count) + "条消息")
# # print("发送了" + str(count) + "条消息")
# wm = WeChatMessage(client)
# wea, temperature, highest, lowest = get_weather()
# data = {"weather":{"value":wea,"color":get_random_color()},"date":{"value":today,"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(),"color":get_random_color()},"highest": {"value":highest,"color":get_random_color()},"lowest":{"value":lowest, "color":get_random_color()}}
# count = 0
# for user_id in user_ids:
#   res = wm.send_template(user_id, template_id, data)
#   count+=1

# print("发送了" + str(count) + "条消息")
