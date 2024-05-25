from fastapi import FastAPI
from pydantic import BaseModel

from repository.search import Search
from service.vector import Vector

app = FastAPI()
vector = Vector()
search = Search()


class UserChatQuestion(BaseModel):
    chatSession: int
    question: str


class UserChatResponse(BaseModel):
    q: UserChatQuestion
    response: str


@app.post("/question/", response_model=UserChatResponse)
async def submit_question(user_question: UserChatQuestion) -> UserChatResponse:
    # get question as vector
    rst = vector.embed(user_question.question)
    print(rst)

    # search in pinecone data to get relevant data
    search_result = search.query(rst);

    # submit to open-api
    return UserChatResponse(q=user_question, response="jen was here")
