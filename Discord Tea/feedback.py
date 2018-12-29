import discord
from discord.ext import commands

import sys
sys.path.insert(0, 'D:/Python Coding/Discord Bots/Discord Tea/')
from utils import rating_data

class FeedbackCog:

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def feedback(self, ctx, *, comment):
        feedback_log = discord.utils.get(self.client.get_all_channels(), id=524769713214062612)

        await ctx.send(":white_check_mark: **| Your feedback has been sent. Thanks, {}!**".format(ctx.author.name))
        await feedback_log.send(":star: **| Received feedback from `{}`: `{}`**".format(ctx.author, comment))

    @commands.command()
    async def rate(self, ctx, rating):
        feedback_log = discord.utils.get(self.client.get_all_channels(), id=524769713214062612)
        stars = ''

        try:
            rating = int(rating)
        except:
            await ctx.send(":no_entry_sign: **| Your rating must be between 1 and 5 and cannot be a decimal!**")
            return

        if rating > 5 or rating < 1:
            await ctx.send(":no_entry_sign: **| Your rating must be between 1 and 5 and cannot be a decimal!**")
            return

        for i in range (0, rating):
            stars += ':star:'
        await ctx.send(":star: **| You rated this service {}! Thanks for your feedback!**".format(stars))
        await feedback_log.send(":star: **| Received rating from `{}`: {}**".format(ctx.author, stars))
        rating_data.add_rating(rating)


def setup(client):
    client.add_cog(FeedbackCog(client))
