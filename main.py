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
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
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
    'DNT': '1',}

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comando(s) foram sincronizado(s)")
    except Exception as e:
        print(f"Falha ao sincronizar os comandos: {e}")
    print(f'Iniciado e logado como: {bot.user}')

@bot.tree.command(name="valor", description="Receba as principais notícias da página inicial do site Valor econômico")
async def valor(interaction:discord.Interaction):
    await interaction.response.defer()
    try:
        color_hex = "#016667"
        discord_color = int(color_hex[1:], 16)
        embed = discord.Embed(title="Valor Econômico", url='https://valor.globo.com/', color=discord_color)
        embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
        embed.set_thumbnail(url="https://s3.glbimg.com/v1/AUTH_1b264e8ce06649ae85acee5d38e32f34/images/novo_logo_valor_economico.png")

        valorUrl = requests.get(url="https://valor.globo.com/", headers=headers)
        soupValor = BeautifulSoup(valorUrl.content, 'html5lib')
        allBlocks = soupValor.find_all('div', class_="highlight__content")
        ibovespaPercentage = soupValor.find(class_="valor-data-chart__head__variation")
        ibovespaPoints = soupValor.find(class_="valor-data-chart__head__points")
        tabelas = soupValor.find(class_="section-data__table")
        index = 1

        for block in allBlocks:
            #if we pass the 6th news start making the footer
            #"why you just don't use footer on the embed?" because the code is mine
            if index > 6:
                if ibovespaPercentage.get_text(strip=True).startswith('-'):
                    embed.add_field(name=f"Porcentagem Ibovespa: 🔻📉 **{ibovespaPercentage.get_text(strip=True)}** 🔻📉",
                                    value=f"Pontos: **{ibovespaPoints.get_text(strip=True)}**")
                else:
                    embed.add_field(name=f"Porcentagem Ibovespa: 📈✅ **{ibovespaPercentage.get_text(strip=True)}** ✅📈",
                                    value=f"Pontos: **{ibovespaPoints.get_text(strip=True)}**")

                #get all the Currency Exchange and just show the comercial values
                for row in tabelas.find_all('tr'):
                    if index == 7: #ignore the first table row that only have things we alredy got before
                        index += 1
                        pass
                    elif index == 8 or index == 10: #only shows the important ones
                        cells = row.find_all('td')
                        moeda = cells[0].get_text(strip=True)
                        compra = cells[1].get_text(strip=True)
                        embed.add_field(name=f"**{moeda}**",
                                        value=f"Valor de compra: **{compra}**",
                                        inline=False)
                        index += 1
                    else:
                        index += 1
                break
            else:
                try: #Get all the main news
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

@bot.tree.command(name='estadao', description="Receba as principais notícias da página inicial do site Estadão")
async def estadao(interaction:discord.Interaction):
    await interaction.response.defer()
    try:
        estadaoUrl = requests.get(url="https://www.estadao.com.br/", headers=headers)
        estadaoSoup = BeautifulSoup(estadaoUrl.content, 'html5lib')
        headlines = estadaoSoup.find_all(class_="headline")

        color_hex = '#0076ec'
        discord_color = int(color_hex[1:], 16)
        embed = discord.Embed(title="Estadao", url='https://www.estadao.com.br/', color=discord_color)
        embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
        embed.set_thumbnail(url="https://statics.estadao.com.br/s2016/portal/logos/metadados/estadao_1x1.png")

        for index, item in enumerate(headlines, start=1):
            if index > 6:
                break
            else:
                if item.find('a'):
                    link = item.find('a')['href']
                    embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**", value=f'{link}', inline=True)
                else:
                    if item.find_parent('a'):
                        link = item.find_parent('a')['href']
                        embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**", value=f'{link}', inline=True)
        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="oglobo", description="Receba as principais notícias da página inicial do site O Globo")
async def oglobo(interaction:discord.Interaction):
    await interaction.response.defer()
    try:
        color_hex = '#014687'
        discord_color = int(color_hex[1:], 16)
        embed = discord.Embed(title="O Globo", url='https://oglobo.globo.com/', color=discord_color)
        embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
        embed.set_thumbnail(url="https://d37iydjzbdkvr9.cloudfront.net/google-assistant/o-globo/logo-globo-1000x1000.jpg")


        ogloboUrl = requests.get(url="https://oglobo.globo.com/", headers=headers)
        ogloboSoup = BeautifulSoup(ogloboUrl.content, 'html5lib')
        manchetes = ogloboSoup.find_all(class_="title")
        bullets = ogloboSoup.find_all(class_="manchete_bullets__title_bullet")
        titulos = ogloboSoup.find_all(class_="highlight__title")
        index = 1


        for item in manchetes:
            if index > 9:
                break
            else:
                embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**",
                                value=f"{item.find_parent('a')['href']}", inline=True)
                index += 1

        for item in bullets:
            if index > 9:
                break
            else:
                embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**",
                                value=f"{item.find_parent('a')['href']}", inline=True)
                index += 1

        for item in titulos:
            if index > 9:
                break
            else:
                embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**",
                                value=f"{item.find('a')['href']}", inline=True)
                index += 1

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="veja", description="Receba as principais notícias da página inicial do site Veja")
async def veja(interaction:discord.Interaction):
    await interaction.response.defer()
    try:
        color_hex = '#af0f08'
        discord_color = int(color_hex[1:], 16)
        embed = discord.Embed(title="Veja", url='https://veja.abril.com.br/', color=discord_color)
        embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0CXVHrn1kc_dh1MQZKi-4RYds3pVmQZdN2g&s")

        vejaUrl = requests.get(url="https://veja.abril.com.br/")
        vejaSoup = BeautifulSoup(vejaUrl.content, 'html5lib')
        titulos = vejaSoup.find_all(class_='title')

        for index, item in enumerate(titulos, start=1):
            if index > 9 or item.get_text(strip=True) == 'Continua após publicidade':
                break
            else:
                embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**",
                                value=f"{item.find_parent('a')['href']}")

        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="uol", description="Receba as principais notícias da página inicial do site UOL")
async def uol(interaction:discord.Interaction):
    await interaction.response.defer()
    try:
        color_hex = '#ff8100'
        discord_color = int(color_hex[1:], 16)
        embed = discord.Embed(title="Uol", url='https://www.uol.com.br/', color=discord_color)
        embed.set_author(name="Repositório oficial no github", url='https://github.com/Kelvinhcs/BotNews')
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/b/bd/UOL_logo.png")

        uolUrl = requests.get(url="https://www.uol.com.br/")
        uolSoup = BeautifulSoup(uolUrl.content, 'html5lib')
        titulos = uolSoup.find_all('h3', class_='title__element')

        for index, item in enumerate(titulos, start=1):
            if index > 9:
                break
            else:
                embed.add_field(name=f"{index} - **{item.get_text(strip=True)}**",
                                value=f"{item.find_parent('a')['href']}")
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")


bot.run(token)