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
        names[message.author] = None
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
            shuffler(names)
            await client.wait_for('message', check=check)
        except:
            await message.channel.send("Not enough people to shuffle! (3 people needed)")

def shuffler(names):
    if len(names) < 3:
        raise Exception("Not enough people")
    givers = names.keys()
    receivers = names.keys()
    final_list = {}
    while any(i == j for i, j in zip(givers, receivers)):
        random.shuffle(givers)
    for giver, receiver in zip(givers, receivers):
        final_list[giver] = receiver
    print(final_list)
    for giver, receiver in names.items():
        giver.send(f"Your santa is {receiver.name}")

client.run("")  # token goes here