import logging
import discord
from ..util import config
from ..util import data

logger = logging.getLogger('text-chat-bot')

async def create(bot, user, guild):
    member_role = guild.get_role(int(config.config['discord']['member_role_id']))
    logger.info(member_role)
    text_id = data.get_channel_id(user, 'text')
    if text_id is not None:
        await user.send(f"You're already setup!")
        return
    user_category = bot.get_channel(int(config.config['discord']['target_catagory']))
    logger.info(user_category)
    # user_category = await guild.create_category(name=f"{user}'s Space!")
    # data.associate_channel(user, user_category, 'group')
    # await user.add_roles(user_category)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, create_instant_invite=False, speak=False),  # everyone
        guild.me:           discord.PermissionOverwrite(read_messages=True),  # the bot
        member_role: discord.PermissionOverwrite(read_messages=False, create_instant_invite=False, connect=False),
        user:          discord.PermissionOverwrite(read_messages=True, speak=True, connect=True) # the users 'group'
    }

    voice_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, create_instant_invite=False, speak=False),  # everyone
        guild.me:           discord.PermissionOverwrite(read_messages=True),  # the bot
        member_role: discord.PermissionOverwrite(view_channel=True, create_instant_invite=False, connect=False),
        user:          discord.PermissionOverwrite(read_messages=True, speak=True, connect=True) # the users 'group'
    }
    

    # name = names.gen_name()
    topic = f'{user}\'s private channel'
    logger.info(topic)
    voice_channel = await user_category.create_voice_channel(f"{user} 🗣", topic=topic, overwrites=voice_overwrites)
    # voice_channel.edit(sync_permissions=True)
    text_channel = await user_category.create_text_channel(f"{user} 💬", topic=topic, overwrites=overwrites)
    # text_channel.edit(sync_permissions=True)

    data.associate_channel(user, channel=text_channel, channel_type='text')
    data.associate_channel(user, channel=voice_channel, channel_type='voice')

    message = config.config['messages']['channel_start']
    await text_channel.send(message.replace('OWNER', user.mention))

async def delete(user, guild):
    await guild.get_channel(data.get_channel_id(user, 'text')).delete()
    await guild.get_channel(data.get_channel_id(user, 'voice')).delete()
    data.delete_user(user)