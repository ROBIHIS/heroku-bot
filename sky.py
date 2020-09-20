import discord
from random import randint, choice
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl
import os
from time import sleep
import requests
import io
import asyncio
from Cybernator import Paginator as pag
import json
import pyowm
import random
from requests import get
from datetime import datetime
import googletrans 
from googletrans import Translator
import time
import pyqrcode
import png

PREFIX = ','

client = commands.Bot( command_prefix = PREFIX )
client.remove_command('help')

# Clear message
@client.command()
@commands.has_permissions( administrator = True )
 
async def clear( ctx, amount : int ):
    await ctx.channel.purge( limit = amount +1 )
 
    await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений', color=0x0c0c0c))

# Kick
@client.command()
@commands.has_permissions( administrator = True )
 
async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.kick( reason = reason )
 
    emb = discord.Embed( title = 'Информация об изгнании', description = f'{ member.name.title() }, был выгнан в связи нарушений правил',
    color = 0xc25151 )
 
    emb.set_author( name = member, icon_url = member.avatar_url )
    emb.set_footer( text = f'Был изганан администратором { ctx.message.author.name }', icon_url = ctx.author.avatar_url )
 
    await ctx.send( embed = emb )

 # Ban
@client.command()
@commands.has_permissions( administrator = True )
 
async def ban( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.ban( reason = reason )
 
    emb = discord.Embed( title = 'Информация о блокировке участника', description = f'{ member.name }, был заблокирован в связи нарушений правил',
    color = 0xc25151 )
 
    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = f'ID: { member.id }', value = f'Блокированный участник : { member }' )
    emb.set_footer( text = 'Был заблокирован администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
 
    await ctx.send( embed = emb )

# Unban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )
        await ctx.send( f'Unbanned user:{ user.mention }' )

        return

@client.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

# Time
async def time( ctx ):
    emb = discord.Embed( title = 'ВРЕМЯ', description = 'Вы сможете узнать текущее время', colour = discord.Color.green(), url = 'https://www.timeserver.ru' )
 
    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer( text = 'Спасибо за использование нашего бота!' )
    emb.set_thumbnail( url = 'https://sun9-35.userapi.com/c200724/v200724757/14f24/BL06miOGVd8.jpg' )
 
    now_date = datetime.datetime.now()
 
    emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ) )
 
    await ctx.author.send( embed = emb )

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx,member:discord.Member,time:int,reason):
    muterole = discord.utils.get(ctx.guild.roles,id=750019233559216139)
    emb = discord.Embed(title="Мут",color=0xff0000)
    emb.add_field(name='Модератор',value=ctx.message.author.mention,inline=False)
    emb.add_field(name='Нарушитель',value=member.mention,inline=False)
    emb.add_field(name='Причина',value=reason,inline=False)
    emb.add_field(name='Время',value=time,inline=False)
    await member.add_roles(muterole)
    await ctx.send(embed = emb)
    await asyncio.sleep(time)
    await member.remove_roles(muterole)

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоеденился к каналу: {channel}')

# Leave_voice
@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
# Card
@client.command(aliases = ['карта', 'card'])
async def card_user(ctx):
    img = Image.new('RGBA', (400, 200), '#232529')
    url = str(ctx.author.avatar_url)[:-10]

    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)

    img.paste(response, (15, 15, 115, 115))

    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator

    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)

    idraw.text((145, 15), f'{name}#{tag}', font = headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

    img.save('user_card.png')

    await ctx.send(file = discord.File(fp = 'user_card.png'))

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')
 
    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')
 
    await ctx.send('Пожалуйста ожидайте')
 
    voice = get(client.voice_clients, guild = ctx.guild)
 
    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }
 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])
 
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')
 
    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
 
    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас проигрывает музыка: {song_name[0]}')

# Pat
@client.command(aliases =['patt', 'Pat'])
async def pat(ctx, member : discord.Member = None):
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)
    print(f'Команду pat использовал пользователь {ctx.author.name}')
    embed = discord.Embed(title = f"{ctx.author} погладил'а {member}",color =0x2196F3)
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

# Hug
@client.command(aliases =['hugg', 'Hug'])
async def hug(ctx, member : discord.Member = None):
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)
    print(f'Команду hug использовал пользователь {ctx.author.name}')
    embed = discord.Embed(title = f"{ctx.author} обнял'а {member}",color =0x2196F3)
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

# Ping
@client.command()
async def ping(ctx):
    ping = client.latency
    ping_emoji = "🟩🔳🔳🔳🔳"
    
    ping_list = [
        {"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
        {"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
        {"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
        {"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
        {"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
        {"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}]
    
    for ping_one in ping_list:
        if ping > ping_one["ping"]:
            ping_emoji = ping_one["emoji"]
            break

    message = await ctx.send("Пожалуйста, подождите. . .")
    await message.edit(content = f"Понг! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:")

# Да я выбрался из дурки и что блять вы обосрались?
@client.command()
async def kill( ctx, member: discord.Member ):

    embed = discord.Embed(title = 'Выстрел', description = 'Вы сможете в кого-то выстрелить.', colour = discord.Color.red())

    embed.add_field( name = '**Доставание дробовика**', value = f"{ctx.author.mention} достаёт дробовик...", inline = False )

    await asyncio.sleep( 3 )
    embed.add_field( name = '**Направление дробовика**', value = f"{ctx.author.mention} направляет дробовик на {member.mention}...", inline = False )

    await asyncio.sleep( 2 )
    embed.add_field( name = '**Стрельба**', value = f"{ctx.author.mention} стреляет в {member.mention}...", inline = False )

    embed.set_image(url='https://media.discordapp.net/attachments/690222948283580435/701494203607416943/tenor_3.gif')

    await asyncio.sleep( 2 )
    embed.add_field( name = '**Кровь**', value = f"{member.mention} истекает кровью...", inline = False )

    await ctx.send( embed = embed )

@client.command()
async def rand(ctx):
	await ctx.send(f"🎲| Вам выпало {random.randint(0, 100)}")

########################
#For use:              #
#pip install discord.py#
########################
#Time in voice         #
#Using JSON            #
#For cogs              #
########################
#By Jabka#5003         #
########################
class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []
 
@client.command(aliases =['winkk', 'Wink'])
async def wink(ctx, member : discord.Member = None):
    response = requests.get('https://some-random-api.ml/animu/wink')
    json_data = json.loads(response.text)
    print(f'Команду wink использовал пользователь {ctx.author.name}')
    embed = discord.Embed(title = f"{ctx.author} подмигинул'a {member}",color =0x2196F3)
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

@client.command()
async def servera(ctx):
    total = 0
    for guild in client.guilds:
        if ctx.author in guild.members:
            total += 1
    await ctx.send(f"Общих серверов: {total}")

@client.command()
async def avatar(ctx, member: discord.Member):
    if not member:
        member = ctx.author

    await ctx.message.delete()

    user = ctx.message.author if not member else member

    embed = discord.Embed(title = f'Аватар пользователя {member}', color = 0xFF000)

    embed.set_image(url = user.avatar_url_as(format = None, size = 4096))
    embed.set_author(icon_url = 'https://www.flaticon.com/premium-icon/icons/svg/2919/2919600.svg', name = 'Участник | Аватар')
    embed.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)
    embed.timestamp = datetime.utcnow()

    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions( administrator = True )
async def changestatus( ctx, statustype:str = None, *, arg:str = None):
    if statustype is None: # Type Check
        await ctx.send( 'Вы не указали тип Статуса' )
    elif arg is None: # Arg Check
        await ctx.send( 'Вы не указали нужный аргумент' )
    else:
        if statustype.lower() == 'game': # Game
            await client.change_presence (activity=discord.Game( name = arg) )
        elif statustype.lower() == 'listen': # Listen
            await client.change_presence( activity=discord.Activity( type=discord.ActivityType.listening, name = arg) )
        elif statustype.lower() == 'watch': # Watch
            await client.change_presence( activity=discord.Activity( type=discord.ActivityType.watching, name = arg) )

@client.command()
async def wiki(ctx, *, query: str):

    msg = await ctx.send("Пожалуйста, подождите. . .")
    sea = requests.get(
        ('https://ru.wikipedia.org//w/api.php?action=query'
         '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
        ).format(query)).json()['query']

    if sea['searchinfo']['totalhits'] == 0:
        await ctx.send(f'По запросу **"{query}"** ничего не найдено :confused:')
    else:
        for x in range(len(sea['search'])):
            article = sea['search'][x]['title']
            req = requests.get('https://ru.wikipedia.org//w/api.php?action=query'
                               '&utf8=1&redirects&format=json&prop=info|images'
                               '&inprop=url&titles={}'.format(article)).json()['query']['pages']
            if str(list(req)[0]) != "-1":
                break
        article = req[list(req)[0]]['title']
        arturl = req[list(req)[0]]['fullurl']
        artdesc = requests.get('https://ru.wikipedia.org/api/rest_v1/page/summary/' + article).json()['extract']
        embed = discord.Embed(title = article, url = arturl, description = artdesc, timestamp = datetime.utcnow(), color = 0x00ffff)
        embed.set_author(name = 'Google | Википедия', url = 'https://en.wikipedia.org/', icon_url = 'https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
        embed.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)

        await msg.delete()
        await ctx.send(embed = embed)

translator = Translator()

@client.command()
async def translate(ctx, dest, *, txt: str):
    try:
        result = translator.translate(txt, dest = dest)

        embed = discord.Embed(title = f'**Перевод твоего сообщения**',
                          description = f"**Твое сообщение:** - {result.origin}\n\n"
                                      f"**Перевод:** - {result.text}\n\n",
                        timestamp = datetime.utcnow(), color = 0x00FF00)
        embed.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)
        embed.set_thumbnail(
            url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Google_Translate_logo_%28old%29.png')
    
        await ctx.send(embed = embed)

    except ValueError:
        embed = discord.Embed(
            description = f':x: {ctx.author.mention}, данного **языка** не существует, я отправлю список **языков** тебе в **лс** :x:',
            timestamp = datetime.utcnow(), color = 0xff0000)

        embed.set_author(icon_url='https://www.flaticon.com/premium-icon/icons/svg/1828/1828665.svg',
                         name = 'Бот | Ошибка')
        embed.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)

        await ctx.send(embed = embed)

        languages = ", ".join(googletrans.LANGUAGES)

        embed = discord.Embed(description = f'**Список всех языков:** {languages}', timestamp = datetime.utcnow(),
                              color = 0x00FF00)

        embed.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)

        await ctx.author.send(embed = embed)

keys = ("z","Z","x","X","c","C","v","V","b","B","n","N","m","M","a","A","s","S","d","D","f","F","g","G","h","H","j","J","k","K","l","L","q","Q","w","W","e","E","r","R","T","t","y","Y","u","U","i","I","o","O","P","p")
@client.command()
async def nitro(ctx):
        a = "https://discord.gift/"
        
        while True:
            cou = 0
            link = ""
            while cou  < 24:
                new_bukva = random.choice(keys)
                link += new_bukva
                cou += 1
                
            await ctx.author.send(f"{a}{link}")

@client.command()
async def emoji(ctx, emoji: discord.Emoji = None):
    if not emoji:
        e = discord.Embed(description = ":x: {0}, укажи **эмодзи**, о которым хочешь узнать **информацию** :x:".format(ctx.author.mention), color = 0xFF0000)

        e.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)
        e.timestamp = datetime.utcnow()

        await ctx.send(embed = e)

    e = discord.Embed(description = f"[Эмодзи]({emoji.url}) сервера - {emoji}", color = 0x00FF00)

    e.add_field(name = "Название эмодзи:", value = "**`{0}`**".format(emoji.name))
    e.add_field(name = "Автор:", value = "{0}".format((await ctx.guild.fetch_emoji(emoji.id)).user.mention))
    e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
    e.add_field(name = "Дата добавления:", value = "**`{0}`**".format((emoji.created_at.date())))
    e.add_field(name = "ID эмодзи:", value = "**`{0}`**".format(emoji.id))
    e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
    e.set_thumbnail(url = "{0}".format(emoji.url))
    e.set_author(icon_url = 'https://www.flaticon.com/premium-icon/icons/svg/3084/3084443.svg', name = 'Бот | Эмодзи')
    e.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)
    e.timestamp = datetime.utcnow()

    await ctx.send(embed = e)

@client.command()
async def rv(ctx, *, text: str):

    t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.send(f"{t_rev}")

@client.command(aliases =['погода'])
async def weather(ctx, *, arg):
    embed = discord.Embed(title = 'Ваша погода', description = 'Вы сможете узнать погоду в любом городе', colour = discord.Color.green())

    owm = pyowm.OWM( 'API Key' ) # ставить ваш, вот сайт: https://openweathermap.org/
    city = arg

    observation = owm.weather_at_place( city )
    w = observation.get_weather()
    temperature = w.get_temperature( 'celsius' )[ 'temp' ]

    embed.add_field( name = '**Температура**', value = f'Температура в { city }: { temperature }', inline = False )

    await ctx.send( embed = embed )

@client.command()
async def stats(ctx):
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))
    embed = discord.Embed(title=f'{client.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name='Bot Version:', value='1.0')
    embed.add_field(name='Версия Python:', value='3.7')
    embed.add_field(name='На чём был создан бот:', value='Python, dbfd')
    embed.add_field(name='Discord.Py версия', value=dpyVersion)
    embed.add_field(name='Версия dbfd', value='4.6')
    embed.add_field(name='Число гильдий:', value=serverCount)
    embed.add_field(name='Число всех учасников:', value=memberCount)
    embed.add_field(name='Разработчики бота:', value="<@709811747846094899>, <@690309119663538388>")
    embed.set_footer(text=f"{client.user.name}")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def gc(ctx, name1, name2, name3):
    name123 = str(name1)
    name1234 = str(name2)
    name12345 = str(name3)
    await ctx.guild.edit(name=name123)
    await asyncio.sleep(0.5)
    await ctx.guild.edit(name=name1234)
    await asyncio.sleep(0.5)
    await ctx.guild.edit(name=name12345)
    await asyncio.sleep(0.5)
    task = asyncio.create_task(gc(ctx, name1, name2, name3))

@client.command()
async def serverstate(ctx):
    guild = ctx.guild
    guild_age = (ctx.message.created_at - guild.created_at).days
    created_at = f"{guild.created_at.strftime('%b %d %Y at %H:%M')}. Это {guild_age} дней назад!"
    totalmembers = ctx.guild.members
    channels = ctx.guild.channels
    textchannels = ctx.guild.text_channels
    voicechannels = ctx.guild.voice_channels
    roletotal = ctx.guild.roles
    
    role = discord.utils.get(ctx.guild.roles,id = 700394552468701336)
    embedserverinfo = discord.Embed(
    title=ctx.guild.name,color =role.color)
    embedserverinfo.set_thumbnail(url=ctx.guild.icon_url)
    embedserverinfo.add_field(name="Айди сервера:", value=guild.id, inline=True)
    embedserverinfo.add_field(name="Создатель сервера:", value=guild.owner.mention, inline=True)
    embedserverinfo.add_field(name="Количество участников:", value=f'{len(totalmembers)}', inline=False)
    embedserverinfo.add_field(name="В сети:", value=len({m.id for m in guild.members if m.status is not discord.Status.offline}))
    embedserverinfo.add_field(name="Каналы:", value=f'{len(channels)} [{len(textchannels)} Текстовых | {len(voicechannels)} Голосовых] ', inline=False)
    embedserverinfo.add_field(name="Количество ролей", value=f'{len(roletotal)}', inline=False)
    embedserverinfo.add_field(name="Регион сервера", value=guild.region, inline=False)
    embedserverinfo.add_field(name="Сервер был создан:", value=created_at, inline=False)
    embedserverinfo.set_footer(text='Создатель бота - RoBi')
    await ctx.send(embed = embedserverinfo)

@client.command(pass_context = True)

async def poll(ctx,*,text = None):
    if text == None:
        await ctx.send(f'**{ctx.message.author.name}** вы не ввели текст для голосования')
    else:
        await ctx.message.delete()
        emb = discord.Embed(title='голосование', colour = discord.colour.Color.gold())
        emb.add_field(name=text, value=':white_check_mark:-да\n❌:-нет')
        message = await ctx.send(embed=emb)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

@client.command(aliases=['roleinfo', 'рольинфо', 'rinf'])
async def role_info(ctx, role: discord.Role):

    rol = discord.Embed(description = f' **Информация о роли {role.mention}**', color = 0x25c059 )
    rol.set_thumbnail(url=ctx.guild.icon_url)
    rol.add_field(name= "Название:", value = f'*{role.name}*', inline = False)
    rol.add_field(name= "Айди роли:", value = f'*{role.id}* ', )
    rol.add_field(name= "Сервер:", value = f'*{role.guild}* ', inline = False)
    rol.add_field(name= "Положение роли:", value = f'*{role.position}* ', inline = False)
    rol.add_field(name= "Отображение от других участников:", value = f'*{role.hoist}* ', inline = False)
    rol.add_field(name= "Участников с этой ролью:", value = f'*{len(role.members)}* ', inline = False)
    rol.add_field(name= "Код цвета роли:", value = f'*{role.color}*', inline = False)
    rol.add_field(name= "Дата созадния роли:", value = f'*{role.created_at.strftime("%d.%m.%Y %H:%M")}*', inline = False)
    rol.add_field(name= "Могут ли участники упоминать роль:", value = f'*{role.mentionable}*', inline = False)
    rol.set_footer(text=f'Вызвал: {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed = rol)

@client.event
async def on_member_ban(guild, member):
    channel = client.get_channel( 734043789966049390 )#Айди канала для логов
    embed = discord.Embed(color=member.color if member.color != discord.Color.default() else discord.Color.red(), timestamp=datetime.datetime.now(datetime.timezone.utc), description=f'**{member.mention} was banned**')
    embed.set_author(name=member, icon_url=str(member.avatar_url_as(static_format='png', size=2048)))
    embed.set_footer(text=f"Member ID: {member.id}")
    await channel.send(embed=embed)
            
@client.event
async def on_member_kick(guild, member):
    channel = client.get_channel( 734043789966049390 )#Айди канала для логов
    embed = discord.Embed(color=member.color if member.color != discord.Color.default() else discord.Color.red(), timestamp=datetime.datetime.now(datetime.timezone.utc), description=f'**{member.mention} was kicked**')
    embed.set_author(name=member, icon_url=str(member.avatar_url_as(static_format='png', size=2048)))
    embed.set_footer(text=f"Member ID: {member.id}")
    await channel.send(embed=embed)

@client.event
async def on_member_unban(guild, member):
    channel = client.get_channel( 734043789966049390 )#Айди канала для логов
    embed = discord.Embed(color=discord.Color.green(), timestamp=datetime.datetime.now(datetime.timezone.utc), description=f'**{member} was unbanned**')
    embed.set_author(name=member, icon_url=str(member.avatar_url_as(static_format='png', size=2048)))
    embed.set_footer(text=f"Member ID: {member.id}")
    await channel.send(embed=embed)

@client.event
async def on_invite_create(invite: discord.Invite):
    channel = client.get_channel( 734043789966049390 )#Айди канала для логов
    embed = discord.Embed(color=discord.Color.green(), timestamp=datetime.datetime.now(datetime.timezone.utc), description=f'**An invite was created**')
    embed.add_field(name='Invite Code', value=invite.code, inline=False)
    embed.add_field(name='Max Uses', value=invite.max_uses, inline=False)
    embed.add_field(name='Temporary', value=invite.temporary, inline=False)

    await channel.send(embed=embed)

@client.command(pass_context = True)
async def yt(ctx,*,text):
    author = ctx.message.author
    text = text.replace(' ','+')
    emb = discord.Embed(title='Yotube',colour=discord.colour.Color.red())
    emb.add_field(name=f'поиск: https://m.youtube.com/results?search_query={text}',value=f'ищет:{text}')
    emb.set_footer(text='by Yotube', icon_url='https://im0-tub-ru.yandex.net/i?id=0762b7c1c2e99fcfd5cc7360bf5db446&n=13')
    await ctx.send(embed=emb)
@yt.error
async def yt_error(ctx,error):
    await ctx.message.delete()
    if isinstance(error,commands.MissingRequiredArgument):
        author = ctx.message.author
        await ctx.send(str(author.mention) + ' вы не ввели текст')
@client.command(pass_context = True)
async def поиск(ctx,*,text):
    author = ctx.message.author
    text2 = text.replace('+',' ')
    emb = discord.Embed(title='Google поиск',colour=discord.colour.Color.red())
    emb.add_field(name=f'поиск: https://google.gik-team.com/?q={text}',value=f'ищет: {text2}')
    emb.set_footer(text='by Google', icon_url='https://images-ext-2.discordapp.net/external/cXsT7out8KJ4DCIKXIdToAdstLgIfOwFIFrXVPVHHno/https/upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%2522G%2522_Logo.svg/2000px-Google_%2522G%2522_Logo.svg.png')
    await ctx.send(embed=emb)
@поиск.error
async def поиск_error(ctx,error):
    await ctx.message.delete()
    if isinstance(error,commands.MissingRequiredArgument):
        author = ctx.message.author
        await ctx.send(f'**{author.name}** вы не ввели что хотите найти')

@client.command(pass_context = True)
async def userinfo(ctx,member:discord.Member):
    bot = member.bot
    if bot == False:
        bot = 'Нет'
    else:
        bot = 'Да'
    if member.status == discord.Status.online:
      status = ':green_circle: Онлайн'
    if member.status == discord.Status.offline:
        status = ':black_circle: Оффлайн'
    if member.status == discord.Status.dnd:
        status = ':red_circle:Не беспокоить'
    if member.status == discord.Status.idle:
        status =':yellow_circle: afk'
    guild = ctx.guild
    await ctx.message.delete()
    author = ctx.message.author
    emb = discord.Embed(title='информация о пользователе',colour=discord.colour.Color.red())
    emb.add_field(name='Дата захода в группу:',value=member.joined_at,inline=False)
    emb.add_field(name='Имя:',value=member.display_name,inline=False)
    emb.add_field(name='Тег:',value=member.discriminator,inline=False)
    emb.add_field(name='Айди:',value=member.id,inline=False)
    emb.add_field(name='Статус:',value=status,inline=False)
    emb.add_field(name='Дата создания аккаунта:',value=member.created_at,inline=False)
    emb.add_field(name='Дата входа на сервер:',value=member.joined_at,inline=False)
    if member.id == guild.owner.id:
        emb.add_field(name = 'В данной группе:',value='создатель',inline=False)
    else:
        emb.add_field(name = 'В данной группе:',value='участник',inline=False)
    emb.add_field(name = 'Высшая роль:',value=member.top_role.mention,inline=False)
    emb.add_field(name = 'Всего ролей:',value=len(member.roles),inline=False)
    emb.add_field(name = ':robot:Бот?',value=bot,inline=False)
    emb.set_thumbnail(url=member.avatar_url)
    emb.set_footer(text='запрошено:' + str(author),icon_url=ctx.message.author.avatar_url)
    message = await ctx.send(embed = emb)
    await asyncio.sleep(15)
    await message.delete()
@userinfo.error
async def userinfo_error(ctx,error):
    await ctx.message.delete()
    if isinstance(error,commands.MissingRequiredArgument):
        author = ctx.message.author
        await ctx.send(f'**{author.name}** вы не ввели пользователя о котором хотите узнать информация')

@client.event
async def on_message_delete(guild, member):
    channel = client.get_channel( 734043789966049390 )#Айди канала для логов
    embed = discord.Embed(color=discord.Color.green(), timestamp=datetime.datetime.now(datetime.timezone.utc), description=f'**{member} Удалено сообщения!**')
    embed.set_author(name=member, icon_url=str(member.avatar_url_as(static_format='png', size=2048)))
    embed.set_footer(text=f"Member ID: {member.id}")
    await channel.send(embed=embed)

# Get token
token = open( 'token.txt', 'r' ).readline()
client.run( token )