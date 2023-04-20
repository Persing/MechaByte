import requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": "Bearer ***REMOVED***"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class SentenceComparator:
    def __init__(self, sentence_key_store):
        self.store = sentence_key_store

    async def get_response(self, question):
        print(f"Generating response to: {question}")
        questions = self.store.get_all_keys()
        output = query({
            "inputs": {
                "source_sentence": question,
                "sentences": questions,
            },
        })
        # get the max index
        print(output)
        max_index = output.index(max(output))
        return self.store.get(questions[max_index])
