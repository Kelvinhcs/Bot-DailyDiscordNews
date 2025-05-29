import requests
from bs4 import BeautifulSoup
import discord
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

g1 = requests.get(url="https://g1.globo.com")
soup = BeautifulSoup(g1.content, 'html5lib')




@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    lowerMessage = message.content.lower()
    if message.author == bot.user:
        return

    elif lowerMessage.startswith('$on'):
        await message.channel.send('Olá, o bot está funcionando perfeitamente até o momento')

    elif lowerMessage.startswith('$ping'):
        await message.channel.send(f'Pong! {bot.latency * 1000:.2f}ms')

    elif lowerMessage.startswith('$g1'):
        await message.channel.send('Carregando notícias...')
        newsMessage = '📰-=-=-=-=-=-=-=-=-=-=- **News G1** -=-=-=-=-=-=-=-=-=-=-📰\n\n'
        noticias = soup.find_all(attrs={"elementtiming": "text-ssr"})

        for contador, item in enumerate(noticias, start=1):
            link = item.find_parent('a')
            if link and link.get('href'):
                newsMessage += (
                    f'{contador} - **{item.get_text(strip=True)}**\n'
                    f'Link: <{link["href"]}>\n\n'
                )
        if len(newsMessage) <= 200:
            await message.channel.send(newsMessage)
        else:
            parts = [newsMessage[i:i+2000] for i in range(0, len(newsMessage), 2000)]
            for part in parts:
                await message.channel.send(part)

bot.run(token)