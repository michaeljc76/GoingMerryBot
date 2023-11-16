import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import responses
import os

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
openai.api_key = os.getenv('AI_KEY')


class Bot(discord.Client):
    async def on_ready(self):
        print(f'{self.user.name} is now running')

    async def on_message(self, message):
        print(f'{message.author} said: "{message.content}" ({message.channel})')

        if message.author == self.user:
            return
        
        command, user_message = None, None

        # determine_text_appropriateness(message.content):

        
        if message.content.startswith('!ai'):
            command = message.content.split(' ')[0]
            user_message = message.content.replace('!ai', '')
            print(command, user_message)

        if(user_message == ""):
            await message.channel.send("Please provide a prompt after !ai")
        elif command == '!ai':
            response = await generate_ai_response(prompt=user_message)
            await message.channel.send(response)

        if message.content.startswith('!translate'):
            command = message.content.split(' ')[0]
            user_message = message.content.replace('!translate', '')
            print(command, user_message)

        if(user_message == ""):
            await message.channel.send("Please provide a message after !translate")
        elif command == '!translate':
            translate_prompt = ("Translate the following text to English, only send the traslation:" + user_message)
            response = await generate_ai_response(prompt=translate_prompt)
            await message.channel.send(response)

        # if await determine_text_appropriateness(message.content):
        #     await message.delete()
        #     await message.author.send("Your message was inappropriate. Please refrain from sending inappropriate messages.")
        

# OPENAI API METHODS

async def generate_ai_response(prompt):
    try:
        # Use OpenAI API to generate a response
        response = openai.completions.create(
            model="text-davinci-003",
            temperature=0.7,
            max_tokens=150,
            prompt=prompt,
        )

        response_dict = response.choices
        if response_dict and len(response_dict) > 0:
            prompt_response = response_dict[0].text
        return prompt_response

    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "An error occurred while generating the response."

intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
    
#         # [TODO]: IF THE MESSAGE IS INAPPROPRIATE, THEN ADD THE POINTS TO A GRAPH FOR EACH USER