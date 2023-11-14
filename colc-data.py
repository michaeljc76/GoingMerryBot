import discord
import json
import matplotlib.pyplot as plt
from discord.ext import commands

# Discord Bot Setup
bot = commands.Bot(command_prefix='!')

user_data = {}  # Structure: { 'user_id': {'posts': 0, 'points': 0, 'violations': 0}, ... }

@bot.event
async def on_ready():
    global user_data
    print(f'We have logged in as {bot.user}')
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        print("Data file not found, starting fresh.")
        user_data = {}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    user_data.setdefault(user_id, {'posts': 0, 'points': 0, 'violations': 0})
    user_data[user_id]['posts'] += 1

    # Logic for points and violations goes here

    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

    await bot.process_commands(message)  # Important to allow command processing

# Command to Generate and Show Graph
@bot.command(name='graph', help='Generates a graph of user data')
async def graph(ctx):
    if not user_data:
        await ctx.send("No data available to generate graph.")
        return

    users = list(user_data.keys())
    posts = [user_data[user]['posts'] for user in users]
    points = [user_data[user]['points'] for user in users]
    violations = [user_data[user]['violations'] for user in users]

    x = range(len(users))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    ax.bar(x, posts, width, label='Posts')
    ax.bar([p + width for p in x], points, width, label='Points')
    ax.bar([p + width*2 for p in x], violations, width, label='Violations')

    ax.set_xlabel('Users')
    ax.set_ylabel('Counts')
    ax.set_title('User Activity on Discord')
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(users)
    ax.legend()

    plt.savefig('userActivities.png')
    plt.close(fig)

    await ctx.send(file=discord.File('userActivities.png'))

bot.run('OUR_BOT_TOKEN')
