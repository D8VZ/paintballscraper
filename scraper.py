import json
import discord as discord
from discord import Embed
from discord.ext import commands
import asyncio
import aiohttp
import os
client = commands.Bot(command_prefix='!',allowed_mentions = discord.AllowedMentions(everyone = True))
client.remove_command('help')
TOKEN = os.environ.get('TOKEN')

async def check_availability():
    await client.wait_until_ready()
    channel = client.get_channel(853326235563589694)
    products_json_url = "https://hormesispaintball.com/products.json?limit=10000"

    while not client.is_closed():
        print("checking")
        async with aiohttp.ClientSession() as session:
            async with session.get(products_json_url) as search:
                if search.status == 200:
                    json_data = await search.json()
                    for x in json_data['products']:
                        for variant in x['variants']:
                            if variant['available'] is True:
                                with open("blocks.json") as blocks:
                                    blocked_names = json.load(blocks)
                                if x['handle'] not in blocked_names:
                                    embed = Embed(title='New Availability',
                                                  url=f'https://hormesispaintball.com/products/{x["handle"]}')
                                    embed.add_field(name='Item',value=x['handle'])
                                    embed.add_field(name='updated at', value=x['updated_at'])
                                    await channel.send(embed=embed)
                                    await channel.send('@everyone')
                                    await asyncio.sleep(1)
        await asyncio.sleep(30)

client.loop.create_task(check_availability())
@client.command()
async def help(ctx):
    embed = Embed(title='Help')
    embed.add_field(name='!help',value='Brings up this page')
    embed.add_field(name='!status', value='status of bot')
    embed.add_field(name='!block_product', value='Used to block testing pages, and other non useful product pages on the site')
    embed.add_field(name='!remove_block', value='Removes blocks, see !list for current blocks')
    embed.add_field(name='!list', value='lists blocked products')
    await ctx.send(embed=embed)

@client.command()
async def status(ctx):
    await ctx.send(embed=Embed(title='UP!'))

@client.command()
async def block_product(ctx, name:str):
    try:
        with open('blocks.json','r+') as json_file:
            data = json.load(json_file)
            data.append(name)
            json_file.truncate(0)
            json_file.seek(0)
            json.dump(data, json_file)


    except Exception as e:
        print(e)
        with open("blocks.json",'w') as file:
            data = [name]
            json.dump(data,file)



@client.command()
async def remove_block(ctx,name):
    with open("blocks.json", 'r+') as file:
        data = json.load(file)
        if name in data:
            data.remove(name)
            file.truncate(0)
            file.seek(0)
            json.dump(data, file)
            await ctx.send(f"removed {name}")

        else:
            await ctx.send("Not blocked")



@client.command()
async def list(ctx):
    try:
        with open("blocks.json", 'r+') as file:
            data = json.load(file)
            await ctx.send(data)
    except Exception:
        await ctx.send("No Blocks")


client.run(TOKEN)