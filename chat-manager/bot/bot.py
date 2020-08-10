import logging
import discord
from discord.ext import commands

from ..util import config
from ..util import data
from ..util.log import fatal_error
from . import lookup
from . import names


logger = logging.getLogger('text-chat-bot')
command_prefix=config.config['discord']['command_prefix']
bot = commands.Bot(command_prefix=command_prefix)


def start():
    global bot
    logger.info("Starting bot...")
    bot.run(config.config['discord']['token'])


@bot.event
async def on_ready():
    global guild, target_catagory
    server_id = config.config['discord']['server_id']
    try:
        guild = bot.get_guild(int(server_id))
        assert guild is not None
    except:
        fatal_error(f'Cannot find server id \'{server_id}\'')

    target_catagory_id = config.config['discord']['target_catagory']
    try:
        target_catagory = bot.get_channel(int(target_catagory_id))
        assert target_catagory is not None
    except:
        fatal_error(f'Cannot catagory \'{target_catagory_id}\'')

    logger.info("Bot online")


@bot.command()
async def create(ctx):
    guild = ctx.guild
    role_id = data.get_channel_id(ctx.author, 'role')
    if role_id is not None:
        await ctx.author.send(f"You're already setup!")
    user_role = await guild.create_role(name=f"{ctx.author}'s Space!")
    data.associate_channel(ctx.author, user_role, 'role')
    await ctx.author.add_roles(user_role)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, create_instant_invite=False, speak=False),  # everyone
        guild.me:           discord.PermissionOverwrite(read_messages=True),  # the bot
        user_role:          discord.PermissionOverwrite(read_messages=True, speak=True, connect=True) # the users 'group'
    }

    name = names.gen_name()
    topic = f'{ctx.author}\'s private channel'
    text_channel = await target_catagory.create_text_channel(name, topic=topic, overwrites=overwrites)
    voice_channel = await target_catagory.create_voice_channel(name, topic=topic, overwrites=overwrites)

    data.associate_channel(ctx.author, channel=text_channel, channel_type='text')
    data.associate_channel(ctx.author, channel=voice_channel, channel_type='voice')

    message = config.config['messages']['channel_start']
    await text_channel.send(message.replace('OWNER', ctx.message.author.mention))


@bot.command()
async def add(ctx):
    private_role = ctx.guild.get_role(data.get_channel_id(ctx.author, 'role'))

    if private_role is None:
        await ctx.author.send(f'You do not yet have a role.')
        return

    if ctx.message.mention_everyone:
        await ctx.author.send(f'You cannot use `@everyone` or `@here` to invite people.')
        return

    for user in ctx.message.mentions:
        logger.warning(user)
        if user.bot:
            await ctx.author.send(f'You cannot add bots to your channel.')
            return
        if user in private_role.members:
            await ctx.author.send(f"'{user.display_name}' is already in your channel.")
            return

        await user.add_roles(private_role)
        await user.send(f"You have been added to {ctx.author.display_name}'s channel.")

        message = config.config['messages']['user_added']
        message = message.replace('USER', user.mention)
        await user.send(message.replace('OWNER', ctx.author.display_name))


@bot.command()
async def remove(ctx):
    private_role = ctx.guild.get_role(data.get_channel_id(ctx.author, 'role'))

    if private_role is None:
        await ctx.author.send(f'You do not yet have a role.')
        return

    if ctx.message.mention_everyone:
        await ctx.author.send(f'You cannot use `@everyone` or `@here` to remove people.')
        return

    voice_channel = lookup.get_channel_by_id(data.get_channel_id(ctx.author, 'voice'), ctx.guild)
    for user in ctx.message.mentions:
        if user not in private_role.members:
            await ctx.author.send(f"'{user.display_name}' is not in your group, so cannot be removed.")
            return

        if user == ctx.author:
            await ctx.author.send(f'You cannot remove yourself from your own group.')
            return
        
        await user.remove_roles(private_role)
        await user.send(f"You have been removed from {ctx.author.display_name}'s group.")


async def add_to_channel(user, channel, channel_type):
    if channel_type == 'text':
        await channel.set_permissions(user, read_messages=True)
    elif channel_type == 'voice':
        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel
        await channel.set_permissions(user, connect=True, speak=True)

async def remove_from_channel(user, channel):
    await channel.set_permissions(user, read_messages=False)
