import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from repository.search import Search
from service.vector import Vector
from service.chat import Chat

# Instantiate the services
app = FastAPI()
vector = Vector()
search = Search()
chat = Chat()

class UserChatQuestion(BaseModel):
    chat_session: int
    question: str


class UserChatResponse(BaseModel):
    q: UserChatQuestion
    response: str


@app.post("/question/", response_model=UserChatResponse)
async def submit_question(user_question: UserChatQuestion) -> UserChatResponse:
    # get question as vector
    rst = vector.embed(user_question.question)

    # search in pinecone data to get relevant data
    search_results = search.query(rst)

    # submit to open-api
    chat_response = chat.submit(user_question.question, search_results)
    return UserChatResponse(q=user_question, response=chat_response)

# This is used for debugging purposes
# Start this via the IDE debugger and then hit the endpoint with postman
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
