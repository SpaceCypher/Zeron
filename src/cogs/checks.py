import time
import nextcord
import os
import random
import psutil 
from datetime import datetime
from nextcord import user
from nextcord.ext import commands
from nextcord.ext import commands, tasks
import aiohttp
from io import BytesIO
import requests
from nextcord import ButtonStyle
from nextcord.ui import button, View, Button
from datetime import datetime

us = 0
um = 0
uh = 0
ud = 0

class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        intents = nextcord.Intents.default()
        intents.members = True
        intents.presences = True
        self.botuptime.start()
    @tasks.loop(seconds=2.0)
    async def botuptime(self):
        global uh, us, um, ud
        us += 2
        if us == 60:
            us = 0
            um += 1
            if um == 60:
                um = 0
                uh += 1
                if uh == 24:
                    uh = 0
                    ud += 1    
    @commands.command(
        aliases=["statistics", "stat", "statistic"],
        description="Shows the bot's statistics",
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats(self, ctx):
        global ud, um, uh, us
        em = nextcord.Embed(title="Zeron Stats",color=nextcord.Color.random())
        em.add_field(name="Days:", value=ud, inline=True)
        em.add_field(name="Hours:", value=uh, inline=True)
        em.add_field(name="Minutes:", value=um, inline=True)
        em.add_field(name="Seconds:", value=us, inline=True)
        em.add_field(name="CPU usage:", value=f"{psutil.cpu_percent()}%", inline=True)
        em.add_field(name="RAM usage:", value=f"{psutil.virtual_memory()[2]}%", inline=True)
        em.set_image(url=self.bot.avatar.url)
        await ctx.send(embed=em)    
    @commands.command(aliases=['minfo','uinfo','whois']) 
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def memberinfo(self,ctx,member:nextcord.Member):
        if member==None:
            member=ctx.author
        if member.status == nextcord.Status.dnd:
            s="**Do Not Disturb |** 🔴"
        elif member.status == nextcord.Status.online:
            s="**Online |** 🟢"
        elif member.status == nextcord.Status.idle:
            s="**Idle |** 🟠"
        elif member.status == nextcord.Status.offline:
            s="**Offline |** ⚫" 
        embed=nextcord.Embed(color=nextcord.Colour.green(),timestamp=ctx.message.created_at)
        embed.add_field(name="Username:",value=member.name,inline=False)
        embed.add_field(name="Nickname:",value=member.nick,inline=False)
        embed.add_field(name="Status: ", value=s,inline=False) 
        if bool(member.bot)==False:
            bo="Human 👨"
        elif bool(member.bot)==True:
            bo="Bot 🤖"
        embed.add_field(name="User: ", value=bo,inline=False)
        if bool(member.premium_since)==False:
            b_e='<a:no:909765403872481280>'
        elif bool(member.premium_since)==True:
            b_e='<a:yes:909765403801182208>'
        embed.add_field(name="Booster: ", value=b_e,inline=True)   
        roles = [role for role in member.roles]
        rr=", ".join([role.mention for role in roles][1:])
        embed.add_field(name="ID Created At:",value=member.created_at.strftime("%a, %d %B %Y , %I:%M %p"),inline=False)
        embed.add_field(name="Joined At:",value=member.joined_at.strftime("%a, %d %B %Y , %I:%M %p"),inline=False)
        embed.add_field(name="Top Role: ", value=member.top_role.mention,inline=False)
        embed.add_field(name=f"Roles({len(roles)-1}): ", value=rr,inline=False)
        if member.activity==None:
            embed.add_field(name="Activity:",value=f"```No Activity```",inline=False)   
        else:
            embed.add_field(name="Activity:",value=f"```{member.activity}```",inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(icon_url=ctx.author.avatar.url,text=f"Info requested by {ctx.author.name}")
        await ctx.send(embed=embed)
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def serverinfo(self,ctx):
        name=str(ctx.guild.name)
        owner=str(ctx.guild.owner)
        region=str(ctx.guild.region)
        s_id=str(ctx.guild.id)
        mc=str(ctx.guild.member_count)
        icon=str(ctx.guild.icon.url)
        embed=nextcord.Embed(title="Server Information",color=nextcord.Colour.from_rgb(3, 252, 198),timestamp=ctx.message.created_at)
        embed.add_field(name="Server Created On",value=f"<t:{int(ctx.guild.created_at.timestamp())}:R>",inline=True)
        embed.add_field(name="Server Name",value=name,inline=True)
        embed.add_field(name="Server Region",value=region,inline=False)
        embed.add_field(name= "Server Owner",value=owner,inline=False)
        embed.add_field(name="Server ID",value=s_id,inline=False)
        embed.add_field(name="Members",value=mc,inline=True)
        embed.add_field(name="Humans 👨",value=len(list(filter(lambda m:not m.bot,ctx.guild.members))),inline=False)
        embed.add_field(name="Bots 🤖",value=len(list(filter(lambda m: m.bot,ctx.guild.members))),inline=False)
        embed.add_field(name="Text channels",value=len(ctx.guild.text_channels),inline=False)
        embed.add_field(name="Voice channels",value=len(ctx.guild.voice_channels),inline=False)
        embed.add_field(name="Server Roles",value=len(ctx.guild.roles),inline=False)
        embed.set_thumbnail(url=icon)
        embed.set_footer(icon_url=ctx.author.avatar.url,text=f"Info requested by {ctx.author.name}")
        await ctx.trigger_typing()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Checks(bot))