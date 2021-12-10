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

class AllConfirm(nextcord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=60)
        self.value = None
        self.ctx=ctx

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.green, custom_id="Confirm"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="Cancel")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()



class Emojis(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name="emojiadd",aliases=["addemo","emoadd","addem"], description="Adds an emoji to the server.")
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def addemoji(self, ctx, url: str, *, name):
        view=AllConfirm(ctx)
        embed=nextcord.Embed(title="Are you sure? ",color=nextcord.Color.dark_theme())
        message=await ctx.send(view=view,embed=embed)      
        await view.wait()
        await message.edit(view=view) 
        if view.value==True:
            for button in view.children:
                button.disabled = True
            await view.wait()
            await message.edit(view=view)
            guild = ctx.guild
            if ctx.author.guild_permissions.manage_emojis:
                async with aiohttp.ClientSession() as ses:
                    async with ses.get(url) as r:

                        try:
                            img_or_gif = BytesIO(await r.read())
                            b_value = img_or_gif.getvalue()
                            if r.status in range(200, 299):
                                emoji = await guild.create_custom_emoji(
                                    image=b_value, name=name
                                )
                                em = nextcord.Embed(
                                    title="Emoji Success",
                                    description=f"Successfully created emoji: <:{name}:{emoji.id}>",
                                )
                                await ctx.send(embed=em)
                                await ses.close()
                            else:
                                em = nextcord.Embed(
                                    title="Emoji Error",
                                    description=f"Error when making request | {r.status} response.",
                                )
                                await ctx.send(embed=em)
                                await ses.close()

                        except nextcord.HTTPException:
                            em = nextcord.Embed(
                                title="Emoji Error", description="File size is too big!"
                            )
                            await ctx.send(embed=em)
        else:

            embed=nextcord.Embed(title="Emoji Was Not Created",color=nextcord.Color.dark_theme())
            for button in view.children:
                button.disabled = True
            await view.wait()
            

    @commands.command(
        alisas=["remove"], description="Removes the specified emoji from the server."
    )
    async def emojiremove(self, ctx, emoji: nextcord.Emoji):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            em = nextcord.Embed(
                title="Emoji Success",
                description=f"Successfully deleted  {emoji}",
            )
            await ctx.send(embed=em)
            await emoji.delete()


    @commands.command(name="steal", description="Steals an emoji form a server")
    async def steal(self, ctx, emoji: nextcord.PartialEmoji, *, text=None):

        if ctx.author.guild_permissions.manage_emojis:

            if text == None:
                text = emoji.name
            else:
                text = text.replace(" ", "_")

            r = requests.get(emoji.url, allow_redirects=True)

            if emoji.animated == True:
                open("emoji.gif", "wb").write(r.content)
                with open("emoji.gif", "rb") as f:
                    z = await ctx.guild.create_custom_emoji(name=text, image=f.read())
                os.remove("emoji.gif")

            else:
                open("emoji.png", "wb").write(r.content)
                with open("emoji.png", "rb") as f:
                    z = await ctx.guild.create_custom_emoji(name=text, image=f.read())
                os.remove("emoji.png")

            embed = nextcord.Embed(
                title="Success",
                description=f"Succesfully Cloned {z}",
                color=nextcord.Color.green(),
            )
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Emojis(bot))
