import os
import discord
import json
import TOKEN
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
async def CML(ctx):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    string = ''
    try:
        for tag in doc.find_all("span",class_ = "mw-headline"):
            string += tag.text + '\n'
        await ctx.send(string)
    except:
        print('error')


@bot.command()
async def move(ctx, *,arg):
    if (len(arg) == 2):
        arg = arg.upper()
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    try:
        Information = ""
        counter = 0
        table1 = ['Damage: ' , 'Guard: ' , 'Startup: ' , 'Active: ' , 'Recovery: ' , 'On-Block: ' , 'Invuln: ']
        table2 = ['Version: ' , 'Damage: ' , 'Guard: ' , 'Startup: ' , 'Active: ' , 'Recovery: ' , 'On-Block: ' , 'Invuln: ']
        #Finds the span block with the ID of the button to be searched like 5p 6k etc.
        input = doc.find("span",class_ = "mw-headline", id = arg)
        mName = input.findChild('big')
        print(mName.get_text())
        #Goes back to the parent node
        h3Container = input.find_parent('h3')
        #Goes to the node immediately below it making sure its a div
        framesBox = h3Container.find_next_sibling('div')
        #Goes in the div and finds the attack info class
        #frames = framesBox.findChild("div", class_ = "attack-info")
        frames = framesBox.findChild("table", class_ = "wikitable attack-data")
        frameData = frames.findChild("tr")
        frameData2 = frameData.find_next_sibling("tr")
        frameList = frameData2.findChildren()
        #This works for moves that dont have extra properties. It wont work for 5D which has uncharged and charged moves
        #Or moves like ky's fireball maybe or anything ky
        if len(frameList) == 7:
            for child in frameList:
                Information += table1[counter] + child.text
                counter += 1
        if len(frameList) == 8:
            for child in frameList:
                Information += table2[counter] + child.text
                counter += 1
        await ctx.send(Information)
        #Print info in attack info 
        #print(frames.get_text())
        #await ctx.send(frameData2.get_text())
        #await ctx.send(arg + " is working")
        print (len(frameList))
        print ('A request was sent')
    except:
        #await ctx.send("Unknown move name")
        await ctx.send(arg + " doesn't working")
        print ("Something bugged. Maybe a wrong move that doesnt exist?")


bot.run(TOKEN.TOKEN)
