import asyncio
import os

import discord
from discord.ext import commands
from discord.ext.commands import is_owner, Context

from lib.MechaByte import MechaByte
from lib.key_store import KeyValueStore

# Load API keys
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the key-value store
store = KeyValueStore('store.pkl')

# Set up Discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents, application_id=1098609791917629441)
asyncio.run(bot.add_cog(MechaByte(store)))


@bot.command(name='sync', help='Sync commands with Discord. (Owner only)')
@is_owner()
async def sync(ctx: Context) -> None:
    synced = await bot.tree.sync()
    await ctx.reply("{} commands synced".format(len(synced)))

# Start the bot
bot.run(DISCORD_TOKEN)

