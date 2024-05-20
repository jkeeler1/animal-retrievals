from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserChatQuestion(BaseModel):
    chatSession: int
    question: str


class UserChatResponse(BaseModel):
    q: UserChatQuestion
    response: str


@app.post("/question/", response_model=UserChatResponse)
async def submit_question(user_question: UserChatQuestion) -> UserChatResponse:
    // embed the question and get the pinecone response
    // ask openai the question and include the pinecone text and urls
    // return openai response
    return UserChatResponse(q=user_question, response="jen was here")
