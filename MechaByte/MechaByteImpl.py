import json
import logging

import MechaByte.SentenceComparatorApi as sc


class MechaByteImpl:
    def __init__(self, bot, store):
        self.bot = bot
        self.store = store
        self.response_gen = sc.SentenceComparator(store)

    async def ask_impl(self, guild_id, question):
        try:
            response = await self.response_gen.get_response(guild_id, question)
            return response
        except Exception as e:
            logging.error(f"Error: {e}")
            return "Oops, something went wrong. Please try again later."

    def get_impl(self, guild_id):
        try:
            # Get all the questions and answers from the key-value store
            qa_data = self.store.get_all_keys(guild_id, "question")

            if len(qa_data) == 0:
                return "I haven't learned anything yet."

            response = "Here are all the questions and answers I know:\n"
            for key in qa_data:
                response += f"{key}\n"

            return response

        except Exception as e:
            logging.error(f"Error: {e}")
            return "Oops, something went wrong. Please try again later."

    def add_impl(self, guild_id, qa_string):

        # Parse the question and answer from the message
        try:
            qa_data = json.loads(qa_string)
        except ValueError:
            return "Oops, I couldn't parse your question and answer. Please try again."

        try:
            # Store the question and answer in the key-value store
            for key, value in qa_data.items():
                self.store.set(guild_id, "question", key, value)

            return "Successfully added question to my knowledge base."
        except Exception as e:
            logging.error(f"Error: {e}")
            return "Oops, something went wrong. Please try again later."

    def delete_impl(self, guild_id, question):
        try:
            # Delete the question and answer from the key-value store
            result = self.store.delete(guild_id, question)
            if result:
                response = "Successfully deleted question from my knowledge base."
            else:
                response = "I don't know that question. I have not removed anything from my knowledge base."
            return response
        except Exception as e:
            logging.error(f"Error: {e}")
            return"Oops, something went wrong. Please try again later."