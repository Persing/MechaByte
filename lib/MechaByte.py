import json

import discord
from discord.ext import commands
from discord.ext.commands import bot

import sen_cmp_api as sc


class MechaByte:
    def __init__(self, store, discord_token, openai):
        self.store = store
        self.discord_token = discord_token
        self.openai = openai
        self.response_gen = sc.SentenceComparator(store)

        # Set up Discord bot
        intents = discord.Intents.all()
        # intents.messages = True
        self.bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # If the message is from the bot itself, ignore it.
        if message.author == self.bot.user:
            return

        print(f"Received message from {message.author}: {message.content}")

    # Define a helper function for generating sarcastic responses
    async def generate_sarcastic_response(self, prompt):
        print(f"Generating response to: {prompt}")
        response = self.openai.Completion.create(
            model="text-davinci-003",
            prompt="Marv is a chatbot that reluctantly answers questions with sarcastic and witty responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\nYou: " + prompt + "\nMarv:",
            temperature=0.5,
            max_tokens=60,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )

        return response.choices[0].text.strip()

    # Define the bot command
    @commands.command(name='ask', help='Ask the bot a question and it will respond sarcastically.')
    async def ask(self, ctx, *, question):
        print(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            response = await self.response_gen.generate_sarcastic_response(question)
            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @commands.command(name='re', help='Get help from the bot.')
    async def re(self, ctx, *, question):
        print(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            response = await self.response_gen.get_response(question)
            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @bot.command(name='help', help='Get help from the bot.')
    async def help(self, ctx):
        print(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            response = "I am a bot that can answer your questions. Use '!re' at the start of your message to get a response. More features coming soon! In the meantime, you can check the pinned comments in this thread for a lot of helpful info."
            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @bot.command(name='add', help='Set a Question Answer pair for the bot.')
    async def add(self, ctx, *, qa_string):
        print(f"Received command from {ctx.author}: {ctx.message.content}")

        # Parse the question and answer from the message
        try:
            qa_data = json.loads(qa_string)
        except ValueError:
            await ctx.send("Oops, I couldn't parse your question and answer. Please try again.")
            return

        try:
            # Store the question and answer in the key-value store
            for key, value in qa_data.items():
                self.store.set(key, value)

            response = "Successfully added question to my knowledge base."
            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @bot.command(name='get', help='Get a Question Answer pair from the bot.')
    async def get_all(self, ctx):
        print(f"Received command from {ctx.author}: {ctx.message.content}")

        try:
            # Get all the questions and answers from the key-value store
            qa_data = self.store.get_all_keys()

            response = "Here are all the questions and answers I know:\n"
            for key in qa_data:
                response += f"{key}\n"

            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @bot.command(name='delete', help='Delete a Question Answer pair from the knowledge base.')
    async def delete(self, ctx, *, question):
        print(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            # Delete the question and answer from the key-value store
            result = self.store.delete(question)
            if result:
                response = "Successfully deleted question from my knowledge base."
            else:
                response = "I don't know that question. I have not removed anything from my knowledge base."
            await ctx.send(response)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @bot.command(name='clear', help='Clear the knowledge base.')
    async def clear(self, ctx):
        print(f"Received command from {ctx.author}: {ctx.message.content}")
        try:
            # Prompt the user for confirmation
            response = "Are you sure you want to clear my knowledge base? This action cannot be undone. Reply 'yes' to confirm, or anything else to cancel."
            await ctx.send(response)

            # Wait for the user's response
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await self.bot.wait_for('message', check=check)

            if msg.content.lower() == 'yes':
                # Clear the key-value store
                self.store.clear()

                response = "Successfully cleared my knowledge base."
                await ctx.send(response)
            else:
                response = "Okay, I will not clear my knowledge base."
                await ctx.send(response)

        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Oops, something went wrong. Please try again later.")

    @bot.event
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
