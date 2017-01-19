import discord

from cogs.utils import checks
from discord.ext import commands

class Config:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def countservers(self):
        """
        Checks how many servers the bot is on"""
        msg = "The bot is in **"
        msg += str(len(self.bot.servers))
        msg += "** servers."
        await self.bot.say(msg)

    @commands.command()
    @checks.is_owner()
    async def shout(self, server_id, *, message):
        """
        Shouts a message to the main channel of a certain server"""
        msg = "```asciidoc\n"
        msg += "Announcement :: Information\n"
        msg += message
        msg += "\n```"
        for server in self.bot.servers:
            if server.id == server_id:
                try:
                    await self.bot.send_message(server, msg)
                    await self.bot.say("'" + message + "'" + " has been send to " + server.name + ".")
                except discord.errors.Forbidden:
                    await self.bot.say("I'm not allowed to do that.")


    @commands.command()
    @checks.is_owner()
    async def listservers(self):
        """
        Checks what servers the bot is on"""
        servers = self.bot.servers
        await self.bot.say("```asciidoc\nThe bot is in the following {} server(s):\n```".format(str(len(self.bot.servers))))
        msg = "```asciidoc\n"
        msg2 = "```asciidoc\n"
        msg3 = "```asciidoc\n"
        msg4 = "```asciidoc\n"
        #msg += "\n"

        messages = [msg, msg2, msg3, msg4]
        count = 0
        for server in servers:
            if len(server.members)<10:
                messages[count] += "{:<1} :: 000{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members)<100:
                messages[count] += "{:<1} :: 00{} users :: {}".format(server.id, len(server.members), server.name)
            elif len(server.members)<1000:
                messages[count] += "{:<1} :: 0{} users :: {}".format(server.id, len(server.members), server.name)
            else:
                messages[count] += "{:<1} :: {} users :: {}".format(server.id, len(server.members), server.name)
            messages[count] += "\n"
            if len(messages[count])>1500:
                count = count+1

        for message in messages:
            if len(message) > 30:
                await self.bot.say(message + "\n```")


    @commands.command(pass_context = True)
    @checks.is_owner()
    async def discrim(self, ctx, discriminator):
        """
        Find users with this discriminator"""
        msg = "Users with discriminator " + discriminator
        msg += ": \n"
        for r in self.bot.get_all_members():
            if r.discriminator == discriminator:
                if r.name in msg:
                    pass
                else:
                    msg += "```\n"
                    msg += r.name
                    msg += "\n```"
        await self.bot.say(msg)


    @commands.command()
    async def countusers(self):
        """
        Checks how many users the bot is connected to"""
        msg = "The bot is connected to **"
        msg += str(len(set(self.bot.get_all_members())))
        msg += "** users."
        await self.bot.say(msg)

    @commands.command()
    @checks.is_owner()
    async def notify(self, *, content):
        """Notifies every server"""
        if content == "shutdown":
            msg = "```asciidoc\n"
            msg += "Announcement :: Shutdown\n"
            msg += "riceBot shutting down... Will be up again soon!"
            msg += "\n```"
        elif content == "info":
            msg = "```asciidoc\n"
            msg += "Announcement :: Information\n"
            msg += "= -=-=-=-=-=-=-=-=-=-=-=- =\n"
            msg += "Thank you for inviting riceBot!\n"
            msg += "For basic information on the bot, a list of commands, or to contact the owner, use: \n"
            msg += "= rice.rice =\n"
            msg += "= rice.help =\n"
            msg += "= rice.contact =\n"
            msg += "To add the bot to your own server, open this:: https://discordsites.com/ricebot/\n"
            msg += "= -=-=-=-=-=-=-=-=-=-=-=- =\n"
            msg += "riceBot ~ managed by FwiedWice"
            msg += "\n```"
        else:
            msg = "```asciidoc\n"
            msg += "Announcement :: Information\n"
            msg += content
            msg += "\n```"
        for server in self.bot.servers:
            try:
                await self.bot.send_message(server, msg)
            except discord.errors.Forbidden:
                pass
        await self.bot.say("Message succesfully sent")


    @commands.command()
    @checks.is_owner()

    async def speak(self, *, content):

        """Says something"""
        await self.bot.say(content)

def setup(bot):
    bot.add_cog(Config(bot))
