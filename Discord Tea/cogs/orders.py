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
        self.order_count = 0
        self.total_order_count = 0
        self.locked = False
        self.ids_temp = [478690278530613269, 471555912012922881, 420042033818763285, 449994901048786944, 336281913578881027, 429312422323683338, 368860954227900416]

    @commands.command()
    async def lock(self, ctx):
        if ctx.author.id not in self.ids_temp:
            await ctx.send("you can't use this")
            return

        if self.locked == False:
            self.locked = True
            await ctx.send("locked orders")
        elif self.locked == True:
            self.locked = False
            await ctx.send("unlocked orders")

    @commands.command()
    async def order(self, ctx, *, order=None):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)
        order_count = 0

        if self.locked == True:
            await ctx.send(":santa: **| The Discord Tea staff are on Christmas break. They'll be ready to serve again in a day or two. Thanks for your patience!**")
            return

        if not order:
            await ctx.send(":grey_question: **| What type of tea would you like to order, {}?**".format(ctx.author.name))
            return

        if len(order) > 150:
            await ctx.send(":no_entry_sign: **| Your order must be under 150 characters long!**")
            return      

        for item in ["coffee", "c0ffee", "coff33", "c0ff3e", "c0ffe3", "coff3e", "coffe3"]:
            if item in order.lower():
                await ctx.send(":rage: **| Your order contained COFFEE! You TRAITOR!!**")
                return

        if "tea" not in order.lower():
            await ctx.send(":no_entry_sign: **| Your order must contain tea!**")
            return

        for orderid in self.order_ids:
            if self.order_ids[str(orderid)][2] == ctx.author:
                order_count += 1

        if order_count >= 2:
            await ctx.send(":no_entry_sign: **| You can only have 2 orders pending at once!**")
            return
        else:
            self.total_order_count += 1
            orderid = self.total_order_count
            self.order_count += 1
            if self.order_count >= 22:
                await ctx.send(":no_entry_sign: **| The order limit of 22 orders has been hit. Please wait hile our staff complete some orders.**")
                return
            elif self.order_count >= 6:
                await ctx.send("Ordered a **{}** for you! It will be delivered soon! Your order ID: `{}`\n\n:warning: Discord Tea is dealing with a large number of orders right now. Service may be delayed.".format(order, orderid))
            else:
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
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def remind(self, ctx):
        kitchen_channel = discord.utils.get(self.client.get_all_channels(), id=524040649973039107)

        await ctx.send(":white_check_mark: **| Reminded staff to brew your order!**")
        await kitchen_channel.send(":warning: **| @here, please check the order list! There are unbrewed orders waiting!**")

    @commands.command()
    async def brew(self, ctx, orderid):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

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
    async def decline(self, ctx, orderid, *, reason=None):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        try:
            self.order_ids[str(orderid)]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
        else:
            await ctx.send(":white_check_mark: **| You declined the order with ID `{}`.**".format(orderid))
            if reason:
                await order_log.send(":triangular_flag_on_post: **| Tea sommelier {} declined the order with ID `{}` with reason '{}'.**".format(ctx.author.name, orderid, reason))
                try:
                    await self.order_ids[str(orderid)][2].send(":triangular_flag_on_post: **| Your order of `{}` was declined by Tea Sommelier {} with reason '{}'.**".format(self.order_ids[str(orderid)][0], ctx.author, reason))
                except:
                    await self.order_ids[str(orderid)][3].send(":triangular_flag_on_post: **| {}, Your order of `{}` was declined by Tea Sommelier {} with reason '{}'.**".format(self.order_ids[str(orderid)][2].mention, self.order_ids[str(orderid)][0], ctx.author, reason))
                self.order_ids.pop(str(orderid), None)
                self.order_count -= 1
            else:
                await order_log.send(":triangular_flag_on_post: **| Tea sommelier {} declined the order with ID `{}` but they didn't specify why.**".format(ctx.author.name, orderid))
                try:
                    await self.order_ids[str(orderid)][2].send(":triangular_flag_on_post: **| Your order of `{}` was declined by Tea Sommelier {} but they didn't specify why.**".format(self.order_ids[str(orderid)][0], ctx.author))
                except:
                    await self.order_ids[str(orderid)][3].send(":triangular_flag_on_post: **| {}, Your order of `{}` declined by Tea Sommelier {} but they didn't specify why.**".format(self.order_ids[str(orderid)][2].mention, self.order_ids[str(orderid)][0], ctx.author))
                self.order_ids.pop(str(orderid), None)
                self.order_count -= 1

    @commands.command()
    async def deliver(self, ctx, orderid):
        order_log = discord.utils.get(self.client.get_all_channels(), id=524040719929704479)

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        try:
            self.order_ids[str(orderid)]
        except KeyError:
            await ctx.send(":no_entry_sign: **| No order with that ID!**")
        else:
            if self.order_ids[str(orderid)][1] == "waiting":
                await ctx.send(":no_entry_sign: **| That order is not ready for delivery!**")
            else:
                try:
                    invite = await self.order_ids[str(orderid)][3].create_invite(max_uses=1, reason="To deliver tea")
                except Exception as e:
                    await ctx.send(":x: **| There was an error creating invite.**")
                    print("ERROR CREATING INVITE: {}".format(str(e)))
                    try:
                        await self.order_ids[str(orderid)][2].send(":x: **| The bot couldn't create an invite to your server `{}` therefore your tea cannot be delivered. Give the bot create invite permissions and order again.**".format(self.order_ids[str(orderid)][3].guild.name))
                    except:
                        await self.order_ids[str(orderid)][3].send(":x: **| {}, The bot couldn't create an invite to this server therefore your tea cannot be delivered. Give the bot create invite permissions and order again.**".format(self.order_ids[str(orderid)][2].mention))
                    self.order_ids.pop(str(orderid), None)
                    self.order_count -= 1
                    return
                else:
                    try:
                        await ctx.author.send(":truck: **| Deliver the order to: {} in <{}>**".format(self.order_ids[str(orderid)][2], invite))
                    except:
                        await ctx.send(":mailbox_with_mail: **| You need to open your DMs for this command.**")
                    await order_log.send(":truck: **| Tea Sommelier {} is delivering the order with ID `{}`!**".format(ctx.author.name, orderid))
                    try:
                        await self.order_ids[str(orderid)][2].send(":truck: **| Tea Sommelier {} is delivering your order! Thanks for using our service!**".format(ctx.author))
                    except:
                        await self.order_ids[str(orderid)][3].send(":truck: **| {}, Tea Sommelier {} is delivering your order! Thanks for using our service!**".format(self.order_ids[str(orderid)][2].mention, ctx.author))
                    self.order_ids.pop(str(orderid), None)
                    self.order_count -= 1

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
            Customer: {} ({})
            Order ID: `{}`
            Order of: {}
            Ordered in: {}, #{}
            Order Status: {}
            **""".format(
                order[2],
                order[2].id,
                orderid,
                order[0],
                order[3].guild, order[3],
                order[1]
            ))

            await ctx.send(embed=embed)

    @commands.command()
    async def random(self, ctx):
        unfinished_orders = []

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

        if not sommelier_data.check(ctx.author):
            await ctx.send(":lock: **| Only Tea Sommeliers can use this command!**")
            return

        for orderid in self.order_ids:
            if self.order_ids[str(orderid)][1] == "waiting":
                unfinished_orders.append(orderid)

        if len(unfinished_orders) > 0:
            assigned_order = random.choice(unfinished_orders)
        else:
            await ctx.send(":no_entry_sign: **| There are no waiting orders right now!**")
            return

        await ctx.send(":white_check_mark: **| You've been assigned the order with ID `{}`! Start brewing!**".format(assigned_order))
        self.order_ids[str(orderid)][1] = "brewing"

    @commands.command(name="active-orders", aliases=["list", "list-o"])
    async def list_orders(self, ctx):

        if not ctx.guild.id == 524024216463605770:
            await ctx.send(":lock: **| This command cannot be used in this server!**")
            return

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
