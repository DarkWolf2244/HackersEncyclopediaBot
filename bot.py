#Module Importation
import json
import discord
from discord.ext import commands
import asyncio
import os
import sys
import datetime
from CalculateLib import *
import logging
from discord.ext import tasks
from collections import defaultdict, deque
#from image_gen import generate_image
import string
from io import BytesIO
import random

adminlist = [525334420467744768]
desc = ("placeholder")

bot = commands.Bot(command_prefix = "Alexa ", description=desc, help_command = None, case_insensitive = True)
bot.remove_command('help')

#@bot.event
#async def on_command_error(ctx,error):
#    await ctx.send('Bot is currently locked, sorry for the inconvenience.')
#    print(error)

@bot.event
async def on_ready():
    print("Up and running")
    await bot.change_presence(status = discord.Status.online)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

#@bot.check
#async def lockdown(ctx):
#    return ctx.author.id in adminlist

@bot.command(description="Provides all the information about a node/program.", brief = '`Alexa info {program/node} {name} [level]`')
async def info(ctx, mode, name, level=None):
    if level is None:
        name = name.lower()
        with open(f'{str(os.getcwd())}\{mode}\{name}.json','r') as f:
            temp = json.load(f)
        name = name.capitalize()
        embed = discord.Embed(color = 0x00ff00)
        a = ''
        if mode.lower() == 'program':
            for i in temp['generalInfo']:
                if i == "imageAddress":
                    continue
                a += f'**{i}**: {temp["generalInfo"][i]}\n\n'
            embed.set_image(url=temp['generalInfo']['imageAddress'])
            embed.add_field(name = f"General stats of {name.capitalize()}:",value = a)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        else:
            name = name.lower()
            with open(f'{str(os.getcwd())}\{mode}\{name}.json','r') as f:
                for i in temp['generalInfo']:
                    a += f'**{i}**: {temp["generalInfo"][i]}\n\n'
                embed.set_image(url=temp[str(len(temp)-1)]['imageAddress'])
                embed.add_field(name = f"General stats of {name.capitalize()}:",value = a)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return

    if level is not None:
        if mode == 'node':   
            name = name.lower()
            with open(f'{str(os.getcwd())}\{mode}\{name}.json','r') as f:
                temp = json.load(f)
            name = name.capitalize()
            embed = discord.Embed(color = 0x00ff00)
            a = ''
            for i in temp[level]:
                if i == 'imageAddress':
                    continue
                a += f'**{i}**: {temp[level][i]}\n'
            embed.set_image(url=temp[level]['imageAddress'])
            embed.add_field(name = f"Stats of {name} at level {level}:",value = a)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        elif mode.lower() == 'program':
            name = name.lower()
            with open(f'{str(os.getcwd())}\{mode}\{name}.json','r') as f:
                temp = json.load(f)
            name = name.capitalize()
            embed = discord.Embed(color = 0x00ff00)
            a = ''
            for i in temp[level]:
                if i == 'imageAddress':
                    continue
                a += f'**{i}**: {temp[level][i]}\n'
            embed.set_image(url=temp['generalInfo']['imageAddress'])
            embed.add_field(name = f"Stats of {name} at level {level}:",value = a)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return  

@bot.command()
async def calculate(ctx):
    author = ctx.author
    answers = []
    questionsList = [
        "What program will be used?",
        "How many of the programs will be used?",
        "What node will be attacked?",
        "Is it guarded by any guardians? (Yes/No)",
        "Please list the level of each guardians."
    ]            
    for i in range(0,len(questionsList)):
        def check(m):
            return m.author == ctx.author and m.guilds == None
        await author.send(questionsList[i])
        answers[i] = await bot.wait_for('message', check = check, timeout = 60)
        if i == 3:
            if answers[i].lower() == 'yes':
                continue
            else:
                break
    
    
@bot.command(description="(This shows the help page that you're currently viewing).", brief="`.help [command]`")
async def help(ctx, *, args=None):
    if args is not None:
        b = args.split()
    try:
        if args is None:
            embed = discord.Embed(color=0x00ff00, title = desc)
            a = list(bot.commands)
            for i in range(0,len(bot.commands)):
                if a[i].hidden == True:
                    pass
                else:
                    embed.add_field(name=a[i].name, value = str(a[i].description),inline=False)
            embed.set_footer(text="For more information on any command type |.help <command>| (work in progress)")
            await ctx.author.send(embed=embed)
            await ctx.send('A message with the help page sent to your DM!')
        elif len(b) == 1:
            reqCommand = bot.get_command(b[0])
            embed = discord.Embed(color=0x00ff00,title = "Help page for " + reqCommand.name + " command:")
            embed.add_field(name="Usage: ", value = str(reqCommand.brief),inline=True)
            if len(reqCommand.aliases) != 0:
                embed.add_field(name="Aliases: ", value = str(reqCommand.aliases), inline = False)
            else:
                embed.add_field(name="Aliases: ", value = "No aliases", inline = False)
            embed.add_field(name="Description on usage:", value = reqCommand.description,inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("Failed sending the message with the help page.")
                         
@bot.command(description = "Return the latency of the bot. Can also be triggered with .ping", aliases=['ping'], brief = "`Alexa ping`")
async def latency(ctx):
    await ctx.send("Pong! "  + str(round(bot.latency * 1000)) + "ms.")
        
@bot.command(brief='`Alexa playDespacito/reboot`', description="This restarts the bot, which is useful if something goes wrong or the bot freezes. Only a select few people are able to use this command.",aliases=['reboot'])
async def playDespacito(ctx):
    if ctx.author.id in adminlist:
        authid= ctx.author
        embed = discord.Embed(color = 0x00ff00)
        embed.add_field(name="Shutdown Command Sent, Bot Rebooting in 3 seconds", value = "Sent By {}".format(authid), inline = False)
        await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await bot.close()
        os.execl(sys.executable, sys.executable, * sys.argv)
    else:
        await ctx.send("Sorry, you aren't allowed to use this command.")
        
        
@bot.command(description="Load a module on to the bot, so we (dev team) don't have to restart the bot each time we change a single line of code in the module")
async def load(ctx, extension, args1=None):
    if ctx.author.id in adminlist:
        if "-s" in args1:
            bot.load_extension(f'cogs.{extension}')
            print(f'{extension} has been loaded')
    
        else:
            await ctx.send(f'{extension} has been loaded')
            bot.load_extension(f'cogs.{extension}')
    
    else:
        await ctx.send("You do not have the proper permissions to perform this action.")
    
@bot.command(description="Unload a module in the bot, in the case of abusing a command in that module")
async def unload(ctx, extension, args1=None):
    if ctx.author.id in adminlist:
        if "-s" in args1:
            bot.unload_extension(f'cogs.{extension}')
            print(f'{extension} has been unloaded')
    
        else:
            await ctx.send(f'{extension} has been unloaded')
            bot.unload_extension(f'cogs.{extension}')
    
    else:
        await ctx.send("You do not have the proper permissions to perform this action.")
    
@bot.command(description="Reload a module in the bot")
async def reload(ctx, extension, args1=None):
    if ctx.author.id in adminlist:
        if "-s" in args1:
            bot.reload_extension(f'cogs.{extension}')
            print(f'{extension} has been reloaded')
    
        else:
            await ctx.send(f'{extension} has been reloaded')
            bot.reload_extension(f'cogs.{extension}')
    
    else:
        await ctx.send("You do not have the proper permissions to perform this action.")

@load.error
async def load_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> Error! Missing required argument! Please specify the module to load")
    
        
@unload.error
async def unload_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> Error! Missing required argument! Please specify the module to unload")
    
        
@reload.error
async def reload_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> Error! Missing required argument! Please specify the module to reload")
            
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(description = "in progress", hidden = True)
async def wip(ctx):
    return
    await ctx.send("Network building started in {}'s DM!".format(ctx.author.name))
    try:
        await ctx.author.send('Network building started!')
    except discord.Forbidden:
        await ctx.send("Hmm, looks like I couldn't DM you. Did you block the bot?")
    connections = nested_dict(2,bool)
    nodeList = {'netCon'}
    i = 0
    queue = deque()
    queue.append('netCon')
    try:
        def check(m):
            return m.author == ctx.author and m.guild is None
        while queue:
            curNode = queue.pop()
            await ctx.author.send('Input all nodes connected to node: {}.'.format(curNode))
            msg = await bot.wait_for('message', timeout = 20.0, check=check)
            if msg.content == 'end':
                for i in connections:
                    connections[i] = dict(connections[i])
                await ctx.author.send(dict(connections))
                break
            msgContent = (msg.content).split()
            for b in range(0,len(msgContent)):
                connections[msgContent[b]][curNode] = True
                connections[curNode][msgContent[b]] = True
                if msgContent[b] not in nodeList: queue.append(msgContent[b])
                nodeList.add(msgContent[b])
        connections = dict(connections)
        for i in connections:
            connections[i] = dict(connections[i])
        print(connections)
        await ctx.author.send(dict(connections))
        im = generate_image(connections)
        with BytesIO() as image_binary:
            im.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.channel.send(file=discord.File(fp=image_binary, filename='image.png'))
    except EOFError:
        await ctx.send("idk")

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)        


def load_cogs(self):
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                self.load_extension(f"cogs.{name}")
                print(f"Loaded cogs.{name}")
            except Exception as e:
                print(f"Couldn't load: {name}.")
                print(e)

token = os.environ.get('BOT_TOKEN')
bot.run('Nzk0NTc1NzYxOTUyNjA0MjMw.X-80WA.C96318WTnLT12y_oKpDHx8Ag6Yo')
#bot.close()

