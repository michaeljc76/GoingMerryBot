import discord
from discord.ext import commands
import responses
import os
from dotenv import load_dotenv
import openai


load_dotenv()

TOKEN=os.getenv('BOT_TOKEN')

openai.api_key = os.getenv('AI_KEY')

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        result = client.determine_text_appropriateness(message)
        if result >= 7:
            await message.delete()
            await message.author.send("Your message was inappropriate. Please refrain from sending inappropriate messages.")
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if message.content.startswith('!'):
            command, *args = message.content[1:].split()
            if command == 'ai':
                gpt_response = client.get_chatgpt_response(args)
                message.send(gpt_response)

    @client.event
    async def determine_text_appropriateness(message):
        try:
            automod = ("Determine whether or not this post is appropriate for a kindergarten environment."
                    "If it is not, then determine a rating from 1-10 on how inappropriate it is."
                    "If it is beyond a 5, then we will delete the post and send a warning to the user."
                    "Restrict your message to ONLY an integer value from 1-10 if it's inappropriate."
                    "If the message IS appropriate, then return a 0."
                    "Here is the message in question: " + message.content)

            # [TODO]: IF THE MESSAGE IS INAPPROPRIATE, THEN ADD THE POINTS TO A GRAPH FOR EACH USER

            response = client.get_chatgpt_response(automod)
            print(response)
            return 1

        except Exception as e:
            print(e)

    @client.event
    async def get_chatgpt_response(args):
        if len(args) == 0:
            return "Please enter a message to generate a response."
        else:
            input_text = " ".join(args)

            # [TODO]: SAVE THIS INPUT MESSAGE TO THE GRAPH FOR EACH USER
            # [NOTE]: If there is aleady a message in the graph, then remove it and add the new one

            return client.generate_ai_response(input_text)
        
    @client.event
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

    client.run(TOKEN)

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)