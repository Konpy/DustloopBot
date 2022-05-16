import os
import discord
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from discord.ext import commands

url = "https://www.dustloop.com/wiki/index.php?title=GGST/Jack-O"
bot = commands.Bot(command_prefix = '!')


@bot.event
async def on_ready():
    print("Potato Bot Ready")

@bot.command()
async def test(ctx):
    await ctx.send("Hey there")

@bot.command()
async def doggy(ctx):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    imgurl = response.json()['message']
    await ctx.send(imgurl)

@bot.command()
async def move(ctx, arg):
    if (len(arg) < 4):
        arg = arg.upper()
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    try:
        #Finds the span block with the ID of the button to be searched like 5p 6k etc.
        input = doc.find("span",class_ = "mw-headline", id = arg)
        #Goes back to the parent node
        h3Container = input.find_parent('h3')
        #Goes to the node immediately below it making sure its a div
        framesBox = h3Container.find_next_sibling('div')
        #Goes in the div and finds the attack info class
        frames = framesBox.findChild("div", class_ = "attack-info")
        #Print info in attack info 
        #print(frames.get_text())
        await ctx.send(frames.get_text())
        #await ctx.send(arg + " is working")
        print ('A request was sent')
    except:
        #await ctx.send("Unknown move name")
        await ctx.send(arg + " doesn't working")
        print ("Something bugged. Maybe a wrong move that doesnt exist?")


bot.run('TOKEN HERE')
