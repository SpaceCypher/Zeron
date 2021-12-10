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
from simpcalc import simpcalc    
class InteractiveView(nextcord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=100)
        self.expr = "  "
        self.ctx=ctx
        self.calc = simpcalc.Calculate()
  

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "1"
        embed=nextcord.Embed(title=f"```{self.expr} ```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "2"
        embed=nextcord.Embed(title=f"```{self.expr} ```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "3"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "+"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "4"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "5"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "6"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            self.expr += "/"
            embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
            await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "7"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "8"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "9"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="x", row=2)
    async def multiply(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "*"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "."
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "0"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except : # if you are function only, change this to BadArgument
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "-"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += "("
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr += ")"
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, label="AC", row=4)
    async def clear(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr = ""
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(style=nextcord.ButtonStyle.red, label="X", row=4)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.expr = self.expr[:-1]
        embed=nextcord.Embed(title=f"```{self.expr}```",color=nextcord.Color.from_rgb(255, 255, 255))
        await interaction.message.edit(embed=embed)
    async def interaction_check(self, interaction) -> bool:
        if interaction.user !=self.ctx.author:
            await interaction.response.send_message("You didn't request the command" , ephemeral=True)
        else:
            return True
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
class Calculator(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(aliases=['calc'])    
    async def calculator(self,ctx):
        view = InteractiveView(ctx)
        embed=nextcord.Embed(title="```\n```",color=nextcord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=embed,view=view)  
def setup(bot):
    bot.add_cog(Calculator(bot))
