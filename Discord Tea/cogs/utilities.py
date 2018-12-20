import discord
from discord.ext import commands
import psutil

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
            **tea!rules** - See ordering rules.
            **tea!ping** - See bot latency.
            **tea!invite** - Get an invite link for Discord Tea.
            **tea!feedback <comment>** - Send feedback to the team!
            **tea!order <order>** - Order some tea. 
            **tea!myorders** - See your current active orders.
            **tea!oinfo <orderID>** - Get the info of an order with its ID.
            ---- Sommelier-only Commands ----
            **tea!oaccept <orderID>** - Accept an order using its ID to brew it.
            **tea!odecline <orderID> <reason>** - Decline an order using its ID.
            **tea!odeliver <orderID>** - Deliver an order: get the invite to the server it was ordered in.
            **tea!ofinish <orderID>** - Finish an order, remove it from the active order list.
            **tea!list-o** - See all unclaimed orders.
            """)

        elif not blacklist_check.check(ctx.author):
            embed.add_field(name="Commands you can use:", value="""
            **tea!rules** - See ordering rules.
            **tea!ping** - See bot latency.
            **tea!invite** - Get an invite link for Discord Tea.
            **tea!feedback <comment>** - Send feedback to the team!
            **tea!order** - Order some tea. 
            **tea!myorders** - See your current active orders.
            **tea!oinfo <orderID>** - Get the info of an order with its ID.
            """)

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.author.send("Invite me with this link: https://discordapp.com/api/oauth2/authorize?client_id=507004433226268699&permissions=2146958839&scope=bot")

    @commands.command()
    async def feedback(self, ctx, *, comment):
        feedback_log = discord.utils.get(self.client.get_all_channels(), id=524769713214062612)

        await ctx.send(":white_check_mark: **| Your feedback has been sent. Thanks, {}!**".format(ctx.author.name))
        await feedback_log.send(":star: **| Received feedback from `{}`: `{}`**".format(ctx.author, comment))

    @commands.command()
    async def rules(self, ctx):
        await ctx.send("""
        **The Rules for Discord Tea are the following:

        • No COFFEE
        • No spammy orders (For example: "tea grsogharihgasuhgosdhgosdg")
        • No NSFW Teas
        • No Offensive Teas (Hitler/Nazi, Sexism, and/or any other forms of Racism - Communism excluded)
        • No Drugs, Medications or Poisons
        • No Human or Animal Body Parts
        • Orders cannot contain text formatting or non-Latin characters, except numbers and !#$%&<>?".
        • Orders cannot contain links.
        • Must Include Tea

        Please respect these rules. Breaking any of them repeatedly will result in being blacklisted from the bot and/or banned from this server.**
        """)

    @comamnds.command()
    async def stats(self, ctx):
        embed = dicord.Embed(color=discord.Color.blue())
        

def setup(client):
    client.add_cog(UtilsCog(client))