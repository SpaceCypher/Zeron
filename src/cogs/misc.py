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

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name="ping")
    async def ping(self,ctx):
        a=await ctx.send(content=f"Pinging....``000``")
        await a.edit(content=f" Ping : ``{(round(self.bot.latency* 1000))}`` ms") 
def setup(bot):
    bot.add_cog(Misc(bot))
        