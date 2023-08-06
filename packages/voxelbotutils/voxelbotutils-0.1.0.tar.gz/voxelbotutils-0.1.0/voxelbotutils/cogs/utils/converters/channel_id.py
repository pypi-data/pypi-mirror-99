import re

from discord.ext import commands


class ChannelID(int):
    """
    A conveter that takes the given value and tries to grab the ID from it.
    When used, this would provide the ID of the channel.
    """

    @classmethod
    async def convert(cls, ctx:commands.Context, value:str) -> int:
        """
        Converts the given value to a valid channel ID.
        """

        match = commands.IDConverter()._get_id_match(value) or re.match(r'<#([0-9]+)>$', value)
        if match is not None:
            return int(match.group(1))
        raise commands.UserNotFound(value)
