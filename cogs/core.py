from discord.ext import commands
from discord import Embed
import discord
import os
import json
from loguru import logger
import networkx as nx # Required for node connections
import matplotlib.pyplot as plt # Required for image processing and saving

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.command(name = "Info", description="Provide infomations of a specific node/program.",
                      usage = "node/program <name> [level]")
    async def info(self, ctx:commands.Context, mode, name, level=None):
        if level is None:
            name = name.lower()
            with open(f'{str(os.getcwd())}\{mode}\{name}.json','r') as f:
                temp = json.load(f)
            name = name.capitalize()
            embed = Embed(color = 0x00ff00)
            a = ''
            if mode.lower() == 'program':
                for i in temp['generalInfo']:
                    if i == "imageAddress":
                        continue
                    a += f'**{i}**: {temp["generalInfo"][i]}\n\n'
                embed.set_image(url=temp['generalInfo']['imageAddress'])
                embed.add_field(name = f"General stats of {name.capitalize()}:",value = a)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            else:
                name = name.lower()
                with open(f'{str(os.getcwd())}\{mode}\{name}.json','r') as f:
                    for i in temp['generalInfo']:
                        a += f'**{i}**: {temp["generalInfo"][i]}\n\n'
                    embed.set_image(url=temp[str(len(temp)-1)]['imageAddress'])
                    embed.add_field(name = f"General stats of {name.capitalize()}:",value = a)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed)

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
                return await ctx.send(embed=embed)
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
                return await ctx.send(embed=embed)
            
    @commands.command()
    async def rickroll(self, ctx:commands.Context):
        await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
    @commands.command()
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
        os.remove("image.png")
        plt.savefig("image.png")
        file = open(f"{os.getcwd()}\image.png",'rb')
        await ctx.send(file =discord.File(fp=file))
        file.close()
        os.remove(f"{os.getcwd()}\image.png")

def setup(bot):
    bot.add_cog(Core(bot))
