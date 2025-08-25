import requests
import os
import schedule
import asyncio
import discord
from discord.ext import commands
from Token import Discord_Token
import random

#meme api call
def Get_Meme():    
    response = requests.get ('https://meme-api.com/gimme')
    Meme_Data = response.json()
    print(response.status_code)
    return Meme_Data

#quote api call
def Get_Quote():
    response = requests.get ('https://zenquotes.io/api/today')
    Quote_Data = response.json()
    print(response.status_code)
    return Quote_Data

#discord intentions set
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = commands.Bot(command_prefix='!',intents = intents)

#Initilize varaibles
counter = 0

#Function for scheduling the quote
async def send_quote():
    await client.wait_until_ready()
    channel_id = 1328789622053929091
    channel = client.get_channel(channel_id)
    Quote_Data = Get_Quote()
    Quote = ''
    Author = ''
    Quote = Quote_Data[0]['q']
    Author = Quote_Data[0]['a']
    await channel.send("<@&1268048648965460028>")
    await channel.send(f"Quote of the day is: {Quote}")
    await channel.send(f"This quote is by: {Author}")
    print(f"Sent quote: {Quote}")
    print(f"Sent author: {Author}")
#Scheduling the time    
def schedule_task():
        schedule.every().day.at("12:48").do(lambda: client.loop.create_task(send_quote()))
async def schedule_send_quote():
    await send_quote()
#What happens when the bot is started         
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    schedule_task()   
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

#Purge command to wipe text channels
@client.command()
@commands.has_role('Purge')
async def purge(ctx):
        limit = 0
        async for msg in ctx.channel.history(limit=None):
            limit += 1
        await ctx.channel.purge(limit=limit)

#meme command to send a random meme
@client.command()
async def meme(ctx):
    Meme_Data = Get_Meme()
    Meme_Url = Meme_Data['preview'][2]
    await ctx.send(Meme_Url)
    print('Meme Sent')
#flip command to make decsions
@client.command()
async def flip(ctx):
    rand = random.randint(0,1)
    global counter
    if counter == 5:
        await ctx.send("I Love Chicken Bakes")
        print("Easter Egg Found!")
        counter = 0
    else:
        if rand == 1:
            await ctx.send("This is a BOOM!")
            print("We BOOMING")
            counter+= 1
        if rand == 0:
            await ctx.send("This is a DOOM!")
            print("We DOOMING")
            counter == 0

#Garmin command
@client.command()
async def garmin(ctx):
     await ctx.send("Okay Garmin Video Speichern")


#Join vc Command
@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
         Channel = ctx.author.voice.channel
         await Channel.connect()
    else:
         await ctx.send("Join a vc First")
 
#leave vc command        
@client.command(pass_context=True)
async def leave(ctx):
        if ctx.voice_client:
             await ctx.guild.voice_client.disconnect()
             await ctx.send("I left the vc")
        else:
             await ctx.send("I am not in a vc")



client.run(Discord_Token)