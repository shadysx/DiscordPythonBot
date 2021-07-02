import discord
from datetime import datetime, timedelta
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


bot = commands.Bot(command_prefix='.')

bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Menu d'aide", url="https://google.com",description="Ceci est le menu d'aide", color=0XFF5733)
    embed.add_field(name=".ping", value='Pour savoir si le bot est On', inline=False)
    embed.add_field(name=".Clear <nombre_messages>", value='Supprime un certain nombre de messages dans le channel', inline=False)
    embed.add_field(name=".MeteoNow <ville>", value="Donne la météo à l'instant présent dans une ville choisie", inline=False)
    embed.add_field(name=".MeteoHour <ville>", value="Donne la météo pour toute la journée d'une ville choisie", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name = 'Clear', help="Cette fonction supprime 5 messages mais peut en supprimer jusqu'a 100: .Clear <nombre_de_messages>")
async def Clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)


@bot.command(name = 'MeteoNow', help="Affiche la température a l'instant présent : \n.MeteoNow <ville>")
async def MeteoNow(ctx, search: str):

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
        
    meteo = FindMeteo()
    await ctx.send(meteo)




@bot.command()
async def MeteoHour(ctx, search: str):
    city = search 
    apiKey = 'a440a00c0ff4abe85ed3319d7e208d73'
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}"
    dateChoice = '2021-07-02'    
    r = requests.get(url).json()

    list_ = r["list"] #List contient un tableau avec chaque tranche 3H
    dataList = []

    for x in range(len(list_)):
        if list_[x]["dt_txt"][0:10] == dateChoice:
            parsed = datetime.strptime(list_[x]["dt_txt"], "%Y-%m-%d %H:%M:%S")
            parsed = parsed - timedelta(hours=1, minutes=0)
            timeExtract = "{:02d}:{:02d}".format(parsed.hour, parsed.minute)
            print(timeExtract)
            resp = f'{timeExtract}, {round(KelvinToCelcius(list_[x]["main"]["temp"]),2)} C°'
            await ctx.send(resp) 

def KelvinToCelcius(kTemp):
        cTemp = kTemp - 273.15
        return cTemp


bot.run('ODU5ODgyOTQ0MzgxMDU5MTQy.YNzKZQ.8h2CYVX9Up6G0zC4tuAuqiJKZ9A')
