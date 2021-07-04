import discord
import random
from datetime import datetime, timedelta, date
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import nacl
import sqlite3

#Permissions
intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True

#Init
bot = commands.Bot(command_prefix='.', intents=intents)

#Database related stuff
conn = sqlite3.connect('members.db') #CHANGE THE SELECT RETURN RESULT TO OBJECT THAT CAN BE ACCESSED LIKE A DICT (WITH LOOP)
c = conn.cursor()

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
    print(ctx.guild)
    
@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        await after.channel.connect()
        voice = discord.utils.get(bot.voice_clients)
        
        time.sleep(1)

        if str(member) == 'ShadySX#1828':
            voice.play(discord.FFmpegPCMAudio("vocals/shady.mp3"))
        elif str(member) == 'Irwinn#6787':
            voice.play(discord.FFmpegPCMAudio("vocals/irwin.mp3"))
        elif str(member) == 'MaBa#5713':
            voice.play(discord.FFmpegPCMAudio("vocals/norrix.mp3"))
        elif str(member) == 'Fontaine#2755':
            voice.play(discord.FFmpegPCMAudio("vocals/fontaine.mp3"))
        elif str(member) == '𝚎𝚊𝚉𝚈#6044':
            voice.play(discord.FFmpegPCMAudio("vocals/eazy.mp3"))
        elif str(member) == 'MaBa#5713':
            voice.play(discord.FFmpegPCMAudio("vocals/irwin.mp3"))

        else: 
            rand = random.randint(1,5)
            if rand == 1:
                voice.play(discord.FFmpegPCMAudio("vocals/song1.mp3"))
            if rand == 2:
                voice.play(discord.FFmpegPCMAudio("vocals/song2.mp3"))
            if rand == 3:
                voice.play(discord.FFmpegPCMAudio("vocals/song3.mp3"))
            if rand == 4:
                voice.play(discord.FFmpegPCMAudio("vocals/song4.mp3"))
            if rand == 5:
                voice.play(discord.FFmpegPCMAudio("vocals/song5.mp3"))


        #CODE QUI PERMET DE SEND UN MESSAGE SANS CTX 
        #channel = bot.get_channel(469873589630533653)
        #if str(member) == 'ShadySX#1828':
        #    await channel.send('Shady a rejoint un channel')
        #    print('ITS HIM DUDE') 

        time.sleep(5)
        await voice.disconnect()

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


@bot.command()
async def Join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def Leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def get_members(ctx):
    await ctx.message.delete()

    for user in list(ctx.guild.members):
        print(user)

@bot.event
async def on_message(message):
    print(f"{message.author} gagne un point de score")
    id_ = (message.author.id)
    c.execute("UPDATE members set score = score + 1 WHERE id=?", (id_,)) 

    conn.commit()

    #CETTE LIGNE PERMET DE NE PAS DEMONTER MON PROGRAMME CAR QUAND ON UTILISE SOIS MEME ON MESSAGE CEST LE BORDEL (VOIR STACK OVERFLOW)
    await bot.process_commands(message) 

@bot.command()
async def Ranks(ctx):
    c.execute("SELECT * FROM members order by score desc LIMIT 5")
    res = c.fetchall()
    await ctx.send("Classement des membres (Messages Envoyés)")
    for member in range(len(res)):
        temp = f"{member+1}: {res[member][1]} {res[member][2]} messages" 
        await ctx.send(temp)

@bot.command()
async def MembersInit(ctx):
    
    membersList = (ctx.guild.members)
    for member in membersList:
        print(member.id, member.name)
        c.execute("INSERT INTO members VALUES(?, ?, 0)", (member.id, member.name))

    conn.commit()


bot.run('ODU5ODgyOTQ0MzgxMDU5MTQy.YNzKZQ.7ENYsnCeqyHPWqsjqSETbLy6xSc')

