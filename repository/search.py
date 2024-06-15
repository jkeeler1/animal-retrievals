import os
from pinecone import Pinecone

class Search(object):


    def __init__(self):
        self.pinecone_client = None

    def query(self, v):
        client = self.__get_client()
        index = client.Index("animals")
        search_results = index.query(namespace="animals", vector=v, top_k=3, include_values=False, include_metadata=True)

        query_results = []
        for match in search_results.matches:
            metadata = match['metadata']
            query_results.append((metadata['chunk'], metadata['url']))

        return query_results

    def __get_client(self):
        if self.pinecone_client is None:
            key = os.environ.get('PINECONE_API_KEY')
            if key is None:
                raise Exception("Missing pinecone api key")

            self.pinecone_client = Pinecone(api_key=key)

        return self.pinecone_client