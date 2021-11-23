import discord

client = discord.Client()

names = {}
newline = '\n'
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


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

client.run("")  # token goes here
