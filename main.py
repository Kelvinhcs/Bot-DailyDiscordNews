import discord
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv


load_dotenv()
token = getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comando(s) foram sincronizado(s)")
    except Exception as e:
        print(f"Falha ao sincronizar os comandos: {e}")
    print(f'Iniciado e logado como: {bot.user}')


@bot.tree.command(name="valor", description="Receba as top 6 notícias da página inicial do site Valor econômico")
async def valor(interaction:discord.Interaction):
    await interaction.response.defer()
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
        }
        color_hex = "#016667"
        discord_color = int(color_hex[1:], 16)
        embed = discord.Embed(title="Valor Econômico", url='https://valor.globo.com/', color=discord_color)
        embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
        embed.set_thumbnail(url="https://s3.glbimg.com/v1/AUTH_1b264e8ce06649ae85acee5d38e32f34/images/novo_logo_valor_economico.png")

        valorUrl = requests.get(url="https://valor.globo.com/")
        soupValor = BeautifulSoup(valorUrl.content, 'html5lib')
        allBlocks = soupValor.find_all('div', class_="highlight__content")
        index = 1
        for block in allBlocks:
            if index > 6:
                break
            else:
                try:
                    title = block.find('h2', class_='highlight__title')
                    aTag = block.find('a')
                    link = aTag['href']
                    embed.add_field(name=f"{index} - **{title.get_text(strip=True)}**", value=f"{link}", inline=True)
                    index += 1
                except Exception as e:
                    print(f"Alguma coisa deu errado: {e}")
                    index -= 1
                    pass

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="g1", description="Receba as top 6 notícias da página inicial do site G1")
async def g1(interaction:discord.Interaction):
    await interaction.response.defer()
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
        }
        color_hex = '#c2170a'
        discord_color = int(color_hex[1:], 16)
        embed = discord.Embed(title="G1", url='https://g1.globo.com/', color=discord_color)
        embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
        embed.set_thumbnail(url="https://s03.video.glbimg.com/x720/2535726.jpg")

        g1Url = requests.get(url="https://g1.globo.com", headers=headers)
        soupG1 = BeautifulSoup(g1Url.content, 'html5lib')
        noticias = soupG1.find_all(attrs={"elementtiming": "text-ssr"})
        for index, item in enumerate(noticias, start=1):
            if index > 6:
                break
            else:
                try:
                    aTag = item.find_parent('a')
                    link = aTag.get('href')
                    embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**", value=f'{link}', inline=True)
                except Exception as e:
                    print(f"Alguma coisa deu errado: {e}")
                    pass
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")



bot.run(token)