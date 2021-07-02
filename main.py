import discord
from datetime import datetime, timedelta, date
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

bot = commands.Bot(command_prefix='.')

bot.remove_command('help')


@bot.command()
async def Help(ctx):
    embed = discord.Embed(title="Menu d'aide", url="https://google.com",description="Ceci est le menu d'aide", color=0XFF5733)
    embed.add_field(name=".ping", value='Pour savoir si le bot est On', inline=False)
    embed.add_field(name=".Clear <nombre_messages>", value='Supprime un certain nombre de messages dans le channel', inline=False)
    embed.add_field(name=".MeteoNow <ville>", value="Donne la météo à l'instant présent dans une ville choisie", inline=False)
    embed.add_field(name=".Meteo <ville> <date>", value="Donne la météo pour toute la journée d'une ville choisie et d'une date choisie", inline=False)
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
        meteo = f"La température (ressentie) à {city} est de {result} C°"
        return meteo
        
    meteo = FindMeteo()
    await ctx.send(meteo)




@bot.command()
async def Meteo(ctx, search: str, date: str):
    city = search 
    apiKey = 'a440a00c0ff4abe85ed3319d7e208d73'
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}"
    dateChoice = DateConverter(date)    
    r = requests.get(url).json()

    list_ = r["list"] #List contient un tableau avec chaque tranche 3H
    dataList = []

    temp = datetime.strptime(dateChoice, "%Y-%m-%d")
    temp = temp - datetime.now()
    if temp > timedelta(hours=120):
        print("Error forecast can be 5 days long")
        await ctx.send("La météo n'est disponible que pour les 5 prochains jours")
        return

    prettyDate = datetime.strptime(dateChoice, "%Y-%m-%d")
    prettyDate = prettyDate.strftime("%A %d %B %Y")
    print(prettyDate) 

    await ctx.send(f'Meteo for {city} {prettyDate}')

    for x in range(len(list_)):
        if list_[x]["dt_txt"][0:10] == dateChoice and list_[x]["dt_txt"][11:13] > '03':
            print(list_[x]["dt_txt"][11:13])
            parsed = datetime.strptime(list_[x]["dt_txt"], "%Y-%m-%d %H:%M:%S")
            parsed = parsed - timedelta(hours=1, minutes=0)
            timeExtract = "{:02d}:{:02d}".format(parsed.hour, parsed.minute)
            print(timeExtract)
            resp = f'{timeExtract}, {round(KelvinToCelcius(list_[x]["main"]["temp"]),2)} C°'
            await ctx.send(resp) 

def DateConverter(date):
    temp = date.split("/")
    day = "{:02d}".format(int(temp[0]))
    month = "{:02d}".format(int(temp[1]))
    newDate = f"2021-{month}-{day}"
    return newDate


def KelvinToCelcius(kTemp):
        cTemp = kTemp - 273.15
        return cTemp

bot.run('ODU5ODgyOTQ0MzgxMDU5MTQy.YNzKZQ.eO7CYpw2RHkR7bkmp4l5z-gRrvY')
