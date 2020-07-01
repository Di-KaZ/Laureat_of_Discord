#!/usr/bin/python3

import discord
from discord.ext import commands

print(discord.__version__)
bot = commands.Bot(command_prefix=';')

bot.game_started = False
bot.catergorys = []
bot.players = []
bot.create_game_msg = None
bot.creating_game = False

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # await message.channel.send("ouais !")
    await bot.process_commands(message)

@bot.command()
async def start(ctx):
    bot.game_started = True
    temp = await ctx.send("Started game !!")
    await temp.delete(delay=5)
    await bot.create_game_msg.delete()

@bot.command()
async def create_game(ctx, *categorys):
    if len(categorys) > 6 or len(categorys) < 1:
        temp = await ctx.send(f'You can only create a baccalaureat between 1 and 6 category')
        await temp.delete(delay=5)
        return
    if bot.game_started:
        temp = await ctx.send("Game already started please wait the end before creating another !")
        await temp.delete(delay=5)
        return
    if bot.creating_game:
        temp = await ctx.send("A game is already in construction with category [{}]".format(', '.join(categorys)))
        await temp.delete(delay=5)
        return
    bot.catergorys = categorys
    bot.create_game_msg = await ctx.send('creating game with category [{}] click the ⚡ to join in !'.format(', '.join(categorys)))
    await bot.create_game_msg.add_reaction("⚡")
    bot.creating_game = True

bot.run('NzI3NDYwMDU0MDA1MTg2NjM0.XvxkVQ.bHsCXP1GyINMGd9tYBAnk53__2Q')
