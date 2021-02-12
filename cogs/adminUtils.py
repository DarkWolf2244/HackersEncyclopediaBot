from discord.ext import commands
import discord
import os
from loguru import logger
from asyncio import sleep
from utils.util import bot_staff

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.check(bot_staff)
    @commands.command(hidden=True)
    async def reload(self, ctx: commands.Context):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    self.bot.reload_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"reloaded cogs.{filename[:-3]}")
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"loaded cogs.{filename[:-3]}")
        logger.info("Cogs reloaded, bot ready")
        await ctx.message.add_reaction("👌")

    @commands.check(bot_staff)
    @commands.command(hidden = True)
    async def load(self, ctx:commands.Context, extension):
        self.bot.load_extension(f"cogs.{extension}")
        logger.info(f"Loaded cogs.{extension}")
        await ctx.message.add_reaction("👌")
    
    @commands.check(bot_staff)
    @commands.command(hidden = True)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f"cogs.{extension}")
        logger.info(f"Unloaded cogs.{extension}")
        await ctx.message.add_reaction("👌")

    @commands.check(bot_staff)
    @commands.command(hidden = True)
    async def restart(self, ctx:commands.Context):
        await ctx.message.add_reaction("👌")
        await sleep(1)
        await bot.close()
        os.execl(sys.executable, sys.executable, * sys.argv)

def setup(bot):
    bot.add_cog(Admin(bot))
