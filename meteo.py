import discord
from discord.ext import commands

@bot.command()
async def hello(ctx):
    await ctx.send("Hello World")
