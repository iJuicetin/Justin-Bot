import discord 
import config
from discord.ext import commands
import random

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('{0} Pong! {1}ms :ping_pong:'.format(ctx.message.author.mention,round(bot.latency*1000)))

@bot.command()
async def choose(ctx, *choices: str):
    try:
        myChoices = " ".join(choices)
        myChoices = myChoices.split(',')
        await ctx.send(random.choice(myChoices))
    except Exception:
        await ctx.send('Enter at least 1 choice')
        return
        
bot.run(config.TOKEN)