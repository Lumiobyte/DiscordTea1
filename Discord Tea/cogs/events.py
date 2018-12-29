import discord
from discord.ext import commands

class EventsCog:

    def __init__(self, client):
        self.client = client

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            pass
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(":x: **| There was an error invoking the command: `{}`**".format(str(e)))
            print("COMMAND INVOKE ERROR: {} threw '{}'".format(ctx.message.content, str(error)))
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(":x: **| You entered a bad argument into the command: `{}`**".format(str(error)))
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(":x: **| This command has a cooldown; please wait **{}s** before using it again.**".format(round(error.retry_after, 2)))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: **| A required command argument is missing.**")
        elif isinstance(error, discord.Forbidden):
            await ctx.send(":x: **| The bot is missing the required permission.**")
        elif isinstance(error, discord.ext.commands.CheckFailure):
            pass
        else:
            await ctx.send(":x: **| An unknown error occurred. `{}`**".format(str(error)))
            print("UNKNOWN ERROR: {} threw '{}'".format(ctx.message.content, str(error)))

    async def on_guild_join(self, guild):
        channel = discord.utils.get(self.client.get_all_channels(), id=524052770513223691)
        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name="Server Join!", value=":arrow_up: Discord Tea joined **{}**! Now on **{}** servers.".format(guild.name, len(self.client.guilds)))
        await channel.send(embed=embed)

    async def on_guild_remove(self, guild):
        channel = discord.utils.get(self.client.get_all_channels(), id=524052770513223691)
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="Server Leave!", value=":arrow_down: Discord Tea left **{}**. Now on **{}** servers.".format(guild.name, len(self.client.guilds)))
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(EventsCog(client))