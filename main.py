import discord
import random

client = discord.Client()

newline = '\n'
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

names = {}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$add'):
        names[message.author] = {"address": None, "receiver": None}
        channel = message.channel
        await channel.send('Please enter an address to mail to')

        def check(m):
            return m.channel == channel
        address = await client.wait_for('message', check=check, timeout=30.0)
        names[message.author]['address'] = address.content
        await message.channel.send(f"Added {message.author.name}. \n Current list: \n {newline.join(i.name for i in names.keys())}")

    if message.content.startswith('$remove'):
        names.pop(message.author)
        await message.channel.send(f"Removed {message.author.name}. \n Current list: \n {newline.join(i.name for i in names.keys())}")

    if message.content.startswith('$list'):
        await message.channel.send(f"Current list: \n {newline.join(i.name for i in names.keys())}")
    if message.content.startswith('$shuffle'):
        channel = message.channel
        await channel.send('Are you sure you want to send out secret santa DMs? Y/N')

        def check(m):
            return m.content == 'y' and m.channel == channel
        await client.wait_for('message', check=check, timeout=30.0)
        try:
            final_dict = shuffler(names)
            for giver, receiver in final_dict.items():
                receiver = receiver['receiver']
                address = final_dict[receiver]["address"]
                await giver.send(f"You are giving a gift to {receiver.name}. Their address is {address}")
        except:
            await message.channel.send("Not enough people to shuffle! (3 people needed)")


def shuffler(names):
    if len(names) < 3:
        raise Exception("Not enough people")
    givers = list(names.keys())
    receivers = list(names.keys())
    final_dict = {}
    while any(i == j for i, j in zip(givers, receivers)):
        random.shuffle(givers)
    for giver, receiver in zip(givers, receivers):
        final_dict[giver] = {"address": names[giver]['address'], "receiver": receiver}
    return final_dict


client.run("")  # token goes here