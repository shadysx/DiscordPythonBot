import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


bot = commands.Bot(command_prefix='.')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def Meteo(ctx, search: str):

    def FindMeteo(): 
        apiKey = 'a440a00c0ff4abe85ed3319d7e208d73'
        city = search 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}"


        r = requests.get(url).json()
        kTemp = r["main"]["temp"]
        result = KelvinToCelcius(kTemp)
        result = int(result)
        meteo = f"La température à {city} est de {result} C°"
        return meteo
        
    def KelvinToCelcius(kTemp):
        cTemp = kTemp - 273.15
        return cTemp

    meteo = FindMeteo()
    await ctx.send(meteo)




@bot.command()
async def MeteoHour(ctx, search: str):
    city = search 
    apiKey = 'a440a00c0ff4abe85ed3319d7e208d73'
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}"
    dateChoice = '2021-07-03'    
    r = requests.get(url).json()

    list_ = r["list"] #List contient un tableau avec chaque tranche 3H
    
    dataList = [] #DataList continet un tableau avec chaque tranche 3h de la date choisie

    for x in range(len(list_)):
        if list_[x]["dt_txt"][0:10] == dateChoice and list_[x]["dt_txt"][11:16] != '00:00' and list_[x]["dt_txt"][11:16] != '03:00':
            dataList.append({"heure" : list_[x]["dt_txt"][11:16], "value" : round(KelvinToCelcius( list_[x]["main"]["temp"]),2)}) 

    await ctx.send(f'Meteo pour le {dateChoice} à {city}, \n')
    for y in range(len(dataList)):
        await ctx.send(f'{dataList[y]["heure"]} Temperature = {dataList[y]["value"]} C°')



def KelvinToCelcius(kTemp):
        cTemp = kTemp - 273.15
        return cTemp


bot.run('ODU5ODgyOTQ0MzgxMDU5MTQy.YNzKZQ.2osL7UGcaYoT6nKln4tdS1mJhYk')
#print(json.dumps(list_, indent=4, sort_keys=True))
