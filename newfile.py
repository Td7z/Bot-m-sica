import google.generativeai as genai
import discord
from discord import app_commands
from discord.ext import commands
import requests
import datetime

# Substitua pela sua chave de API do Google Generative AI
genai.configure(api_key="SUA_API_KEY_AQUI")

# IDs do seu bot e servidor Discord
clientId = 1164542069814083684 
guildId = 997944541875286098
token = 'SEU_TOKEN_AQUI'

# Criar um novo cliente do Discord
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# Carregar o modelo Gemini
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Mensagem de boas-vindas (apenas no console)
bem_vindo = "# Bem Vindo ao Assistente Mil Grau com Gemini AI #"
print(len(bem_vindo) * "#")
print(bem_vindo)
print(len(bem_vindo) * "#")
print("###   Digite 'sair' para encerrar    ###")
print("")

# Quando o cliente estiver pronto
@client.event
async def on_ready():
    print(f'Logado como {client.user}!')
    try:
        synced = await client.tree.sync(guild=discord.Object(id=guildId))
        print(f'Comandos slash (/) registrados com sucesso: {len(synced)}')
    except Exception as e:
        print(f'Erro ao registrar comandos slash (/): {e}')

# Comando para conversar com o Gemini
@client.tree.command(name="conversar", description="Converse com o Gemini AI!", guild=discord.Object(id=guildId))
async def conversar(interaction: discord.Interaction, *, mensagem: str):
    # Envia a mensagem para o Gemini
    response = chat.send_message(mensagem)

    # Responde ao usuário com a resposta do Gemini
    await interaction.response.send_message(f"**Você:** {mensagem}\n**Gemini:** {response.text}")

# Comando Ping
@client.tree.command(name="ping", description="Responde com Pong!", guild=discord.Object(id=guildId))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Comando Gato
@client.tree.command(name="gato", description="Mostra uma imagem aleatória de gato!", guild=discord.Object(id=guildId))
async def gato(interaction: discord.Interaction):
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        response.raise_for_status()
        imageUrl = response.json()[0]['url']
        embed = discord.Embed(color=0x0099ff, title="Meow!")
        embed.set_image(url=imageUrl)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f'Ocorreu um erro ao buscar a imagem do gato: {e}')
        await interaction.response.send_message('Ocorreu um erro ao buscar a imagem do gato.')

# Comando Data
@client.tree.command(name="data", description="Mostra a data e hora atuais.", guild=discord.Object(id=guildId))
async def data(interaction: discord.Interaction):
    data_formatada = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    await interaction.response.send_message(f'A data e hora atuais são: {data_formatada}')

# Comando Java
@client.tree.command(name="java", description="Obtem O Endereço De IP Minecraft Java Edition", guild=discord.Object(id=guildId))
async def java(interaction: discord.Interaction):
    await interaction.response.send_message("```\nrickmonst.redhosting.com.br\n``` ")

# Comando Bedrock
@client.tree.command(name="bedrock", description="Obtenha O IP  E Porta Do Minecraft Bedrock Edition", guild=discord.Object(id=guildId))
async def Bedrock(interaction: discord.Interaction):
    await interaction.response.send_message("```\nIP : br.redhosting.com.br \nPorta : 25576\n```  ")

# Iniciar o bot
client.run(token)