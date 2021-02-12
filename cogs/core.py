from discord.ext import commands
from discord import Embed
import discord
import os
import json
from loguru import logger

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

def setup(bot):
    bot.add_cog(Core(bot))
