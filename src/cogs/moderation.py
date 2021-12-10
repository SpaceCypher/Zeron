import nextcord
from nextcord.channel import CategoryChannel,DMChannel
from nextcord.colour import Color
from nextcord.components import Button
from nextcord.embeds import Embed
from nextcord.ext import commands
from nextcord.ext.commands.cooldowns import BucketType
from nextcord.ui.view import View
from nextcord.ext import commands
import json
import random
import asyncio
from datetime import datetime
from difflib import get_close_matches

from nextcord.webhook import sync


class AllConfirm(nextcord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=200)
        self.value = None
        self.ctx=ctx

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.grey,emoji="<a:yes:909765403801182208>")
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.grey, emoji="<a:no:909765403872481280>")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()
    async def interaction_check(self, interaction) -> bool:
        if interaction.user !=self.ctx.author:
            await interaction.response.send_message("You can't use that!!" , ephemeral=True)
        else:
            return True  
BOT_USER_ID="897762972603150346"
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send
    @commands.command(name="tempban")
    @commands.has_permissions(ban_members=True)
    async def tempban(self,ctx, user:nextcord.User, time=None,reason=None):
        if reason==None:
            reason="No Reason"
            if user!= None:
                if time==None:
                    em = nextcord.Embed(title=f"<a:yes:909765403801182208> | {user.name} Was Banned indefinitely")
                    await ctx.send(embed=em) 
                    await ctx.guild.ban(user) 
                if time !=None :   
                    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
                    tempban1 = int(time[0]) * time_convert[time[-1]]     
                    em = nextcord.Embed(title=f"<a:yes:909765403801182208> | `{user.name}` Was Banned | Duration: {tempban1}{time[1:]} | Reason:{reason}")
                    await ctx.send(embed=em) 
                    if bool(user.bot)==True:
                        await ctx.guild.ban(user)
                        await asyncio.sleep(tempban1)
                        await ctx.guild.unban(user) 
                    else:    
                        await  DMChannel.send(user,f"**{ctx.guild.name}**: You have been banned for {tempban1}{time[1:]}\n**Reason:** {reason}")      
                        await ctx.guild.ban(user)
                        await asyncio.sleep(tempban1)
                        await ctx.guild.unban(user)  
            else:
                em = nextcord.Embed(title=f"<a:no:909765403872481280> | Member To Ban Was  Found")
                await ctx.send(embed=em) 
    @commands.command(name="ban", description="Bans the member from your server.")
    
    
    async def ban(self, ctx, member: nextcord.Member = None, *, reason=None):
        """
        **Info**: Bans a member
        """
        if member == None:
            embed1 = nextcord.Embed(
                title="Ban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="Ban yourself... only a skid would do that XD !",
            )
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",)
            return await ctx.send(embed=em3)
        guild = ctx.guild
        banEmbed = nextcord.Embed(title=f"Moderation Action <:moderation:910472145824542721> | Ban Case ",color=nextcord.Color.red())
        banEmbed.add_field(name="Reason: ", value=reason)
        view=AllConfirm(ctx)
        await ctx.send(embed=banEmbed,view=view)
        await view.wait()
        if view.value==False:
            em = nextcord.Embed(title=f"<a:no:909765403872481280> | *{member.name} Was Not Banned!*")
            await ctx.send(embed=em)
        elif view.value== True:
            em = nextcord.Embed(title=f"<a:yes:909765403801182208> | *{member.name} Was Banned!*")
            await ctx.send(embed=em)
            await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
            await member.ban(reason=reason)
    @commands.command(description="Lucas unban method")    
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,*,member):
        f"""
        **Info**: Unbans a member
        """
        banned_user = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_user:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
        view=AllConfirm(ctx)        
        if view.value==False:
            em = nextcord.Embed(title=f"<a:no:909765403872481280> | *{member.name} Was Not Unbanned!*")
            await ctx.send(embed=em)
        elif view.value== True:
            em = nextcord.Embed(title=f"<a:yes:909765403801182208> | *{member.name} Was Unbanned!*")
            await ctx.send(embed=em)
    @commands.command(name="kick", description="Kicks the member from your server.")
    
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                title="Kick Error", description="Member to kick - Not Found")
            return await ctx.send(embed=embed1)
        if not (ctx.guild.me.guild_permissions.kick_members):
            embed2 = nextcord.Embed(title="Kick Error",description="I require the ``Kick Members`` permisson to run this command - Missing Permission")
            return await ctx.send(embed=embed2)
        if member.id == ctx.author.id:
            embed = nextcord.Embed(title="Kick Error", description="Can't kick yourself ",)
            return await ctx.send(embed=embed)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        kickEmbed = nextcord.Embed(title=f"Moderation Action <:moderation:910472145824542721> | Kick Case ",color=nextcord.Color.red())
        kickEmbed.add_field(name="Reason: ", value=reason)
        view=AllConfirm(ctx)
        await ctx.send(embed=kickEmbed,view=view)
        await view.wait()
        view=AllConfirm(ctx)        
        if view.value==False:
            em = nextcord.Embed(title=f"<a:no:909765403872481280> | *{member.name} Was Not Kicked!*")
            await ctx.send(embed=em)
        elif view.value== True:
            em = nextcord.Embed(title=f"<a:yes:909765403801182208> | *{member.name} Was Kicked!*")
            await ctx.send(embed=em)
        await member.send(f"You got kicked in **{ctx.guild}** | Reason: **{reason}**")
        await member.kick(reason=reason)
    @commands.command(aliases=["cs", "ci", "channelinfo"])
    
    async def channelstats(self, ctx, channel: nextcord.TextChannel = None):
        f"""
        **Info**: Get ChannelStats
        *Syntax*: "{self.ctx.prefix}" channelstats [channel]
        """
        if channel == None:
            channel = ctx.channel

        embed = nextcord.Embed(
            title=f"**ChannelStats for {channel.name}**",
            description=f"{'Category :{}'.format(channel.category.name) if channel.category else 'Channel is not in any category'}",
       color=nextcord.Color.random())
        embed.add_field(name="Channel Guild:-", value=ctx.guild.name, inline=True)
        embed.add_field(name="Channel Id:-", value=channel.id, inline=False)
        embed.add_field(name="Channel Topic:-",value=f"{channel.topic if channel.topic else 'No topic.'}",inline=False,)
        embed.add_field(name="Channel Position:-", value=channel.position, inline=True)
        embed.add_field(name="Channel Slowmode?", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="Channel is NSFW?", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Channel Permissions Synced?", value=bool(CategoryChannel.permissions_synced), inline=True)
        embed.add_field(name="Channel is Annoucement?", value=channel.is_news(), inline=True)
        embed.add_field(name="Channel Hash:", value=hash(channel), inline=True)
        embed.add_field(name="Channel Creation Time:", value=channel.created_at.strftime("%a, %d %B %Y , %I:%M %p"), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
    @commands.command(name="tempmute", description="Mutes a member indefinitely.")
    @commands.has_permissions(manage_messages=True)
    
    async def tempmute(
        self, ctx, member: nextcord.Member = None, time=None, *, reason=None
    ):
        guild = ctx.guild
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if member == None:
            em1 = nextcord.Embed(
                title="Tempmute Error", description="Member to mute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Tempmute Error", description="Don't bother, ive tried"
            )
            return await ctx.send(embed=em5)
        if time == None:
            em2 = nextcord.Embed(
                title="Tempmute Error", description="Time to mute - Not Found"
            )
            return await ctx.send(embed=em2)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Tempmute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Tempmute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Tempmute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Tempmute Error",
                description="Muted role too high to give to a member",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )

        if not time == None:
            time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            tempmute = int(time[0]) * time_convert[time[-1]]
            embed = nextcord.Embed(
                title="Tempmute Success",
                description=f"{member.mention} was muted ",
                colour=nextcord.Colour.blue(),
            )
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Duration", value=time)
            await ctx.send(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(
                f"You have been muted from: **{guild.name}** | Reason: **{reason}** | Time: **{time}**"
            )
            if not time == None:
                await asyncio.sleep(tempmute)
                await member.remove_roles(mutedRole)
                await member.send(f"You have been unmuted from **{guild}**")
            return


    @commands.command(
        name="mute", description="Mutes a member for a specific amount of time."
    )
    
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: nextcord.Member = None, *, reason=None):
        guild = ctx.guild
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )
        if member == None:
            em1 = nextcord.Embed(
                title="Mute Error", description="Member to mute - Not Found"
            )
            return await ctx.send(embed=em1)

        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Mute Error", description="Error"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Mute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Mute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Mute Error",
                description="I require the **Manage Roles** permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Mute Error",
                description="Muted role too high to give to a member",
            )
            return await ctx.send(embed=em3)
      

        embed = nextcord.Embed(
            title="Mute Success",
            description=f"{member.mention} was muted Indefinitly ",
            colour=nextcord.Colour.blue(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(
            f"You have been muted from: **{guild.name}** | Reason: **{reason}**"
        )
        return

    @commands.command(name="unmute", description="Unmutes a muted member.")
    
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: nextcord.Member = None, *, reason=None):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Unmute Error", description="Member to unmute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Unmute Error", description="wHat? <:WHA:815331017854025790>"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Unmute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Unmute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Unmute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Unmute Error",
                description="Muted role too high to remove from a member",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )

        embed = nextcord.Embed(
            title="Unmute Success",
            description=f"{member.mention} was unmuted ",
            colour=nextcord.Colour.blue(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.remove_roles(mutedRole, reason=reason)
        await member.send(
            f"You have been unmuted from: **{guild.name}** | Reason: **{reason}**"
        )
        return

    @commands.command(description="Clears a bundle of messages.",aliases=['purge'])
    
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        amount = amount + 1
        if amount > 101:
            em1 = nextcord.Embed(
                title="Clear Error",
                description="Purge limit exedeed - Greater than 100",
            )
            return await ctx.send(embed=em1)
        else:
            await ctx.channel.purge(limit=amount)
            msg = await ctx.send("Cleared Messages")
            asyncio.sleep(10)
            await msg.delete()

    @commands.command(description="Change the channels slowmode.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int):
        try:
            if time == 0:
                em1 = nextcord.Embed(
                    title="Slowmode Success", description="Slowmode turned off"
                )
                await ctx.send(embed=em1)
                await ctx.channel.edit(slowmode_delay=0)
            elif time > 21600:
                em2 = nextcord.Embed(
                    title="Slowmode Error", description="Slowmode over 6 hours"
                )
                await ctx.send(embed=em2)
            else:
                await ctx.channel.edit(slowmode_delay=time)
                em3 = nextcord.Embed(
                    title="Slowmode Success",
                    description=f"Slowmode set to {time} seconds",
                )
                await ctx.send(embed=em3)
        except Exception:
            await ctx.send("Error has occoured, notifying dev team")
            print(Exception)

    @commands.command(
        aliases=["giverole", "addr"], description="Gives a member a certain role."
    )
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a user to give them a role!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a role to give {} that role!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Add Role Error",
                description="You do not have enough permissions to give this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            addRole = True
            for role_ in member.roles:
                if role_ == role:
                    addRole = False
                    break
            if not addRole:
                embed = nextcord.Embed(
                    title="Add Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Add Role Success",
                    description=f"{role.mention} has been assigned to {member.mention}",
                )
                await ctx.send(embed=em)
                await member.add_roles(role)
                return
        except Exception:
            print(Exception)

    @commands.command(
        aliases=["takerole", "remover"],
        description="Removes a certain role from a member.",
    )
    @commands.has_permissions(manage_roles=True)
    async def removerole(
        self,
        ctx,
        member: nextcord.Member = None,
        role: nextcord.Role = None,
        *,
        reason=None,
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a user to remove a role from them!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a role to remove the role from {}!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Remove Role Error",
                description="You do not have enough permissions to remove this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            roleRemoved = False
            for role_ in member.roles:
                if role_ == role:
                    await member.remove_roles(role)
                    roleRemoved = True
                    break
            if not roleRemoved:
                embed = nextcord.Embed(
                    title="Remove Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Remove Role Success!",
                    description=f"{role.mention} has been removed from {member.mention}",
                )
                await ctx.send(embed=em)
                return
        except Exception:
            print(Exception)

    @commands.command(description="Locks the channel.")
    @commands.has_permissions(kick_members=True)
    async def lock(self, ctx, channel: nextcord.TextChannel = None, setting = None):
        if setting == '--server':
            view = LockConfirm()
            em = nextcord.Embed(
                title="Are you sure?",
                description="This is a very risky command only to be used in important situations such as, `Raid on the Server`. **If this command is used for the wrong purpose you may risk getting demoted if not banned from the staff team.**",
            )
            await ctx.author.send(embed = em, view=view)
            await view.wait()
            if view.value is None:
                await ctx.author.send("Command has been Timed Out, please try again.")
            elif view.value:
                for channel in ctx.guild.channels:
                    await channel.set_permissions(
                        ctx.guild.default_role,
                        reason=f"{ctx.author.name} locked {channel.name} using --server override",
                        send_messages=False,
                    )
                embed = nextcord.Embed(
                title="Lockdown Success",
                description=f"Locked entire server ",
                )
                await ctx.send(embed=embed)
            else:
                lockEmbed = nextcord.Embed(
                    title="Lock Cancelled",
                    description="Lets pretend like this never happened them :I",
                )
                await ctx.author.send(embed=lockEmbed)
            return
        if channel is None:
            channel = ctx.message.channel
        await channel.set_permissions(
            ctx.guild.default_role,
            reason=f"{ctx.author.name} locked {channel.name}",
            send_messages=False, #
        )
        embed = nextcord.Embed(
            title="Lockdown Success",
            description=f"Locked {channel.mention} ",
        )
        await ctx.send(embed=embed)

    @commands.command(description="Unlocks the channel.")
    @commands.has_permissions(kick_members=True)
    async def unlock(self, ctx, channel: nextcord.TextChannel = None, setting=None):
        if setting == '--server':
            for channel in ctx.guild.channels:
                await channel.set_permissions(
                    ctx.guild.default_role,
                    reason=f"{ctx.author.name} unlocked {channel.name} using --server override",
                    send_messages=None,
                )
            embed = nextcord.Embed(
            title="Unlock Success",
            description=f"Unlocked entire server ",
            )
            await ctx.send(embed=embed)
            return
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(
            ctx.guild.default_role,
            reason=f"{ctx.author.name} unlocked {channel.name}",
            send_messages=True,
        )
        embed = nextcord.Embed(
            title="Unlock Success",
            description=f"Unlocked {channel.mention} ",
        )
        await ctx.send(embed=embed)

    @commands.command(description="Modbans the member.")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def modban(self, ctx, member, *, reason=None):
        if reason is None:
            reason = f"{ctx.author.name} modbanned {member.name}"
        else:
            reason = (
                f"{ctx.author.name} modbanned {member.name} for the reason of {reason}"
            )
        if member == None:
            embed1 = nextcord.Embed(
                title="Ban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="No banning yourself...",
            )
            return await ctx.send(embed=embed69)
        em = nextcord.Embed(
            title="Are you sure?",
            description="This is a very risky command only to be used in important situations such as, `NSFW or NSFLPosting` or `Raid on the Server`. Only use this command if no admin is online or responding. **If this command is used for the wrong purpose you may risk getting demoted if not banned from the staff team.**",
        )
        await ctx.author.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.author.send("Command has been Timed Out, please try again.")
        elif view.value:
            guild = ctx.guild
            banMsg = random.choice("BANNED")
            banEmbed = nextcord.Embed(
                title="Ban Success", description=f"{member.mention} {banMsg}"
            )
            banEmbed.add_field(name="Reason", value=reason)
            await ctx.author.send(embed=banEmbed)
            await member.ban(reason=reason)
            await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        else:
            banEmbed = nextcord.Embed(
                title="Ban Cancelled",
                description="Lets pretend like this never happened them :I",
            )
            await ctx.author.send(embed=banEmbed)
    

def setup(bot):
    bot.add_cog(Moderation(bot))