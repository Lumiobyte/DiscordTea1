import discord
from discord.ext import commands

import sys
sys.path.insert(0, 'D:/Python Coding/Discord Bots/Discord Tea/')
from utils import blacklist_check, sommelier_data

class OwnerCog:

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, module):
        try:
            self.client.unload_extension(module)
            self.client.load_extension(module)
        except Exception as e:
            await ctx.send(":negative_squared_cross_mark: **ERROR:** Could not load cog `{}`: `{}`".format(module, str(e)))
        else:
            await ctx.send(":white_check_mark: Successfully reloaded module `{}`.".format(module))

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, mode, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Blacklisted")

        if mode == 'add':
            blacklist_check.blacklist_add(user)
            await ctx.send(":white_check_mark: **| Blacklisted {}.**".format(user.name))
            await user.add_roles(role)
        elif mode == 'remove':
            blacklist_check.blacklist_remove(user)
            await ctx.send(":white_check_mark: **| Removed {} from the blacklist.**".format(user.name))
            await user.remove_roles(role)

    @commands.command()
    @commands.is_owner()
    async def sommeliers(self, ctx, mode, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Tea Sommelier")

        if mode == 'add':
            sommelier_data.sommelier_add(user)
            await ctx.send(":white_check_mark: **| Registered {} as a Tea Sommelier.**".format(user.name))
            await user.add_roles(role)
        elif mode == 'remove':
            sommelier_data.sommelier_remove(user)
            await ctx.send(":white_check_mark: **| Unregistered {} as a Tea Sommelier.**".format(user.name))
            await user.remove_roles(role)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send(":white_check_mark: **| Shutting down.**")
        await self.client.logout()

def setup(client):
    client.add_cog(OwnerCog(client))