# bot.py
import asyncio
import json
from datetime import datetime, timedelta
from time import sleep

import discord
from discord.ext import commands

import discord_utils
from bot_config import initialize_bot_config
from bot_service import BotService
from datetime_wrapper import format_timedelta
from emoji_wrapper import THUMBS_UP, THUMBS_DOWN, get_count_for_emoji, BALLOT_BOX
from topic_service import TopicService, get_vote_count

bot = commands.Bot(command_prefix='!')
bot_config = initialize_bot_config(datetime.now())
bot_service = BotService(bot, bot_config)
topic_service = TopicService()


@bot.event
async def on_ready():
    await greet()


async def greet():
    bot_channel_id = bot_service.find_channel_id(bot_config.bot_channel_name)
    bot_channel = await bot.fetch_channel(bot_channel_id)
    await bot_channel.send(f"chirp chirp! I ({bot_config.bot_name}) woke up at: {bot_config.started_at}")


@bot.command(help="Randomly chooses a person from the role set via the SRE_ROLE_NAME environment variable")
async def choose(ctx):
    response = bot_service.handle_choose_member_from()
    await ctx.send(response)


@bot.command()
async def robin_says(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def which(ctx):
    await ctx.send(bot_config.bot_name)


@bot.command()
async def env(ctx):
    await ctx.send(discord_utils.safe_env_vars())


@bot.command()
async def current_config(ctx):
    await ctx.send(discord_utils.current_configuration(bot_config))


@bot.command()
async def health(ctx):
    await ctx.send(discord_utils.health(bot_config))


@bot.command()
async def noise(ctx):
    voicechannel = discord.utils.get(ctx.guild.channels, name='Bot Voice')
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio("youtube-VCLHsusZNQw-Bird_Chirping_Sound_Effect.webm"),
            after=lambda e: print('done', e))
    await ctx.send("playing noise")


@bot.command(aliases=['cd'])
async def countdown(ctx, arg):
    await ctx.send(f"Starting {arg} second timer")
    mins_from_now = datetime.now() + timedelta(seconds=int(arg))
    while datetime.now() < mins_from_now:
        time_remaining_as_delta = mins_from_now - datetime.now()
        if time_remaining_as_delta.seconds < 5:
            await noise(ctx)
        time_remaining = format_timedelta(time_remaining_as_delta)
        await ctx.send(f"{time_remaining} remaining")
        sleep(10)
    await ctx.send("Time's up!")


@bot.command(aliases=['add'])
async def add_topic(ctx, *args):
    topic = ' '.join(map(str, args))
    topic_service.add(topic)
    await ctx.send(f"Added topic: {topic}")


@bot.command()
async def start_topic(ctx, display_id):
    topic = topic_service.get_topic_by_display_id(display_id)
    topic.started = True
    await ctx.send(f"Let's chat about!: {topic.title}")
    should_continue = True
    while should_continue:
        await countdown(ctx, 90)

        continue_vote_msg_id = await call_vote(ctx)
        await countdown(ctx, 18)
        should_continue = await process_vote(ctx, continue_vote_msg_id)

    next_topic = topic_service.get_next_topic(topic)
    await ctx.send(f"Next topic by votes is : {next_topic.title}")
    await ctx.send(f"You can start it when you are ready by using:")
    await ctx.send(f"!start_topic {next_topic.display_id}")


@bot.command()
async def list_topics(ctx):
    await ctx.send(f"Great! Now cast your votes by clicking on the emoji!")
    await list_topics_manual(ctx)


@bot.command(aliases=['list'])
async def list_topics_manual(ctx):
    topics = topic_service.all()

    for t in topics:
        msg = await ctx.send(t.title)
        t.msg_id = msg.id
        await msg.add_reaction(BALLOT_BOX)


@bot.command(aliases=['d', 'display', 'results'])
async def display_results(ctx):
    await ctx.send(f"Alright, here's the topics ordered by number of votes")
    await display_results_manual(ctx)
    await ctx.send(f"Please choose a topic and start it with:")
    await ctx.send(f"!start_topic <topic_number>")


@bot.command()
async def display_results_manual(ctx):
    topics = topic_service.all()

    for t in topics:
        msg = await ctx.fetch_message(t.msg_id)
        t.vote_count = get_vote_count(msg)

    topics_by_vote = sorted(topics, key=lambda the_topics: the_topics.vote_count, reverse=True)
    count = 1
    await ctx.send(f"Topic #, Title,  # of votes")
    for t in topics_by_vote:
        t.display_id = count
        await ctx.send(f"{t.display_id}) {t.title}: {t.vote_count}")
        count = count + 1


@bot.command(aliases=['what'])
async def what_is_lean_coffee(ctx):
    async with ctx.channel.typing():
        await ctx.send(
            f"TL/DR Lean Coffee is a structured yet agendaless meeting where topics are driven by it's participants.")
        await ctx.send(f"For more info and history check out http://leancoffee.org/")


@bot.command(aliases=['how'])
async def how_does_it_work(ctx):
    async with ctx.channel.typing():
        await ctx.send(f"Relax Lean Robin will guide you through a session!")
        await asyncio.sleep(1)
        await ctx.send(f"First you will add topics you wish to talk about")
        await asyncio.sleep(1)
        await ctx.send(f"Next you will vote on which topics interest you most!")
        await asyncio.sleep(1)
        await ctx.send(
            f"Finally you'll start discussing a topic for usually about 3 mins. After which you will all vote "
            f"on whether to continue for another 1-3 mins or move onto the next topic")


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    ctx = await bot.get_context(message)

    if message.content.startswith('Ready to vote'):
        async with ctx.channel.typing():
            await ctx.send('Great! Here are all the topics:')
            await ctx.send('You can vote by clicking on the emoji')
            await ctx.send('When finished you can say "All done voting" or !results')
            await vote(ctx)
    if message.content.startswith('All done voting'):
        async with ctx.channel.typing():
            await ctx.send('Great! Here are the results...')
            await display_results_manual(ctx)
            await ctx.send("I'll start the highest voted topic")
            await start_topic(ctx, 1)
    if message.content.startswith('Yes'):
        await start_topic(ctx, 1)

    await bot.process_commands(message)


@bot.command(aliases=['start'])
async def start_a_lean_coffee_session(ctx):
    topic_service.clear()
    async with ctx.channel.typing():
        await ctx.send(f"Welcome to Lean Robin's Lean Coffee session!")
        await asyncio.sleep(1)

    async with ctx.channel.typing():
        await ctx.send(f"Let's start by adding some topics for our conversation!")
        await asyncio.sleep(1)
        await ctx.send(f"You can add topics using:")
        await asyncio.sleep(1)
        await ctx.send(f"!add_topic <some_topic_name>")
        await asyncio.sleep(1)
        await ctx.send(f"When you are all done adding topics just say \"Ready to vote\"")


@bot.command(alias=['vote'])
async def vote(ctx):
    await ctx.send(f"Now that everyone has had time to enter topics it's time to vote!")
    await ctx.send(f"Here are the entered topics:")
    await list_topics_manual(ctx)
    await ctx.send(f"If you'd like I can start a timer for you using:")
    await ctx.send(f"!countdown <number of seconds>")
    await ctx.send(f"When you are done voting just let me know by saying \"All done voting\"")


@bot.command()
async def dump_topics(ctx):
    topics = topic_service.all()

    for t in topics:
        await ctx.send(json.dumps(t.__dict__))


@bot.command()
async def call_vote(ctx):
    msg = await ctx.send("Continue talking about the current topic?")
    await msg.add_reaction(THUMBS_UP)
    await msg.add_reaction(THUMBS_DOWN)
#    print(f"msg id: {msg.id}")
    return msg.id


@bot.command()
async def process_vote(ctx, arg):
    msg = await ctx.fetch_message(arg)
    up_count = get_count_for_emoji(msg, THUMBS_UP)
    down_count = get_count_for_emoji(msg, THUMBS_DOWN)
    await ctx.send(f"👍: {up_count}")
    await ctx.send(f"👎: {down_count}")
    if up_count < down_count:
        await ctx.send(f"Alright next topic!")
        return False
    else:
        await ctx.send(f"Continue the conversation...")
        return True


@bot.command()
async def msg_info(ctx, arg):
    msg = await ctx.fetch_message(arg)
    for x in msg.reactions:
        await ctx.send(f"reaction: {x.emoji} count: {x.count}")


if __name__ == '__main__':
    discord_utils.output(f"Starting bot: {bot_config.bot_name}")
    discord_utils.output(f"Entering guild: {bot_config.guild_name}")
    STARTED_AT = datetime.now()

    bot.run(bot_config.discord_token)
