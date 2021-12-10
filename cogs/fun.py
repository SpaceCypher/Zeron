import datetime
from re import M, U  
import nextcord
import aiohttp
import textwrap
from nextcord import embeds
from nextcord.colour import Color
from nextcord.components import Button
from nextcord.embeds import Embed
from nextcord.ext import commands
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.ui.view import View
from nextcord.ext import commands
import json
from PIL import Image
from io import BytesIO
import random
import json
import requests
import asyncio
import urllib
import praw
import urllib
from time import *
class Nmeme(nextcord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=100)

        self.value = None
        self.ctx = ctx             	
    @nextcord.ui.button(label='Next Meme',  emoji="👏",style=nextcord.ButtonStyle.green)
    async def next_meme(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.ctx.author == interaction.user:
            pass
        else:
            await interaction.response.send_message("You didn't request the command", ephemeral=True)
        MApi=urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')
        Md=json.load(MApi)
        murl=Md['url']
        murlt=Md["postLink"]
        mn=Md['title']
        mu=Md["ups"]
        ms=Md['subreddit']
        em=nextcord.Embed(title=mn,url=murlt)
        em.set_image(url=murl)
        em.set_footer(text=f"👍 {mu} | 💬 {random.randint(1,100)}")
        await interaction.message.edit(embed=em)
    @nextcord.ui.button(label='End Meme Session',style=nextcord.ButtonStyle.red)
    async def ems(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()
    async def interaction_check(self, interaction) -> bool:
        if interaction.user !=self.ctx.author:
            await interaction.response.send_message("You didn't request the command" , ephemeral=True)
        else:
            return True    
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def wanted(self,ctx,user:nextcord.Member=None):
        if user==None:
            user=ctx.author
        wanted=Image.open("wanted.jpg")
        asset=user.avatar.replace(size=128)
        data=BytesIO(await asset.read())
        pfp=Image.open(data)
        pfp=pfp.resize((177,177))
        wanted.paste(pfp,(119,214))
        wanted.save("profile.jpg")
        await ctx.send(file=nextcord.File("profile.jpg"))
    @commands.command()
    async def joke(self,ctx):
        url1="https://v2.jokeapi.dev/joke/Any?type=twopart"
        r=requests.get(url1)  
        joke1=r.json()
        s=joke1["setup"]
        d=joke1["delivery"]
        em1=nextcord.Embed(title="JOKE:",description=f"{s}\n||{d}||",color=nextcord.Color.random())
        await ctx.send(embed=em1)
    @commands.command()
    async def meme(self,ctx):
        MApi=urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')
        Md=json.load(MApi)
        murl=Md['url']
        murlt=Md["postLink"]
        mn=Md['title']
        mu=Md["ups"]
        ms=Md['subreddit']
        em=nextcord.Embed(title=mn,url=murlt)
        em.set_image(url=murl)
        em.set_footer(text=f"👍 {mu} | 💬 {random.randint(1,100)}")
        view=Nmeme(ctx)
        message=await ctx.send(view=view,embed=em)
        await view.wait()
        if view.value ==False:
            for button in view.children:
                button.disabled = True
        else:
            for button in view.children:
                button.disabled = True
        await view.wait()        
        await message.edit(view=view)        
            
            
    @commands.command()
    async def pokedex(self,ctx,pname):
        url11=f"https://some-random-api.ml/pokedex?pokemon={pname}"
        r11=requests.get(url11)  
        ppdex=r11.json()
        d=ppdex["description"]
        w=ppdex["weight"]
        h=ppdex["height"]
        t=ppdex["type"]
        n=ppdex["name"]
        g=ppdex["gender"]
        a=ppdex["abilities"]
        em_p=nextcord.Embed(title=f"Pokedex-",description=d)  
        em_p.add_field(name="Name",value=n)
        em_p.add_field(name="Height",value=h)
        em_p.add_field(name="Weight",value=w)
        gens = [j for j in g]
        rr1=", ".join(gens)
        em_p.add_field(name="Gender",value=rr1)
        typ = [types for types in t]
        t1=", ".join(typ)
        em_p.add_field(name="Type",value=f"{t1}")
        abs = [i for i in a]
        rr=", ".join(abs)
        em_p.add_field(name="Abilities",value=rr)
        img1=ppdex["sprites"[:]]
        img=img1["animated"]
        em_p.set_thumbnail(url=img)
 
        await ctx.send(embed=em_p)


def setup(bot):
    bot.add_cog(Fun(bot))