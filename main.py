#!/usr/bin/python3

import discord
from discord.ext import commands
from text import *
from Session import Session

g_secret = 'NzI3NDYwMDU0MDA1MTg2NjM0.XvxkVQ.bHsCXP1GyINMGd9tYBAnk53__2Q'
bot = commands.Bot(command_prefix='!')
bot.sessions = []

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.type is discord.ChannelType.private:
        for session in bot.sessions:
            if session.isUserInSession(message.author):
                if await session.reciveWord(message.author, message.content):
                    bot.sessions.remove(session)
    await bot.process_commands(message)

@bot.command()
async def start(ctx):
    for session in bot.sessions:
        if ctx.message.author == session.getOwner():
            await session.start(bot.user)
            return
    await ctx.send(g_no_session_created.format(ctx.message.author.mention))

@bot.command()
async def baccalaureat(ctx, num_round, *categories):
    for session in bot.sessions:
        if ctx.message.author == session.getOwner() or session.isUserInSession(ctx.message.author):
            await ctx.send(g_error_in_session.format(ctx.message.author.mention))
            return
    num_categories = len(categories)
    if num_categories not in range(1, 6):
        await ctx.send(g_error_categories)
    for category in categories:
        category = category.upper()
    invitation = await ctx.send(g_invitation.format(ctx.message.author.mention,', '.join(categories), num_round))
    await invitation.add_reaction("⚡")
    bot.sessions.append(Session(invitation, ctx.message.author, int(num_round), categories))

@bot.command()
async def cancel(ctx):
    for session in bot.sessions:
        if ctx.message.author == session.getOwner():
            await session.stop(bot.user)
            await ctx.send(g_session_cancel.format(ctx.message.author.mention))
            bot.sessions.remove(session)
            return
    temp = await ctx.message.channel.send(g_default_error_msg.format(ctx.message.author.mention))
    await temp.delete(delay=2)

bot.run(g_secret)