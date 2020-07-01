#!/usr/bin/python3

import discord
from discord.ext import commands
from Player import Players
from Session import Session

g_secret = 'NzI3NDYwMDU0MDA1MTg2NjM0.XvxkVQ.bHsCXP1GyINMGd9tYBAnk53__2Q'
bot = commands.Bot(command_prefix=';')

bot.creators = []
bot.sessions = []

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # await message.channel.send("ouais !")
    await bot.process_commands(message)

@bot.command()
async def start(ctx):
    for session in bot.sessions:
        if ctx.message.author == session.getOwner():
                await session.start(ctx.message.author, bot.user, ctx)
                return
    ctx.send(f"You have not created any session [{ctx.message.author.mention}]")

@bot.command()
async def create_game(ctx, *categorys):
    if ctx.message.author in bot.creators:
        await ctx.send(f'You are already creating a session {ctx.message.author.mention}')
        return 
    if len(categorys) > 6 or len(categorys) < 1:
        await ctx.send('You can only create a baccalaureat between 1 and 6 category')
        return
    bot.creators.append(ctx.message.author)
    bot.sessions.append(Session(ctx.message, categorys))
    create_game_msg = await ctx.send('{} is creating a **Baccalaureat** game with category [**{}**] click the ⚡ to join in !'.format(ctx.message.author.mention,', '.join(categorys)))
    await create_game_msg.add_reaction("⚡")

@bot.command()
async def cancel(ctx):
    for creator in bot.creators:
        for session in bot.sessions:
            if creator == ctx.message.author and creator == session.getOwner():
                await session.stop(bot.user)
                await ctx.send('Deleting **Baccalaureat** session of {}\nPlayers were {}'.format(ctx.message.author.mention,', '.join(session.getPlayers().mentions())))
                bot.sessions.remove(session)
                bot.creators.remove(creator)

bot.run(g_secret)
