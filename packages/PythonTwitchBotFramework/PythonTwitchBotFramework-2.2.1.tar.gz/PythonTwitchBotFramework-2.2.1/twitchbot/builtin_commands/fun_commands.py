from secrets import choice
from random import randint

from twitchbot import (
    Message,
    CommandContext,
    Command,
    InvalidArgumentsError
)


@Command('roll', context=CommandContext.BOTH, syntax='(sides)', help='rolls a X sided die')
async def cmd_roll(msg: Message, *args):
    try:
        sides = int(args[0]) if args else 6
    except ValueError:
        raise InvalidArgumentsError(reason='invalid value for sides', cmd=cmd_roll)

    num = randint(1, sides)
    user = msg.mention if msg.is_privmsg else ''
    await msg.reply(f'{user} you rolled a {num}')


@Command('crashcode', permission='crashcode')
async def cmd_crash_code(msg: Message, *args):
    await msg.reply(f'you may not crash me! {msg.mention}')


@Command('choose', syntax='<option> <option> ect', help='chooses a random option passed to the command')
async def cmd_choose(msg: Message, *args):
    if len(args) < 2:
        raise InvalidArgumentsError(reason='missing required arguments', cmd=cmd_choose)

    await msg.reply(f'result: {choice(args)}')


@Command('color', permission='color', syntax='<color>', help='sets the bots chat color')
async def cmd_color(msg: Message, *args):
    if not args:
        raise InvalidArgumentsError(reason='missing required arguments', cmd=cmd_color)

    await msg.channel.color(args[0])
    await msg.reply(f'set color to {args[0]}')


magic_8_ball_messages = [
    'it is certain',
    'yes',
    'not happening',
    'no',
    'maybe',
    "it's possible",
]


@Command('8ball', syntax='<question>', help='prints a random answer to the question')
async def cmd_8ball(msg: Message, *args):
    await msg.reply(f'{msg.mention} {choice(magic_8_ball_messages)}')
