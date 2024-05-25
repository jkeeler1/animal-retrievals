import os

from openai import OpenAI


class Vector(object):
    MODEL = "text-embedding-ada-002"

    def __init__(self):
        self.openaiClient = None

    # given a value, get the embedding for the value
    def embed(self, val):
      client = self.__get_client()
      response = client.embeddings.create(
        input=val,
        model=self.MODEL
      )
      return response.data[0].embedding

    # instantiate an openai client
    def __get_client(self):
        if self.openaiClient is None:
            key = os.environ.get('OPENAI_API_KEY')
            if key is None:
                raise Exception("Missing openai api key")

            org_id = os.environ.get('OPENAI_ORG_ID')
            if org_id is None:
                raise Exception("Missing openai api key")

            self.openaiClient = OpenAI(api_key=key, organization=org_id)

        return self.openaiClient
