import logging
import discord
from discord.ext import commands

from ..util import config
from ..util import data
from ..util.log import fatal_error
from . import lookup
from . import names

logger = logging.getLogger('text-chat-bot')
bot = commands.Bot(command_prefix=config.config['discord']['command_prefix'])

def start():
    global bot
    logger.info("Starting bot...")
    bot.run(config.config['discord']['token'])
    # bot.loop.create_task(get_ch())

# async def get_ch():
#     await bot.wait_until_ready()
#     logger.info("Getting data...")

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
    if data.get_channel_id(ctx.author) is not None:
        logger.debug(f'User \'{ctx.author}\' already has a channel')
        await ctx.author.send(f'You already have a channel.')
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, create_instant_invite=False), # everyone
        guild.me: discord.PermissionOverwrite(read_messages=True), # the bot
    }

    name = names.gen_name()
    topic = f'{ctx.author}\'s private channel'
    channel = await target_catagory.create_text_channel(name, topic=topic, overwrites=overwrites)

    data.associate_channel(ctx.author, channel)
    await add_to_channel(ctx.author, channel)

    message = config.config['messages']['channel_start']
    await channel.send(message.replace('OWNER', ctx.message.author.mention))

@bot.command()
async def add(ctx):
    private_channel = lookup.get_channel_by_id(data.get_channel_id(ctx.author), target_catagory)

    if private_channel is None:
        await ctx.author.send(f'You do not yet have a channel.')
        return

    if ctx.message.mention_everyone:
        await ctx.author.send(f'You cannot use `@everyone` or `@here` to invite people.')
        return

    for user in ctx.message.mentions:
        if user.bot:
            await ctx.author.send(f'You cannot add bots to your channel.')
            return
        if user in private_channel.members:
            await ctx.author.send(f'\'{user.display_name}\' is already in your channel.')
            return

        await add_to_channel(user, private_channel)
        await user.send(f'You have been added to {ctx.author.display_name}\'s channel.')

        message = config.config['messages']['user_added']
        message = message.replace('USER', user.mention)
        await private_channel.send(message.replace('OWNER', ctx.author.display_name))

@bot.command()
async def remove(ctx):
    private_channel = lookup.get_channel_by_id(data.get_channel_id(ctx.author), target_catagory)

    if private_channel is None:
        await ctx.author.send(f'You do not yet have a channel.')
        return

    if ctx.message.mention_everyone:
        await ctx.author.send(f'You cannot use `@everyone` or `@here` to remove people.')
        return

    for user in ctx.message.mentions:
        if user not in private_channel.members:
            await ctx.author.send(f'\'{user.display_name}\' is not in your channel, so cannot be removed.')
            return

        if user == ctx.author:
            await ctx.author.send(f'You cannot remove yourself from your own channel.')
            return

        if user.permissions_in(private_channel).administrator:
            await ctx.author.send(f'You cannot remove admins.')
            return

        await remove_from_channel(user, private_channel)
        await user.send(f'You have been removed from {ctx.author.display_name}\'s channel.')


async def add_to_channel(user, channel):
    await channel.set_permissions(user, read_messages=True)

async def remove_from_channel(user, channel):
    await channel.set_permissions(user, read_messages=False)
