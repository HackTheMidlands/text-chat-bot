import logging
import discord
from discord.ext import commands

from ..util import config
from ..util import data
from ..util.log import fatal_error
from . import lookup
from . import names
from . import crud


logger = logging.getLogger('text-chat-bot')
command_prefix=config.config['discord']['command_prefix']
bot = commands.Bot(command_prefix=command_prefix, case_insensitive=True)


def start():
    global bot
    logger.info("Starting bot...")
    bot.run(config.config['discord']['token'])


async def delete_all(guild):
    ids = list(data.mapping.keys()).copy()
    for user_id in ids:
        user = guild.get_member(int(user_id))
        logger.info(user)
        await crud.delete(user, guild)


@bot.event
async def on_error(event_method, *args, **kwargs):
    logger.error(f'{event_method}, {args}, {kwargs}')

@bot.event
async def on_ready():
    global guild, target_catagory
    server_id = config.config['discord']['server_id']
    try:
        guild = bot.get_guild(int(server_id))
        assert guild is not None
        logger.info(f"Logged into {guild}")
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
    await crud.create(bot, ctx.author, ctx.guild)

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def delete(ctx):
    user = ctx.author
    text_id = data.get_channel_id(user, 'text')
    if text_id is None:
        await user.send(f"You're not setup!")
        return
    await crud.delete(user, ctx.guild)

@bot.command()
async def add(ctx):
    text_channel = ctx.guild.get_channel(data.get_channel_id(ctx.author, 'text'))
    voice_channel = ctx.guild.get_channel(data.get_channel_id(ctx.author, 'voice'))

    if text_channel is None:
        await create(ctx)
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
        if user in text_channel.members:
            await ctx.author.send(f"'{user.display_name}' is already in your channel.")
            return

        await add_to_channel(user=user, channel=text_channel, channel_type='text')
        await add_to_channel(user=user, channel=voice_channel, channel_type='voice')
        await user.send(f"You have been added to {ctx.author.display_name}'s channel.")

        message = config.config['messages']['user_added']
        message = message.replace('USER', user.mention)
        await user.send(message.replace('OWNER', ctx.author.display_name))


@bot.group(name='rename')
async def rename(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f'Invalid rename command passed...\nTry `{command_prefix[0]}rename text` or `{command_prefix[0]}rename voice`!')

@rename.command(name='voice')
async def rename_voice(ctx, *, name):
    voice_channel = ctx.guild.get_channel(data.get_channel_id(ctx.author, 'voice'))
    if voice_channel is None:
        await create(ctx)
    try:
        await voice_channel.edit(name=name)
    except Exception as e:
        logger.warning(e)
        await ctx.send('oopsies! someone who can deal with it gets to see an error now!')

@rename.command(name='text')
async def rename_text(ctx, *, name):
    text_channel = ctx.guild.get_channel(data.get_channel_id(ctx.author, 'text'))
    if text_channel is None:
        await create(ctx)
    try:
        await text_channel.edit(name=name)
    except Exception as e:
        logger.warning(e)
        await ctx.send('oopsies! someone who can deal with it gets to see an error now!')


@bot.command()
async def remove(ctx):
    text_channel = ctx.guild.get_channel(data.get_channel_id(ctx.author, 'text'))
    voice_channel = ctx.guild.get_channel(data.get_channel_id(ctx.author, 'voice'))

    if text_channel is None:
        await ctx.author.send(f'You do not yet have a channel.')
        return

    if ctx.message.mention_everyone:
        await ctx.author.send(f'You cannot use `@everyone` or `@here` to remove people.')
        return

    for user in ctx.message.mentions:
        if user not in text_channel.members:
            await ctx.author.send(f"'{user.display_name}' is not in your group, so cannot be removed.")
            return

        if user == ctx.author:
            await ctx.author.send(f'You cannot remove yourself from your own group.')
            return
        await remove_from_channel(user=user, channel=text_channel)
        await remove_from_channel(user=user, channel=voice_channel)


async def add_to_channel(user, channel, channel_type):
    if channel_type == 'text':
        await channel.set_permissions(user, read_messages=True)
    elif channel_type == 'voice':
        overwrite = discord.PermissionOverwrite()
        await channel.set_permissions(user, view_channel=True, connect=True, speak=True)

async def remove_from_channel(user, channel):
    await channel.set_permissions(user, overwrite=None)
