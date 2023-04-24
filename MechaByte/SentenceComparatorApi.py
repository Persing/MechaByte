import logging
import os

import requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class SentenceComparator:
    def __init__(self, sentence_key_store):
        self.store = sentence_key_store

    async def get_response(self, guild_id, question):
        logging.info(f"Generating response to: {question}")
        questions = self.store.get_all_keys(guild_id, "question")

        if len(questions) == 0:
            return "I haven't learned anything yet."

        # Check if any of the questions match exactly
        if question in questions:
            return self.store.get[guild_id]["question"][question]

        output = query({
            "inputs": {
                "source_sentence": question,
                "sentences": questions,
            },
        })

        # get the max index
        logging.debug(output)
        max_index = output.index(max(output))
        return self.store.get(guild_id, question, questions[max_index])
