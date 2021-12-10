'''Our required imports'''
import asyncio
import datetime
import inspect
import io
from logging import exception
import asyncpg
import json
import os
import platform
import random
from rich.progress import track
import sys
from nextcord.ext import commands, menus
import time
from contextlib import suppress
from io import BytesIO
from random import randint
from urllib import parse
from urllib.parse import quote_plus
import nextcord 
from nextcord import channel
import praw
import requests
import contextlib
from nextcord import DMChannel, User, message
from nextcord.colour import Color
from nextcord.ext import commands
from nextcord.ext.commands import (ChannelNotFound, CommandNotFound, Context,
                                   command)
from nextcord.ext.commands.core import has_permissions
from nextcord.utils import get
from PIL import Image
from pyfiglet import figlet_format
import json

'''Loading The Bot Name And The Token'''
f = open('config.json')
data = json.load(f)
bot_token=data['token']
a=figlet_format(data['bot_name'], font='ogre')
'''Intents are required'''
intents = nextcord.Intents.all()
'''Change the default ? to anything you want'''
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
  print(f"{a}\n Has Connected To nextcord")


#load cogs
files = []
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        files.append(f"cogs.{filename[:-3]}")
        print(f"Loaded ---> {filename}")
for file in track(files, description="Standby-----"):
    bot.load_extension(file)
# load jishaku (a debugging tool) if you want, its optional
# pip install jishaku
# bot.load_extension("jishaku")   
class HelpEmbed(nextcord.Embed): # Our embed with some preset attributes to avoid setting it multiple times
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
        self.set_footer(text=text)
        self.color = nextcord.Color.blurple()


class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(

                    command_attrs={
                "help" : "The help command for the bot",
                "aliases": ['commands',"HELP","Help"]
            }
        ) # create our class with some aliases and cooldown
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)    
    async def send(self, **kwargs):
        """a short cut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """triggers when a `<prefix>help` is called"""
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        usable = 0 

        for cog, commands in mapping.items(): #iterating through our mapping of cog: commands
            if filtered_commands := await self.filter_commands(commands): 
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog: # getting attributes dependent on if a cog exists or not
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No Category"
                    description = "Commands with no category"

                embed.add_field(name=f"{name} [{amount_commands}]", value=description)

        embed.description = f"{len(bot.commands)} commands | {usable} usable" 

        await self.send(embed=embed)

    async def send_command_help(self, command):
        embed = nextcord.Embed(color=0x42cbf5)
        embed.add_field(name="Command Description:", value=f"{command.help}")
        embed.add_field(name="Syntax:", value=f"```{self.get_command_signature(command)}```",inline=False)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        else:
            embed.add_field(name="Aliases", value="No Aliases", inline=False)  
            
        if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
            embed.add_field(name="Cooldown",value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = HelpEmbed(title=title, description=description )

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help )
           
        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())
        


bot.help_command = MyHelp()

bot.run(bot_token)