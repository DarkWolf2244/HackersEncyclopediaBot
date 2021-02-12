import json
import discord
from discord.ext import commands
from datetime import datetime
import random


def getConfig():
    with open('config.json') as f:
        return json.load(f)

def bot_staff(ctx):
    return ctx.author.id in ctx.bot.config["owners"]

class Embed(discord.Embed):
    def __init__(self, ctx: commands.Context, **kwargs):
        self.ctx = ctx
        self.timestamp = datetime.now()
        super().__init__(color=discord.Color.green(), **kwargs)

    def author(self):
        return super().set_author(name=self.ctx.author, icon_url=self.ctx.author.avatar_url)
