from discord.ext import commands
from discord import Embed
import discord
import os
import json
from loguru import logger
import networkx as nx # Required for node connections
import matplotlib.pyplot as plt # Required for image processing and saving
from utils.CalculateLib import *

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.command(name = "Info", description="Provide infomations of a specific node/program.",
                      usage = "node/program <name> [level]")
    async def info(self, ctx:commands.Context, mode, name, level=None):
        if level is None:
            name = name.lower()
            with open(f'{str(os.getcwd())}{os.path.sep}{mode}{os.path.sep}{name}.json','r') as f:
                temp = json.load(f)
            name = name.capitalize()
            embed = Embed(color = 0x00ff00)
            a = ''
            if mode.lower() == 'program':
                for i in temp['generalInfo']:
                    if i == "imageAddress":
                        continue
                    a += f'**{i}**: {temp["generalInfo"][i]}\n'
                embed.set_image(url=temp['generalInfo']['imageAddress'])
                embed.add_field(name = f"General stats of {name.capitalize()}:",value = a)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            else:
                name = name.lower()
                with open(f'{str(os.getcwd())}{os.path.sep}{mode}{os.path.sep}{name}.json','r') as f:
                    for i in temp['generalInfo']:
                        a += f'**{i}**: {temp["generalInfo"][i]}\n\n'
                    embed.set_image(url=temp[str(len(temp)-1)]['imageAddress'])
                    embed.add_field(name = f"General stats of {name.capitalize()}:",value = a)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed)

        if level is not None:
            if mode == 'node':   
                name = name.lower()
                with open(f'{str(os.getcwd())}{os.path.sep}{mode}{os.path.sep}{name}.json','r') as f:
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
                return await ctx.send(embed=embed)
            elif mode.lower() == 'program':
                name = name.lower()
                with open(f'{str(os.getcwd())}{os.path.sep}{mode}{os.path.sep}{name}.json','r') as f:
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
                return await ctx.send(embed=embed)

    @commands.command(name="netBuild", description="Creates a visual representation of user's network.", usage = "")
    async def netBuild(self, ctx:commands.Context):
        g = nx.Graph() # Initialise a graph
        nodeList = {} # Initialise the node list - it contains info on node connections
        while True: # Until the user says "stop"
            await ctx.send('Input')
            nodeString = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.channel == ctx.channel) # Ask user for input (Ex: "netConnection-Core")
            # Break out of the loop if the user is finished with connecting
            if nodeString.content.lower() == "end":
                break
            # Skip current iteration if input string is nothing
            if nodeString.content == "":
                await ctx.send("Well, you can't connect nothing to nothing. Try again.")
                continue
            dashCount = 0 # Number of hyphens in the input string

            for symbol in nodeString.content: # Check to see how many hyphens in input, we can't have more or less than one
                if symbol == "-":
                    dashCount += 1 
            
            # Tell the user why it can't be accepted and continue
            if dashCount < 0:
                await ctx.send("Sorry, you haven't given me any connection. Please try again.")
                continue
            elif dashCount > 1:
                await ctx.send("Sorry, that's too many connections. Please give me one connection at a time.")
                continue
                
            # Extract the node names from the input string
            nodes = nodeString.content.split("-", 1) # Splits up nodeString from index 0 to the hypen, then hyphen to
                                             # end. Max splits is 1, as specified. It returns an array
            await ctx.send(nodes)

            node1 = nodes[0]
            node2 = nodes[1]
                # Check which node is already in the node list, append the other one to it.
                # If none exist, create a new entry.
            # At this point I got confused and gave up. It creates a back-connection, that's all.
            if node1 in nodeList.keys() and node2 not in nodeList.keys():
                nodeList[node1].append(node2)
                nodeList[node2] = [node1]
            elif node2 in nodeList.keys():
                nodeList[node2].append(node1)
                nodeList[node1] = [node2]
            elif node1 in nodeList.keys() and node2 in nodeList.keys():
                nodeList[node1].append(node2)
                nodeList[node2].append(node1)
            else:
                nodeList[node1] = [node2]
                nodeList[node2] = [node1]

        # Create nodes based on node list
        for node in nodeList.keys():
            g.add_node(node)

        # Connect nodes in graph
        for node in nodeList.keys():
            for connectedNode in nodeList[node]:
                g.add_edge(node, connectedNode)

        nx.draw(g, with_labels = True)
        plt.savefig("image.png")
        file = open(f"{os.getcwd()}{os.path.sep}image.png",'rb')
        await ctx.send(file=discord.File(fp=file))
        file.close()
        os.remove(f"{os.getcwd()}{os.path.sep}image.png")


    @commands.command()
    async def calculate(self, ctx:commands.Context):
        await ctx.send('What node are you using to store the programs?')
        takenNode = {'defProg':{}}
        program = {}
        node = {}
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        a = await self.bot.wait_for('message', check = check)
        a = a.content.lower().split()
        with open(f"{os.getcwd()}{os.path.sep}node{os.path.sep}{a[0]}.json",'r') as f:
            b = json.loads(f.read())
            takenNode['firewall'] = int(b[str(a[1])]['NodeFirewall'].replace(',',''))
            takenNode['fixedFirewall'] = int(b[str(a[1])]['NodeFirewall'].replace(',',''))
            takenNode['regen'] = int(b['generalInfo']['RegenerationRate'].replace('%',""))
        await ctx.send('What defensive program are you using?')
        a = await self.bot.wait_for('message',check=check)
        a = a.content.lower()
        c= 0
        if a == 'none':
            pass
        else:
            a = a.split()
            c = 0
            for i in a:
                c += 1
                b = i.split('-')
                with open(f"{os.getcwd()}{os.path.sep}program{os.path.sep}{b[0]}.json",'r') as f:
                    d = json.loads(f.read())
                if b[0] == 'protector':
                    takenNode['defProg'][str(c)] = [int(d[str(b[1])]['BufferSize'].replace(',','')), 7, int(d[str(b[1])]['BufferSize'].replace(',',''))]
                else:
                    takenNode['defProg'][str(c)] = [int(d[str(b[1])]['BufferSize'].replace(',','')), 0, int(d[str(b[1])]['BufferSize'].replace(',',''))]
            c = 0
        await ctx.send("What program are you using?")
        a = await self.bot.wait_for('message',check = check)
        a = a.content.lower().split()
        for i in a:
            c += 1
            b = i.split('-')
            print(b)
            with open(f"{os.getcwd()}{os.path.sep}program{os.path.sep}{b[0]}.json",'r') as f:
                d = json.loads(f.read())
            program[str(c)] = {}
            program[str(c)]['damage'] = float(d[str(b[1])]['Strength(DPS)']) * float(d['generalInfo']['ProjectileTime'].replace(" Second",'').replace("s",''))
            program[str(c)]['installTime'] = float(d['generalInfo']['InstallTime'].replace(" Second",'').replace("s",''))
            program[str(c)]['interval'] = float(d['generalInfo']['Delay'].replace(" Second",'').replace("s",''))
            program[str(c)]['projectileTime'] = float(d['generalInfo']['ProjectileTime'].replace(" Second",'').replace("s",''))
            program[str(c)]['localCounter'] = 0
            if b[0] == 'shuriken':
                program[str(c)]['mode'] = 'multi'
            else:
                program[str(c)]['mode'] = None
            if b[0] == 'blaster':
                program[str(c)]['stun'] = 2
            else:
                program[str(c)]['stun'] = 0
        await ctx.send("What node will be tested?")
        a = await self.bot.wait_for('message',check = check)
        a = a.content.lower().split()
        for i in a:
            b = i.split('-')
            with open(f"{os.getcwd()}{os.path.sep}node{os.path.sep}{b[0]}.json",'r') as f:
                d = json.loads(f.read())
            node[b[0]] = {}
            node[b[0]]['guardians'] = {}
            node[b[0]]['sentryCounter'] = 0
            node[b[0]]['nodeCounter'] = 0
            node[b[0]]['stunCounter'] = 0
            node[b[0]]['firewall'] = int(d[str(b[1])]['NodeFirewall'].replace(',',''))
            node[b[0]]['fixedFirewall'] = int(d[str(b[1])]['NodeFirewall'].replace(',',''))
            node[b[0]]['regen'] = int(d['generalInfo']['RegenerationRate'].replace('%',''))
            if "Strength(DPS)" not in d[str(b[1])]:
                node[b[0]]['DPS'] = 0
                node[b[0]]['interval'] = 0
            else:
                node[b[0]]['DPS'] = float(d[str(b[1])]['Strength(DPS)']) * float(d['generalInfo']['ProjectileTime'].replace(' Second','').replace('s',''))
                node[b[0]]['interval'] = float(d['generalInfo']['ProjectileTime'].replace(' Second','').replace('s',''))
        c = 0
        await ctx.send("Do they have AV installed? If so, what level is it?")
        a = await self.bot.wait_for('message',check=check)
        a = a.content.lower()
        if a == 'no' or a == 'none':
            for i in node:
                node[i]['sentryDPS'] = 0
        else:
            with open(f"{os.getcwd()}{os.path.sep}node{os.path.sep}sentry.json",'r') as f:
                d = json.loads(f.read())
            for i in node:
                node[i]['sentryDPS'] = int(d[a]['Strength(DPS)'])
        await ctx.send("Specify which guardian is connected to which node. 'end' to stop.")
        while True:
            a = await self.bot.wait_for('message',check = check)
            a = a.content
            if a.lower() == 'end':
                break
            a = a.lower().split()
            b = a[1].split('-')
            for i in b:
                c += 1
                with open(f"{os.getcwd()}{os.path.sep}node{os.path.sep}guardian.json",'r') as f:
                    d = json.loads(f.read())
                node[a[0]]['guardians'][str(c)] = [int(d[i]['ShieldBuffer'].replace(',','')), 0, int(d[i]['ShieldBuffer'].replace(',',''))]
        print(takenNode)
        print(program)
        print(node)
        await ctx.send(bruteCal(takenNode,program,node))
                                              
def setup(bot):
    bot.add_cog(Core(bot))
