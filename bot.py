import discord 
import config
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import random 
from random import randint
import urllib.request
import json

bot = commands.Bot(command_prefix = "j!", description= "Bot made by Justin Chan")
bot.owner_id = 153714829964738560
bot.activity = discord.Game("{0}help for a list of commands!".format(bot.command_prefix))
bot.remove_command('help')

@bot.event
async def on_ready():
    print('We have logged in as {0.user} \nCreated by Justin Chan ({1})'.format(bot, bot.owner_id))

@bot.command()
async def stop(ctx):
    if ctx.message.author.id == bot.owner_id:
        await ctx.send("Good Bye World! :earth_africa:")
        await bot.logout()

@bot.command()
async def ping(ctx):
    await ctx.send('{0} Pong! {1}ms :ping_pong:'.format(ctx.message.author.mention,round(bot.latency*1000)))

@bot.command()
async def choose(ctx, *choices: str):
    try:
        myChoices = " ".join(choices)
        myChoices = myChoices.split(',')
        await ctx.send('I choose {0}'.format(random.choice(myChoices)))
    except Exception:
        await ctx.send('Enter at least 1 choice')
        return

@bot.command()
async def help(ctx):
    helpMsg = discord.Embed(
        title = 'Justin-Bot commands - Created in Python by Justin Chan',
        description = 'Commands :grin:',
        colour = discord.Colour.blue()
    )
    helpMsg.set_footer(text='Use {0} as prefix!'.format(bot.command_prefix))
    helpMsg.set_thumbnail(url='https://statici.behindthevoiceactors.com/behindthevoiceactors/_img/chars/aipom-pokemon-detective-pikachu-3.35.jpg')
    helpMsg.add_field(
        name='{0}ping'.format(bot.command_prefix),
        value='Returns the bot\'s latency.',
        inline=False     
    )
    helpMsg.add_field(
        name='{0}choose choice1,choice2,...'.format(bot.command_prefix),
        value='Randomly chooses a given choice.',
        inline=False
    )
    helpMsg.add_field(
        name='{0}nba player fullname'.format(bot.command_prefix),
        value='Returns the information of a given active nba player.',
        inline=False
    )
    helpMsg.add_field(
        name='{0}reddit subreddit'.format(bot.command_prefix),
        value='Returns a random post from the front page of the subreddit given.',
        inline=False
    )
    await ctx.send(embed=helpMsg)

@bot.command()
async def nba(ctx, *name: str):
    try:
        firstName = name[0]
        lastName = name[1]
        mainUrl = urllib.request.urlopen("http://data.nba.net/10s/prod/v1/today.json")
        urlData = json.loads(mainUrl.read().decode())
        playerEndUrl = urlData['links']['leagueRosterPlayers']
        teamEndUrl = urlData['links']['teams']
        
        playerUrl = "http://data.nba.net/10s"+playerEndUrl
        teamUrl = "http://data.nba.net/10s"+teamEndUrl
        playerUrl = urllib.request.urlopen(playerUrl)
        teamUrl = urllib.request.urlopen(teamUrl)
        playerData = json.loads(playerUrl.read().decode())
        teamData = json.loads(teamUrl.read().decode())
        
        lengthPlayers = len(playerData['league']['standard'])
        lengthTeams = len(teamData['league']['standard'])
        for x in range(lengthPlayers):
            tempLastName = playerData['league']['standard'][x]['lastName']
            tempFirstName = playerData['league']['standard'][x]['firstName']
            if tempLastName.lower() == lastName.lower() and tempFirstName.lower() == firstName.lower():
                firstName = playerData['league']['standard'][x]['firstName']
                lastName = playerData['league']['standard'][x]['lastName']
                jerseyNum = playerData['league']['standard'][x]['jersey']
                position = playerData['league']['standard'][x]['teamSitesOnly']['posFull']
                height = playerData['league']['standard'][x]['heightFeet'] + '\'' + playerData['league']['standard'][x]['heightInches'] + '\" (' + playerData['league']['standard'][x]['heightMeters'] + 'm)'
                weight = playerData['league']['standard'][x]['weightPounds'] + 'lb'
                teamSize = len(playerData['league']['standard'][x]['teams'])
                teamNum = playerData['league']['standard'][x]['teams'][teamSize-1]['teamId']

        for x in range(lengthTeams):
            tempTeamId = teamData['league']['standard'][x]['teamId']
            if tempTeamId == teamNum:
                teamName = teamData['league']['standard'][x]['fullName']

        nbaMsg = discord.Embed(
            title = '{0} {1} #{2}'.format(firstName,lastName,jerseyNum),
            description = ':basketball:',
            colour = discord.Colour.red()
        )
        nbaMsg.set_thumbnail(url='https://theundefeated.com/wp-content/uploads/2017/05/nba-logo.png?w=700')
        nbaMsg.add_field(
            name='Team',
            value='{0}'.format(teamName),
            inline=False
        )
        nbaMsg.add_field(
            name='Position',
            value='{0}'.format(position),
            inline=False
        )
        nbaMsg.add_field(
            name='Height',
            value='{0}'.format(height),
            inline=False
        )
        nbaMsg.add_field(
            name='Weight',
            value='{0}'.format(weight),
            inline=False
        )
        await ctx.send(embed=nbaMsg)
    except Exception:
        await ctx.send('Player not found!')
        return

@bot.command()
async def reddit(ctx, subreddit):
    output = await ctx.send('Working...')
    await output.delete()
    try:
        url = "https://old.reddit.com/r/"+subreddit
        source = requests.get(url, headers = {'User-agent': 'Justin-Bot v1'}).text
        soup = BeautifulSoup(source, 'lxml')
        siteTable = soup.find("div",{"class":"sitetable linklisting"})
    except Exception:
        await ctx.send('Subreddit not found')
        return

    try:
        post = siteTable.findAll("div",{"data-context":"listing"})
        randNum = randint(0,len(post)-1)
        while 'stickied' in post[randNum]["class"]:
            randNum = randint(0,len(post)-1)
        randPostTitle = post[randNum].find("div",{"class":"entry unvoted"}).div.p.a.text
        randPostLink = post[randNum]["data-url"]
    except Exception:
        await ctx.send('NSFW Subreddit. ')
        return

    if randPostLink.startswith('/r/'):
        randPostLink = "https://old.reddit.com"+randPostLink

    # one message for easy deletion
    await ctx.send('**Title:**\n{0}\n**Post:**\n{1}'.format(randPostTitle,randPostLink))
    
    

bot.run(config.TOKEN)