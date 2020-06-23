import discord

def get_user_by_name(name, guild):
    return discord.utils.get(guild.members, name=name)

def get_user_by_id(id, guild):
    return discord.utils.get(guild.members, id=id)

def get_channel_by_id(id, guild):
    return discord.utils.get(guild.channels, id=id)
