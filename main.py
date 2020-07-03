import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.sessions = []

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def start(ctx):
    for session in bot.sessions:
        if ctx.message.author == session.getOwner():
            #start session
            return
    await ctx.send("")