import nextcord
from nextcord.ext import commands
import zlib
import io
import re
import aiohttp
from nextcord.ext.commands import bot
class ProgrammingCog(commands.Cog, name = "Programming"):
    """Commands for programmers"""

    def __init__(self, bot):
        self.bot = bot
        self.bot = bot
        self.bot.session = aiohttp.botSession(loop=self.bot.loop)
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
        
from nextcord.ext import commands
import zlib
import io
import re
import aiohttp
class ProgrammingCog(commands.Cog, name = "Programming"):
    """Commands for programmers"""

    def __init__(self, bot):
        self.bot = bot
        self.bot = bot
        self.bot.session = aiohttp.botSession(loop=self.bot.loop)
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
        
    @property
    def session(self):
        return self.bot.http._HTTPbot__session

    async def _run_code(self, *, lang: str, code: str):
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code})
        return await res.json()

    @commands.command()
    async def run(self, ctx: commands.Context, *, codeblock: str):
        """
        Run code and get results instantly
        **Note**: You must use codeblocks around the code
        Supported languages: awk, bash, brainfuck, c, cpp, crystal, csharp, d, dash, deno, elixer, emacs, go, haskell, java, jelly, julia, kotlin, lisp, lua, nasm, nasm64, nim, node, osabie, paradoc, perl, php, prolog, python2, python, ruby, rust, scala, swift, typescript, zig
        """
        matches = self.regex.findall(codeblock)
        if not matches:
            return await ctx.reply(embed=nextcord.Embed(title="Uh-oh", description="Couldn't quite see your codeblock"))
        lang = matches[0][0] or matches[0][1]
        if not lang:
            return await ctx.reply(embed=nextcord.Embed(title="Uh-oh", description="Couldn't find the language hinted in the codeblock or before it"))
        code = matches[0][2]
        result = await self._run_code(lang=lang, code=code)

        await self._send_result(ctx, result)

    @commands.command()
    async def runl(self, ctx:commands.Context, lang:str, *, code:str):
        """
        Run a single line of code, **must** specify language as first argument
        Supported languages: awk, bash, brainfuck, c, cpp, crystal, csharp, d, dash, deno, elixer, emacs, go, haskell, java, jelly, julia, kotlin, lisp, lua, nasm, nasm64, nim, node, osabie, paradoc, perl, php, prolog, python2, python, ruby, rust, scala, swift, typescript, zig
        """
        result = await self._run_code(lang=lang, code=code)
        await self._send_result(ctx, result)

    async def _send_result(self, ctx:commands.Context, result:dict):
        if "message" in result:
            return await ctx.reply(embed=nextcord.Embed(title="Uh-oh", description=result["message"], color=Color.red()))
        output = result['output']
#        if len(output) > 2000:
#            url = await create_guest_paste_bin(self.session, output)
#            return await ctx.reply("Your output was too long, so here's the pastebin link " + url)
        embed = nextcord.Embed(
            title=f"{result['language'][0].upper() + result['language'][1:]}")
        newline = '\n'
        rep = {"python3": "py", "python2": "py", 'node': 'js'}
        rep = dict((re.escape(k), v) for k, v in rep.items()) 
        pattern = re.compile("|".join(rep.keys()))
        converted_language = pattern.sub(lambda m: rep[re.escape(m.group(0))], result['language'])
        limit = 1024 - (29 + len(converted_language))
        output = f"```{converted_language}\n{output[:limit]}```{(len(output)>limit) * (newline + '**Output shortened**')}"
        embed.add_field(name="Output", value=output or "**No output**")
        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.reply(output)

def setup(bot):
    bot.add_cog(ProgrammingCog(bot))