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
    if message.channel.type is discord.ChannelType.private:
        for session in bot.sessions:
            if message.author in session.getUsers():
                if await session.reciveWord(message.author, message.content):
                    bot.creators.remove(session.getOwner())
                    bot.sessions.remove(session)
    # await message.channel.send("ouais !")
    await bot.process_commands(message)

@bot.command()
async def start(ctx):
    for session in bot.sessions:
        if ctx.message.author == session.getOwner():
                await session.start(ctx.message.author, bot.user, ctx)
                return
    await ctx.send(f"Tu na pas crée de salon {ctx.message.author.mention} !")

@bot.command()
async def create_game(ctx, ground, *categorys):
    new_categorys = []
    if ctx.message.author in bot.creators:
        await ctx.send(f'Tu crée déja un salon {ctx.message.author.mention} !')
        return 
    if len(categorys) > 6 or len(categorys) < 1:
        await ctx.send('Tu peut seulement avoir entre **1 et 6 catégories**')
        return
    bot.creators.append(ctx.message.author)
    create_game_msg = await ctx.send('{} crée un salon de **Baccalaureat** avec les catégories [**{}**] elle dureras **{} round** appuie sur ⚡ pour la rejoindre !'.format(ctx.message.author.mention,', '.join(categorys), ground))
    await create_game_msg.add_reaction("⚡")
    for category in categorys:
        new_categorys.append(category.upper())
    bot.sessions.append(Session(create_game_msg, ctx.message.author, ground, new_categorys))

@bot.command()
async def cancel(ctx):
    for creator in bot.creators:
        for session in bot.sessions:
            if creator == ctx.message.author and creator == session.getOwner():
                await session.stop(bot.user)
                await ctx.send('Supression du salon de {}\nLes joueurs {} sont maintenant liiibre !'.format(ctx.message.author.mention,', '.join(session.getPlayers().mentions())))
                bot.sessions.remove(session)
                bot.creators.remove(creator)
                return
    temp = await ctx.message.channel.send(f"Nani {ctx.message.author.mention} ?? ")
    await temp.delete(delay=2)

bot.run(g_secret)
