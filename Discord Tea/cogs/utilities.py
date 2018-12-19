import discord
from discord.ext import commands

import sys
sys.path.insert(0, 'D:/Python Coding/Discord Bots/Discord Tea/')
from utils import blacklist_check, sommelier_data

class UtilsCog:

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(":ping_pong: Pong! `{}ms`".format(round(self.client.latency * 1000, 3)))

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name="Discord Tea Help - Prefix: tea!")

        if sommelier_data.check(ctx.author):
            embed.add_field(name="Commands you can use:", value="""
            **tea!ping** - See bot latency.
            **tea!invite** - Get an invite link for Discord Tea.
            **tea!order <order>** - Order some tea. 
            **tea!oaccept <orderID>** - Accept an order using its ID to brew it.
            **tea!odecline <orderID> <reason>** - Decline an order using its ID.
            **tea!odeliver <orderID>** - Deliver an order: get the invite to the server it was ordered in.
            **tea!list-o** - See all unclaimed orders.
            """)

        elif not blacklist_check.check(ctx.author):
            embed.add_field(name="Commands you can use:", value="""
            **tea!ping** - See bot latency.
            **tea!invite** - Get an invite link for Discord Tea.
            **tea!order** - Order some tea. 
            **tea!myorders** - See your current active orders.
            **tea!oinfo <orderID>** - Get the info of an order with its ID.
            """)

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.author.send("Invite me with this link: https://discordapp.com/api/oauth2/authorize?client_id=507004433226268699&permissions=2146958839&scope=bot")


def setup(client):
    client.add_cog(UtilsCog(client))