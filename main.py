import random
import discord
from bot_logic import gen_pass, gen_emodji, flip_coin
from settings import settings

# La variable intents almacena los privilegios del bot
intents = discord.Intents.default()
# Activar el privilegio de lectura de mensajes
intents.message_content = True
# Crear un bot en la variable cliente y transferirle los privilegios
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Hemos iniciado sesión como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    contenido = message.content.lower()
    respuesta = ""
    
    if contenido.startswith('hi'):
        respuesta = "Hi!"
    elif contenido.startswith("baila tu cuerpo alegria macarena"):
        respuesta = "que tu cuerpo pa' dale alegria y cosa buena"

    elif contenido.startswith('$smile'):
        respuesta = gen_emodji()
    elif contenido.startswith('$coin'):
        respuesta = str(flip_coin())
    elif contenido.startswith('$pass'):
        respuesta = gen_pass(10)
        
    # Comando de Piedra, Papel o Tijera
    elif contenido.startswith('!ppt'):
        partes = message.content.split()
        if len(partes) > 1:
            eleccion_usuario = partes[1].lower()
            opciones = ["piedra", "papel", "tijera"]
            
            if eleccion_usuario in opciones:
                eleccion_bot = random.choice(opciones)
                
                if eleccion_usuario == eleccion_bot:
                    res = "¡Empate!"
                elif (eleccion_usuario == "piedra" and eleccion_bot == "tijera") or \
                     (eleccion_usuario == "papel" and eleccion_bot == "piedra") or \
                     (eleccion_usuario == "tijera" and eleccion_bot == "papel"):
                    res = "¡Le ganaste al bot! "
                else:
                    res = "¡Te gané! :)"
                    
                respuesta = f"Tú elegiste {eleccion_usuario}, yo elegí {eleccion_bot}. {res}"
            else:
                respuesta = "Elige entre: `piedra`, `papel` o `tijera`."
        else:
            respuesta = "Usa el formato correcto: `!ppt piedra` (o papel / tijera)"

    # Comando de Slap (Palmada)
    elif contenido.startswith('!slap'):
        # message.mentions contiene una lista de todos los usuarios mencionados en el mensaje
        if len(message.mentions) > 0:
            usuario_objetivo = message.mentions[0]
            respuesta = f"👋 {message.author.mention} le dio una tremenda palmada a {usuario_objetivo.mention} por portarse mal."
        else:
            respuesta = "Tienes que mencionar a alguien. Ejemplo: `!slap @usuario`"
            
    else:
        # Si no es un comando conocido, el bot lo ignora por completo
        return

    # Enviar la respuesta únicamente por el chat de Discord
    await message.channel.send(respuesta)

client.run(settings["TOKEN"])