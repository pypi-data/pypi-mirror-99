import discord
from discord.ext import commands

from . import utils


class MiscCommands(utils.Cog):

    @commands.command(aliases=['support', 'guild'], cls=utils.Command, add_slash_command=False)
    @utils.checks.is_config_set('command_data', 'guild_invite')
    @commands.bot_has_permissions(send_messages=True)
    async def server(self, ctx:utils.Context):
        """
        Gives the invite to the support server.
        """

        await ctx.send(f"<{self.bot.config['command_data']['guild_invite']}>", embeddify=False)

    @commands.command(aliases=['patreon'], cls=utils.Command, add_slash_command=False)
    @utils.checks.is_config_set('command_data', 'donate_link')
    @commands.bot_has_permissions(send_messages=True)
    async def donate(self, ctx:utils.Context):
        """
        Gives you the bot's creator's donate link.
        """

        await ctx.send(f"<{self.bot.config['command_data']['donate_link']}>", embeddify=False)

    @commands.command(cls=utils.Command, add_slash_command=False)
    @commands.bot_has_permissions(send_messages=True)
    @utils.checks.is_config_set('command_data', 'website_link')
    async def website(self, ctx:utils.Context):
        """
        Gives you a link to the bot's website.
        """

        await ctx.send(f"<{self.bot.config['command_data']['website_link']}>", embeddify=False)

    @commands.command(cls=utils.Command, aliases=['information'], add_slash_command=False)
    @commands.bot_has_permissions(send_messages=True)
    @utils.checks.is_config_set('command_data', 'info')
    async def info(self, ctx:utils.Context):
        """
        Gives you information on how to use the bot and what the bot is about.
        """

        await ctx.send(f"<{self.bot.config['command_data']['info']}>")

    @commands.command(cls=utils.Command, hidden=True, add_slash_command=False)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    @utils.checks.is_config_set('command_data', 'echo_command_enabled')
    async def echo(self, ctx:utils.Context, *, content:str):
        """
        Echos the given content into the channel.
        """

        await ctx.send(content, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False), embeddify=False)


def setup(bot:utils.Bot):
    x = MiscCommands(bot)
    bot.add_cog(x)
