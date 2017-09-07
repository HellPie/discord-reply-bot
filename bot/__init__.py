import re
import json
from random import randint

from discord import Game
from discord.ext.commands import Bot

from bot.config import CONFIG

PARENTS = ['202163416083726338', '225511609567543297']  # HellPie, Kirei
ADORABLE_PEOPLE = ['202163416083726338', '225511609567543297', '245997507606216704',
                   '210279248685039616']  # HellPie, Kirei, Sejin, Amanda.
ZANTOMODE_PEOPLE = ['172331493828460545', '88792744587169792'].extend(ADORABLE_PEOPLE)  # zanto, SakuraJinkyu
LESSER_CREATURES = ['228162606580367370', '280096430356430848']  # Sageth, Pmik
CHANCE_FACTOR = 1  # 20%

REPLIES_STATUS = True

SIMULATE_USER = None
SIMULATE_COUNT = 0

ZANTOCONF = {}

bot = Bot(CONFIG.get(section='BOT', option='PREFIX').split(' '), description=CONFIG['BOT']['DESCRIPTION'])


@bot.event
async def on_ready():
	print('Logged in as:')
	print('Username: ' + bot.user.name)
	print('ID: ' + bot.user.id)
	print('------')


@bot.event
async def on_message(message):
	if message.author.id == bot.user.id:
		return
	if not REPLIES_STATUS and message.author.id not in ADORABLE_PEOPLE:  # Bypass disabled replies for the selected few
		await bot.process_commands(message)
		return
	author = message.author
	global SIMULATE_USER
	global SIMULATE_COUNT
	if SIMULATE_USER is not None and SIMULATE_COUNT > 0:
		author = await bot.get_user_info(SIMULATE_USER)  # Change the user to the test subject
		SIMULATE_COUNT -= 1
	if re.compile('^ay[y]+$', re.IGNORECASE).match(message.content):
		if author.id == '208286812089614337' and randint(0, 9) <= CHANCE_FACTOR:  # Obi
			return await bot.send_message(message.channel, 'lmao <:obi_face:330095063067525132>')
		return await  bot.send_message(message.channel, 'lmao')
	elif re.compile('^wew$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'lad')
	elif re.compile('^dead$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'ass')
	elif re.compile('^frigg$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'off')
	elif re.compile('^oh? ?shit$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'waddup')
	elif re.compile('^shut ?up!?( @.+#\d+!?)?$', re.IGNORECASE).match(message.content) and message.author.id not in ADORABLE_PEOPLE:  # Always disable mean replies for nice people
		return await bot.send_message(message.channel, 'wow, such a Sageth')  # Gone, but I like this too much
	elif re.compile('^k( .*)?$', re.IGNORECASE).match(message.content) and author.id == '170985598297964544':  # DMX
		_random = randint(0, 3)
		if _random == 0:
			return await bot.send_message(message.channel, 'fuck off DMX')
		if _random == 1:
			return await bot.send_message(message.channel, 'Wow... how original...')
		if _random == 2:
			return await bot.send_message(message.channel, 'https://cdn.discordapp.com/attachments/313911775500173313/344152842614865923/6e3.png')
		if _random == 3:
			return await bot.send_message(message.channel, 'k, nard')
	elif re.compile('^fuck off( [a-z#0-9]+)?$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, '{} has got work to do'.format(message.author.name))
	elif re.compile('^smokes$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'let\'s go')
	elif re.compile('^safety$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'always off')
	elif re.compile('^sh?leep ti(ght|te)(,? [a-z#0-9]+)?$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'don\'t let the genjis bite')
	elif re.compile('^i( ?(ly|((love|luv) (yo)?u))),? (@?(Not)?Hime|(@auto-reply-bot#9347|<@!311154146969518083>))!?$', re.IGNORECASE).match(message.content):
		if author.id == '208286812089614337':  # Obi
			return await bot.send_message(message.channel, 'ily too obi <3{}'.format(
				' <:obi_face:330095063067525132>' if randint(0, 9) <= CHANCE_FACTOR else '.'))
		elif author.id == '225511609567543297':  # Kirei <3
			return await bot.send_message(message.channel, 'ily a lot mommy :two_hearts: :two_hearts: ^~^')
		elif author.id == '202163416083726338':  # _HellPie
			return await bot.send_message(message.channel, 'ily too dad <3 <3 ^~^')
		elif author.id in ['117349345296121864', '245997507606216704', '210279248685039616']:  # Halo, sejin., Amanda.
			return await bot.send_message(message.channel, 'cute angel main, ily too \\*-\\*')
		elif author.id == '157725308127150081':  # Bjorn
			return await bot.send_message(message.channel, 'ily too darlin\' c:')
		elif author.id == '133006275305930753':  # Lotus
			return await bot.send_message(message.channel, 'Same, but Id love you more if you switched off widow...')
		elif author.id in LESSER_CREATURES:
			return await bot.send_message(message.channel, '1. wow, pedo 2. I have a boyfriend')
		else:
			return await bot.send_message(message.channel, 'ty, have a nice day darlin\'')
	elif re.compile('^suc[ck] an? egg$', re.IGNORECASE).match(message.content) and message.author.id not in ADORABLE_PEOPLE:  # Always disable mean replies for nice people
		return await bot.send_message(message.channel, 'no, you, eggsucker')
	elif re.compile('^wo[ah]{2}!*$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'WOW')
	elif re.compile('^no((rmie)|(o+b))s?!*$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'reeeeeeeeeeeeeeeeeeee, just like obi')
	elif re.compile('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:calvinHug:\d+>',  re.IGNORECASE).match(message.content):
		final_emote = ''
		if author.id in ADORABLE_PEOPLE:
			final_emote = '<:moon2cute:316630780313075712>'
		return await bot.send_message(message.channel, '<@{}> <:jay3hugged:332946887202308097> {}'.format(author.id, final_emote))
	elif re.compile('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:jay3hugged:\d+>', re.IGNORECASE).match(message.content):
		final_emote = ''
		if author.id in ADORABLE_PEOPLE:
			final_emote = '<:moon2cute:316630780313075712>'
		return await bot.send_message(message.channel, '<@{}> <:calvinHug:326950539524964352> {}'.format(author.id, final_emote))
	else:
		await bot.process_commands(message)


@bot.command(pass_context=True)
async def zantoconf(ctx,  *body):  # Use ':$zantoconf <character> as <emote>' to replace ONE character with an emote or any other string in ':$zantomode <text>'
	if ctx.message.author.id not in PARENTS and ctx.message.author.id not in ZANTOMODE_PEOPLE:
		return
	args = ' '.join(body).split(' as ')
	if len(args) < 2:
		return await bot.send_message(ctx.message.channel, "Need something like ':$zantoconf <character> as <emote>'")
	ZANTOCONF[args[0]] = args[1]
	with open('zantoconf.json', 'w') as zantoconfjson:  # Never delete this file, it's the thing that stores the settings
		json.dump(ZANTOCONF, zantoconfjson)
	return await bot.send_message(ctx.message.channel, "{} => {} - Configured".format(args[0], args[1]))


@bot.command(pass_context=True)
async def zantomode(ctx, *sentence):
	if ctx.message.author.id not in PARENTS and ctx.message.author.id not in ZANTOMODE_PEOPLE:  # Zanto, SakuraJinkyu
		return
	global ZANTOCONF
	with open('zantoconf.json') as zantoconfjson:
		ZANTOCONF = json.load(zantoconfjson)
	# space = "<:regional_indicator_none:336187638514057226>"  # Custom emoji for an empty blue square
	space = "<:jay3thinking:332958429083729933> "
	message = ' '
	sentence = ' '.join(sentence)
	for c in sentence:
		c = c.lower()
		if c in ZANTOCONF:
			message += '{} '.format(str(ZANTOCONF[c]))
		elif c == ' ':
			message += space
		elif c == '?':
			message += ':question: '
		elif c == '!':
			message += ':exclamation: '
		elif re.compile('[a-z]', re.IGNORECASE).match(c):
			message += ':regional_indicator_{}: '.format(c.lower())
	if message != ' ':
		return await bot.send_message(ctx.message.channel, message)
	else:
		return await bot.send_message(ctx.message.channel, "Unable to emojify message :(")


@bot.group(pass_context=True)
async def himemod(ctx):
	pass


@himemod.command(pass_context=True)
async def config(ctx, flag, value, *extras):
	if ctx.message.author.id != '202163416083726338':  # HellPie
		return
	if flag == 'STATUS':
		await bot.change_presence(game=Game(name=value if value is not None else '', url=extras[0] if len(extras) > 0 and extras[0] is not None else '', type=1 if len(extras) > 1 and extras[1] == 'STREAM' else 0))
	elif flag == 'SIMULATE':
		global SIMULATE_USER
		if value is not None or value is not 'None':
			SIMULATE_USER = value
			user = await bot.get_user_info(SIMULATE_USER)
			value = '{}#{}'.format(user.name, user.discriminator)
		for args in extras:
			kvpair = args.split(':')
			global SIMULATE_COUNT
			if kvpair[0] == 'count':
				SIMULATE_COUNT = int(kvpair[1])
			elif kvpair[0] == 'stop':
				SIMULATE_COUNT = 0
	elif flag == 'REPLIES':
		global REPLIES_STATUS
		if value is None or value is '' or value == 'TOGGLE':
			value = 'OFF' if REPLIES_STATUS else 'ON'
		if value == 'ON':
			REPLIES_STATUS = True
		elif value == 'OFF':
			REPLIES_STATUS = False
	return await bot.send_message(ctx.message.channel, 'Updated: `{}` to `{}`{}'.format(flag, value, 'with extras `{}`'.format(extras) if len(extras) > 0 else ''))


def start():
	bot.run(CONFIG.get(section='LOGIN', option='TOKEN'))
