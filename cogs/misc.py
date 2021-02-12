from discord.ext import commands
import discord


class Misc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Not working rn", usage = "a")
    async def help(self, ctx, *, args=None):
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
                embed.add_field(name="Usage: ", value = str(reqCommand.usage),inline=True)
                if len(reqCommand.aliases) != 0:
                    embed.add_field(name="Aliases: ", value = str(reqCommand.aliases), inline = False)
                else:
                    embed.add_field(name="Aliases: ", value = "No aliases", inline = False)
                embed.add_field(name="Description on usage:", value = reqCommand.description,inline=False)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("Failed sending the message with the help page.")


def setup(bot):
    bot.add_cog(Misc(bot))
