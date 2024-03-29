import time
import nextcord
import os
import random
from nextcord.ext.commands import bot
import psutil 
from datetime import datetime
from nextcord import user
from nextcord.ext import commands
from itertools import starmap
from nextcord.ext import menus
from nextcord.ext import commands, tasks
import aiohttp
from io import BytesIO
import requests
from nextcord import ButtonStyle
from nextcord.ui import button, View, Button
from datetime import datetime
from itertools import chain
def get_command_signature(self, command):
    return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)
    def get_command_brief(self, command):
        return " "
    async def send_bot_help(self, mapping):
        all_commands = list(chain.from_iterable(mapping.values()))
        formatter = HelpPageSource(all_commands, self)
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)

    async def send_command_help(self, command):
        embed = nextcord.Embed(color=0x42cbf5)
        embed.add_field(name="Command Description:", value=f"{command.help}")
        embed.add_field(name="Syntax:", value=f"```{self.get_command_signature(command)}```",inline=False)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        else:
            embed.add_field(name="Aliases", value="No Aliases", inline=False)  

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)
    

class HelpPageSource(menus.ListPageSource):
    def __init__(self, data, helpcommand):
        super().__init__(data, per_page=6)
        self.helpcommand = helpcommand
    def format_command_help(self, no, command):
        signature = self.helpcommand.get_command_signature(command)
        docs = self.helpcommand.get_command_brief(command)
        return f"{no}. {signature}\n{docs}"
    
    async def format_page(self,menu, entries):
        page = menu.current_page
        max_page = self.get_max_pages()
        starting_number = page * self.per_page + 1
        iterator = starmap(self.format_command_help, enumerate(entries, start=starting_number))
        page_content = "\n".join(iterator)
        embed = nextcord.Embed(
                title=f"**All Commands**", 
                description=page_content,
                color=0x42cbf5
            )
        embed.set_footer(text=f"Use [prefix] help [command] for more info on a command ! ")
        return embed    
class MyMenuPages(nextcord.ui.View, menus.MenuPages):
    def __init__(self, source, *, delete_message_after=False):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None
        self.delete_message_after = delete_message_after

    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author

    @nextcord.ui.button(emoji='⏮️', style=nextcord.ButtonStyle.green)
    async def first_page(self, button, interaction):
        await self.show_page(0)

    @nextcord.ui.button(emoji='◀️', style=nextcord.ButtonStyle.green)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)

    @nextcord.ui.button(emoji='⏹️', style=nextcord.ButtonStyle.red)
    async def stop_page(self, button, interaction):
        self.stop()
        if self.delete_message_after:
            await self.message.delete(delay=0)

    @nextcord.ui.button(emoji='▶', style=nextcord.ButtonStyle.green)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)

    @nextcord.ui.button(emoji='⏭️', style=nextcord.ButtonStyle.green)
    async def last_page(self, button, interaction):
        await self.show_page(self._source.get_max_pages() - 1)            
class HelpCog(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
       help_command = MyHelp()
       help_command.cog = self 
       bot.help_command = help_command
       
def setup(bot):
    bot.add_cog(HelpCog(bot))        