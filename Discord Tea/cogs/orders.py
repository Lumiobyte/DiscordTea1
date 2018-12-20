import discord
from discord.ext import commands
import random

import sys
sys.path.insert(0, 'D:/Python Coding/Discord Bots/Discord Tea/')
from utils import blacklist_check, sommelier_data

class OrdersCog:

    def __init__(self, client):
        self.client = client
        self.order_ids = {}

    @commands.command()
    async def order(self, ctx, *, order=None):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not order:
            await ctx.send(":grey_question: **| What type of tea would you like to order, {}?**".format(ctx.author.name))
            return

        if len(order) > 150:
            await ctx.send(":no_entry_sign: **| Your order must be under 150 characters long!**")
            return      

        if "coffee" in order.lower():
            await ctx.send(":rage: **| Your order contained COFFEE! You TRAITOR!!**")
            return

        if "tea" not in order.lower():
            await ctx.send(":no_entry_sign: **| Your order must contain tea!**")
        else:
            orderid = random.randint(0, 99999)
            await ctx.send("Ordered a **{}** for you! It will be delivered soon! Your order ID: `{}`".format(order, orderid))
            self.order_ids[str(orderid)] = [order, "waiting", ctx.author, ctx.channel]
            await order_log.send(":inbox_tray: **| Received order of `{}` with ID `{}`. Ordered by {} in server {}.**".format(order, orderid, ctx.author, ctx.guild.name))

    @commands.command()
    async def myorders(self, ctx):
        users_ids = []
        embed_value = ''
        order_count = 0
        embed = discord.Embed(color=discord.Color.orange())

        for orderid in self.order_ids:
            if self.order_ids[orderid][2] == ctx.author:
                users_ids.append(orderid)

        if len(users_ids) <= 0:
            embed.add_field(name="Your Active Orders (0)", value="You have no active orders! Use tea!order to order something.")
        else:
            for orderid in users_ids:
                order_count += 1
                embed_value += 'OrderID `{}`: order of `{}` - Status: `{}`\n'.format(
                    orderid,
                    self.order_ids[orderid][0],
                    self.order_ids[orderid][1]
                )
            embed.add_field(name="Your active orders ({})".format(order_count), value=embed_value)

        await ctx.send(embed=embed)

    @commands.command()
    async def oaccept(self, ctx, orderid):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        try:
            self.order_ids[str(orderid)]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
        else:
            if self.order_ids[str(orderid)][1] != "waiting":
                await ctx.send(":no_entry_sign: **| That order is already being processed by a sommelier!**")
            else:
                self.order_ids[str(orderid)][1] = "brewing"
                await ctx.send(":white_check_mark: **| You claimed the order of `{}`! Start brewing!**".format(self.order_ids[str(orderid)][0]))
                await order_log.send(":man: **| Tea sommelier {} claimed the order with ID `{}` and is now brewing it!**".format(ctx.author.name, orderid))
                try:
                    await self.order_ids[str(orderid)][2].send(":man: **| Tea Sommelier {} claimed your order and is brewing it!**".format(ctx.author))
                except:
                    await self.order_ids[str(orderid)][3].send(":man: **| {}, Tea Sommelier {} claimed your order and is brewing it!**".format(self.order_ids[str(orderid)][2].mention, ctx.author))      

    @commands.command()
    async def odecline(self, ctx, orderid, *, reason=None):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        try:
            self.order_ids[str(orderid)]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
        else:
            if self.order_ids[str(orderid)][1] != "waiting":
                await ctx.send(":no_entry_sign: **| That order is already being processed by a sommelier!**")
            else:
                await ctx.send(":white_check_mark: **| You declined the order with ID `{}`.**".format(orderid))
                if reason:
                    await order_log.send(":triangular_flag_on_post: **| Tea sommelier {} declined the order with ID `{}` with reason '{}'.**".format(ctx.author.name, orderid, reason))
                    try:
                        await self.order_ids[str(orderid)][2].send(":triangular_flag_on_post: **| Your order of `{}` was declined by Tea Sommelier {} with reason '{}'.**".format(self.order_ids[str(orderid)][0], ctx.author, reason))
                    except:
                        await self.order_ids[str(orderid)][3].send(":triangular_flag_on_post: **| {}, Your order of `{}` was declined by Tea Sommelier {} with reason '{}'.**".format(self.order_ids[str(orderid)][2].mention, self.order_ids[str(orderid)][0], ctx.author, reason))
                    self.order_ids.pop(str(orderid), None)
                else:
                    await order_log.send(":triangular_flag_on_post: **| Tea sommelier {} declined the order with ID `{}` but they didn't specify why.**".format(ctx.author.name, orderid))
                    try:
                        await self.order_ids[str(orderid)][2].send(":triangular_flag_on_post: **| Your order of `{}` was declined by Tea Sommelier {} but they didn't specify why.**".format(self.order_ids[str(orderid)][0], orderid, ctx.author))
                    except:
                        await self.order_ids[str(orderid)][3].send(":triangular_flag_on_post: **| {}, Your order of `{}` declined by Tea Sommelier {} but they didn't specify why.**".format(self.order_ids[str(orderid)][2].mention, self.order_ids[str(orderid)][0], ctx.author))
                    self.order_ids.pop(str(orderid), None)

    @commands.command()
    async def odeliver(self, ctx, orderid):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        try:
            self.order_ids[str(orderid)]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
        else:
            if self.order_ids[str(orderid)][1] != "brewing":
                await ctx.send(":no_entry_sign: **| That order is not ready for delivery!**")
            elif self.order_ids[str(orderid)][1] == "delivering":
                await ctx.send(":no_entry_sign: **| That order is already being delivered by a Tea Sommlier!**")
            else:
                try:
                    invite = await self.order_ids[str(orderid)][3].create_invite(max_uses=1, reason="To deliver tea")
                except Excpetion as e:
                    await ctx.send(":x: **| There was an error creating invite.**")
                    print("ERROR CREATING INVITE: {}".format(str(e)))
                    return
                else:
                    self.order_ids[str(orderid)][1] = "delivering"
                    try:
                        await ctx.author.send(":truck: **| Deliver the order to: <{}>**".format(invite))
                    except:
                        await ctx.send(":mailbox_with_mail: **| You need to open your DMs for this command.**")
                    await order_log.send(":truck: **| Tea Sommelier {} has claimed the order with ID `{}` for delivery!**".format(ctx.author.name, orderid))
                    try:
                        await self.order_ids[str(orderid)][2].send(":truck: **| Tea Sommelier {} has claimed your order for delivery! Expect it to arrive soon!**".format(ctx.author))
                    except:
                        await self.order_ids[str(orderid)][3].send(":truck: **| {}, Tea Sommelier {} has claimed your order for delivery! Expect it to arrive soon!**".format(self.order_ids[str(orderid)][3].mention, ctx.author))


    @commands.command()
    async def ofinish(self, ctx, orderid):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        try:
            self.order_ids[str(orderid)]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
        else:
            if self.order_ids[str(orderid)][1] != "delivering":
                await ctx.send(":no_entry_sign: **| That order is not ready to be declared finished!**")
            else:
                await ctx.send(":white_check_mark: **| Order Completed!**")
                await order_log.send(":outbox_tray: **| Order with ID `{}` was finished by Tea Sommelier {}.**".format(orderid, ctx.author.name))
                self.order_ids.pop(str(orderid), None)

    @commands.command()
    async def oinfo(self, ctx, orderid):
        try:
            self.order_ids[str(orderid)]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
        else:
            order = self.order_ids[str(orderid)]
            embed = discord.Embed(color=discord.Color.teal())
            embed.add_field(name="Order Information ({})".format(orderid), value="""**
            Customer: {}
            Order ID: `{}`
            Order of: {}
            Ordered in: {}, #{}
            Order Status: {}
            **""".format(
                order[2],
                orderid,
                order[0],
                order[3].guild, order[3],
                order[1]
            ))

            await ctx.send(embed=embed)

    @commands.command(name="active-orders", aliases=["list", "list-o"])
    async def list_orders(self, ctx):

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        order_count = 0
        helper_counter = 0
        helper_value = ''
        embed_value_list = []
        list_of_embeds = []

        for orderid in self.order_ids:
            order_count += 1
            helper_counter += 1
            helper_value += "**ID `{}`: `{}` ordered by `{}`. Status: `{}`**\n".format(orderid, self.order_ids[orderid][0], self.order_ids[orderid][2], self.order_ids[orderid][1])
            if helper_counter >= 5:
                embed_value_list.append(helper_value)
                helper_counter = 0
                helper_value = ''

        if helper_value != '':
            embed_value_list.append(helper_value)

        if order_count <= 0:
            embed = discord.Embed(color=discord.Color.magenta())
            embed.add_field(name="All active orders ({})".format(order_count), value="No active orders!")
            await ctx.send(embed=embed)
            return

        for embed_value in embed_value_list:
            embed = discord.Embed(color=discord.Color.magenta())
            embed.add_field(name="All Active Orders ({})".format(order_count), value=embed_value)
            list_of_embeds.append(embed)

        for embed in list_of_embeds:
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(OrdersCog(client))