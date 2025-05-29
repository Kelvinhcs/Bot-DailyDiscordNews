from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

#loading token from .env
load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

#setting the default permissions and the prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

#url and soup section
g1Url = requests.get(url="https://g1.globo.com")
soupG1 = BeautifulSoup(g1Url.content, 'html5lib')


@bot.event
async def on_ready():
    print(f'Iniciado e logado como: {bot.user}')


@bot.command()
async def news(ctx):
    await ctx.reply('Carregando notícias...')
    newsMessage = '📰-=-=-=-=-=-=-=-=-=-=- **Notícias do G1** -=-=-=-=-=-=-=-=-=-=-📰\n\n'
    noticias = soupG1.find_all(attrs={"elementtiming": "text-ssr"})

    for contador, item in enumerate(noticias, start=1):
        link = item.find_parent('a')
        if link and link.get('href'):
            newsMessage += (
                f'{contador} - **{item.get_text(strip=True)}**\n'
                f'Link: <{link["href"]}>\n\n'
            )
    if len(newsMessage) <= 200:
        await ctx.send(newsMessage)
    else:
        parts = [newsMessage[i:i + 2000] for i in range(0, len(newsMessage), 2000)]
        for part in parts:
            await ctx.send(part)



bot.run(token)