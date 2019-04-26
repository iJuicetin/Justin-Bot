import discord 
import config
import requests
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Yeet its working')

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))
    await client.process_commands(message)

@client.command()
async def about():
    await client.say("Shitty bot made by Justin")

@client.command()
async def help():
    await client.say("``` **Commands:** \n")

@client.command()
async def ping():
    await client.say("Pong!")

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

# Using Riot Games API, this command will return the summoners rank!
@client.command()
async def league(*SummonerNameIn):
    SummonerName = ''
    # Loop through when name has spaces
    for word in SummonerNameIn:
        SummonerName += word
    # Retrieve ID from summoner name
    responseJSON = requestSummonerData(SummonerName)
    ID = responseJSON['id']
    ID = str(ID)
    # Get ranked data using ID
    rankedJSON = requestRankedData(ID)
    print(len(rankedJSON))
    Name = str(rankedJSON[0]['summonerName'])
    await client.say("**Summoner: ** "+Name+"\n")
    for i in range(len(rankedJSON)):
        QType = str(rankedJSON[i]['queueType'])
        QType = QType.replace("_"," ")
        Tier = str(rankedJSON[i]['tier'])
        Rank = str(rankedJSON[i]['rank'])
        lp = str(rankedJSON[i]['leaguePoints'])
        # Print out data
        await client.say("**Queue: **"+ QType + "\n" +"**Rank: **"+Tier+" "+Rank+" "+ lp +" lp ")

def requestSummonerData(SummonerName):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+SummonerName+"?api_key="+config.RiotAPI
    print(URL)
    response = requests.get(URL)
    return response.json()

def requestRankedData(ID):
    URL = "https://na1.api.riotgames.com/lol/league/v4/positions/by-summoner/"+ID+"?api_key="+config.RiotAPI
    print(URL)
    response = requests.get(URL)
    return response.json()

client.run(config.TOKEN)