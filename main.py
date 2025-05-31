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



@bot.event
async def on_ready():
    print(f'Iniciado e logado como: {bot.user}')


@bot.command()
async def news(ctx):

    #url and soup section
    g1Url = requests.get(url="https://g1.globo.com")
    soupG1 = BeautifulSoup(g1Url.content, 'html5lib')
    valorUrl = requests.get(url="https://valor.globo.com/")
    soupValor = BeautifulSoup(valorUrl.content, 'html5lib')


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


@bot.command()
async def valor(ctx):
    color_hex = "#016667"
    discord_color = int(color_hex[1:], 16)
    embed = discord.Embed(title="Valor Econômico", color=discord_color, url='https://valor.globo.com/')
    embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
    embed.set_thumbnail(url="https://s3.glbimg.com/v1/AUTH_1b264e8ce06649ae85acee5d38e32f34/images/novo_logo_valor_economico.png")

    valorUrl = requests.get(url="https://valor.globo.com/")
    soupValor = BeautifulSoup(valorUrl.content, 'html5lib')

    allBlocks = soupValor.find_all('div', class_="highlight__content")

    for index, block in enumerate(allBlocks, 1):
        if index > 6:
            break
        else:
            title = block.find('h2', class_='highlight__title')
            aTag = block.find('a')
            link = aTag['href']
            embed.add_field(name=f"{index} - **{title.get_text(strip=True)}**", value=f"{link}", inline=True)

    await ctx.send(embed=embed)

bot.run(token)