"""
    Murad:
    CHECK THE [TODO]: 's!!!!

    VERY IMPORTANT!!!!
"""

from sqlite3 import Error
from dotenv import load_dotenv
from db import db_connect

import sqlite3
import os
import discord
from discord.ext import commands
import openai

TOKEN = os.getenv('API_KEY')

# help commend prefix> !help
bot = commands.Bot(command_prefix='!')

@bot.command(name='help')
async def help_command(ctx):
    help_message = "Available commands:\n"
    for command in bot.commands:
        help_message += f"!{command.name}: {command.description}\n"
    await ctx.send(help_message)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')

    # Check if from bot
    if message.author == bot.user:
        return

    # Call determine_text_appropriateness only once
    result = await determine_text_appropriateness(message)

    if result != 0:
        # Delete message
        await message.delete()
        # Send warning to user
        await message.author.send("Your message was inappropriate. Please refrain from sending inappropriate messages.")

        return

    # [TODO]: ADD POINTS TO A GRAPH FOR EACH USER
    # [TODO]: INCREMENT 'amount_of_posts' FOR EACH USER

    channel_send = message.channel.name
    # [TODO]: SAVE THE CHANNEL NAME TO THE GRAPH FOR EACH USER
    # [NOTE]: If there is already a channel name in the graph, then remove it and add the new one

    # Check if the message starts with the ! prefix
    if message.content.startswith('!'):
        # Get the command and arguments
        command, *args = message.content[1:].split()
        if command == 'ai':
            gpt_response = await get_chatgpt_response(args)
            await message.channel.send(gpt_response)


# @bot.command(name='ai')
async def determine_text_appropriateness(message):
    try:
        automod = ("Determine whether or not this post is appropriate for a kindergarten environment."
                   "If it is not, then determine a rating from 1-10 on how inappropriate it is."
                   "If it is beyond a 5, then we will delete the post and send a warning to the user."
                   "Restrict your message to ONLY an integer value from 1-10 if it's inappropriate."
                   "If the message IS appropriate, then return a 0."
                   "Here is the message in question: " + message.content)

        # [TODO]: IF THE MESSAGE IS INAPPROPRIATE, THEN ADD THE POINTS TO A GRAPH FOR EACH USER

        response = await get_chatgpt_response(automod)
        print(response)
        return response

    except Exception as e:
        print(e)


# Translates text from one language to another using ChatGPT openAI
async def translate_text(message):
    try:
        translate_prompt = ("Translate the following text from its current language to English."
                            "Only send the translation, nothing else.: " + message.content)
        text_to_send = await get_chatgpt_response(translate_prompt)

        # Send message to chat
        await message.channel.send(text_to_send)

    except Exception as e:
        print(e)


async def get_chatgpt_response(args):
    if len(args) == 0:
        return "Please enter a message to generate a response."
    else:
        input_text = " ".join(args)

        # [TODO]: SAVE THIS INPUT MESSAGE TO THE GRAPH FOR EACH USER
        # [NOTE]: If there is already a message in the graph, then remove it and add the new one

        return generate_ai_response(input_text)


async def generate_ai_response(input_text):
    try:
        # Use OpenAI API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            temperature=0.7,
            max_tokens=150,
            n=1
        )

        return response.choices[0].text

    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "Sorry, an error occurred while generating the AI response."
