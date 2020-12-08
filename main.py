import config
import discord
import discord.utils
from discord.utils import get
import time
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

client = discord.Client(intents=intents)

def remove(mymesage): 
    mymesage = mymesage.replace(" ", "")
    mymesage = mymesage.replace("!create", "")
    mymesage = mymesage.replace("!end", "")
    mymesage = mymesage.split(",")
    return mymesage


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    game = discord.Game("all alone")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    print("got message")
    if message.channel.id == config.createchannel:
        if message.content.startswith("!create"):
            msg = message.content
            db = remove(str(msg))
            print(str(db))
            game = discord.Game("the waiting game")
            await client.change_presence(status=discord.Status.online, activity=game)

            channel = client.get_channel(config.announcechannel)

            async for message in channel.history(limit=1):
                await message.add_reaction('✅')
                global messageid
                messageid = message.id
                
                timeout = int(db[0])   # [seconds]

                timeout_start = time.time()

                while time.time() < timeout_start + timeout:
                    role = get(message.guild.roles, id=config.role)
                    def check(reaction, user):
                        return str(reaction.emoji) == '✅' and reaction.message.id == messageid
                    try:
                        reaction, user = await client.wait_for('reaction_add', check=check, timeout=1)
                    except:
                        pass
                    else:
                        await user.add_roles(role)

            game = discord.Game("a game with you all!")
            await client.change_presence(status=discord.Status.online, activity=game)

        elif message.content.startswith("!end"):
            game = discord.Game("all alone")
            await client.change_presence(status=discord.Status.idle, activity=game)
            role = get(message.guild.roles, id=config.role)
            for m in role.members:
                await m.remove_roles(role)
                await asyncio.sleep(len(role.members)**(1/4))
            i = len(config.eventchannels)
            print(str(i))
            while i-1 >= 0:
                channel = client.get_channel(config.eventchannels[i-1])
                await channel.send("------------------------------------------------------------------------------------------")
                i -= 1
                


client.run(config.token)