import os
from openai import OpenAI

class Chat(object):
    MODEL = "gpt-3.5-turbo"

    def __init__(self):
        self.openai_client = None

    def create_system_message(self, context_info):
        # context_info is a series of tuples where each tuple is a pinecone result
        # (content, url), (content, url), (content, url)
        context = "\n".join([f"{i + 1}. {info[0]} ({info[1]})" for i, info in enumerate(context_info)])
        instructions = (
            "When answering the user's question, if you use any information from the provided context, "
            "please include the corresponding URL(s) at the end of your answer under a 'References' section."
            "The urls you should use are right after the provided context and look like jen.com."
            "If the provided context was not helpful please response with the message [None]"
        )
        return {"role": "system", "content": f"{instructions}\n\n{context}"}

    # this is the user's question
    def create_user_message(self, content):
        return {"role": "user", "content": f"{content}"}

    async def submit(self, question, search_results):
        client = self.__get_client()
        messages = [self.create_system_message(search_results), self.create_user_message(question)]

        completion = client.chat.completions.create(
            model=self.MODEL,
            messages=messages
        )

        print(dir(completion.choices[0]))

        message = completion.choices[0].message
        content = message.content

        return content


    def __get_client(self):
        if self.openai_client is None:
            key = os.environ.get('OPENAI_API_KEY')
            if key is None:
                raise Exception("Missing openai api key")

            org_id = os.environ.get('OPENAI_ORG_ID')
            if org_id is None:
                raise Exception("Missing openai api key")

            self.openai_client = OpenAI(api_key=key, organization=org_id)

        return self.openai_client

