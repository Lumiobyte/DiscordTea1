import discord
from discord.ext import commands
import psutil

import sys
sys.path.insert(0, 'D:/Python Coding/Discord Bots/Discord Tea/')
from utils import blacklist_check, sommelier_data, rating_data

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
            **tea!rate <rating>** - Rate this service! Give a rating between 1 and 5.
            **tea!approval** - View the average rating for the service.
            **tea!order <order>** - Order some tea. 
            **tea!myorders** - See your current active orders.
            **tea!oinfo <orderID>** - Get the info of an order with its ID.
            """)
            embed.add_field(name="Sommelier Commands", value="""
            **tea!brew <orderID>** - Accept an order using its ID to brew it.
            **tea!decline <orderID> <reason>** - Decline an order using its ID.
            **tea!deliver <orderID>** - Deliver an order: get the invite to the server it was ordered in.
            **tea!list** - See all unclaimed orders.
            **tea!random** - Get assigned a random waiting order.
            **tea!blacklist <add/remove> <user>** - Blacklist or unblacklist a user.
            """)

        elif not blacklist_check.check(ctx.author):
            embed.add_field(name="Commands you can use:", value="""
            **tea!rules** - See ordering rules.
            **tea!ping** - See bot latency.
            **tea!invite** - Get an invite link for Discord Tea.
            **tea!feedback <comment>** - Send feedback to the team!
            **tea!rate <rating>** - Rate this service! Give a rating between 1 and 5.
            **tea!approval** - View the average rating for the service.
            **tea!order <order>** - Order some tea. 
            **tea!myorders** - See your current active orders.
            **tea!oinfo <orderID>** - Get the info of an order with its ID.
            """)

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("Invite me with this link: https://discordapp.com/api/oauth2/authorize?client_id=507004433226268699&permissions=2146958839&scope=bot\nJoin the support server: https://discord.gg/xUhjnnd")

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
        • Orders cannot contain people's names
        • Orders cannot contain text formatting or non-Latin characters, except numbers and !#$%&<>?".
        • Orders cannot contain links.
        • Must Include Tea

        Please respect these rules. Breaking any of them repeatedly will result in being blacklisted from the bot and/or banned from this server.**
        """)

    @commands.command()
    async def stats(self, ctx):
        embed = dicord.Embed(color=discord.Color.blue())

    @commands.command()
    async def approval(self, ctx):
        average = rating_data.get_average()
        await ctx.send(":star: **| Our average approval rating is: {}:star:**".format(round(average, 2)))

    @commands.command()
    async def blacklist(self, ctx, mode, user: discord.User):
        blist_log = discord.utils.get(self.client.get_all_channels(), id=524403883200610305)

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        if mode == 'add':
            blacklist_check.blacklist_add(user)
            await ctx.send(":white_check_mark: **| Blacklisted {}.**".format(user.name))
            await blist_log.send(":triangular_flag_on_post: **| `{}` has been blacklisted.**".format(user))
        elif mode == 'remove':
            blacklist_check.blacklist_remove(user)
            await ctx.send(":white_check_mark: **| Removed {} from the blacklist.**".format(user.name))
            await blist_log.send(":radio_button: **| `{}` was removed from the blacklist.**".format(user))
        

def setup(client):
    client.add_cog(UtilsCog(client))