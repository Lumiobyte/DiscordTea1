import discord
from discord.ext import commands
from utils import blacklist_check, sommelier_data

TOKEN = 'TOKEN'

client = commands.Bot(command_prefix=["tea!", "Tea!"])
client.remove_command('help')

cogs = ['cogs.orders', 'cogs.owner', 'cogs.utilities', 'cogs.events']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print("ERROR: Could not load cog '{}': {}".format(cog, str(e)))

@client.event
async def on_ready():
    print("Discord Tea is online!")
    await client.change_presence(activity=discord.Game(name="with tea | tea!help"))

@client.check
async def is_blacklisted(ctx):
    if blacklist_check.check(ctx.author):
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="You are blacklisted.", value="You have been blacklisted and cannot use this bot.\nIf you wish to appeal, please join https://discord.gg/xUhjnnd")
        await ctx.send(embed=embed)
        return False
    else:
        return True

client.run(TOKEN)
