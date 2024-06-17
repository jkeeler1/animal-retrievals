import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from repository.search import Search
from service.vector import Vector
from service.chat import Chat

# Instantiate the services
app = FastAPI()
vector = Vector()
search = Search()
chat = Chat()


class UserChatQuestion(BaseModel):
    question: str
    chat_session_id: int

    @field_validator('question')
    @classmethod
    def question_validator(cls, v):
        if v is None or len(v) == 0 or len(v) > 2000:
            raise ValueError('invalid question')
        return v

    @field_validator('chat_session_id')
    @classmethod
    def chat_session_id_validator(cls, v):
        if v is None:
            raise ValueError('invalid chat session id')
        return v

@app.exception_handler(RequestValidationError)
async def exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()[0]['msg'],
                                  "custom msg": {"Invalid input"}}),
    )

class UserChatResponse(BaseModel):
    q: UserChatQuestion
    response: str


@app.post("/question/", response_model=UserChatResponse)
async def submit_question(user_question: UserChatQuestion) -> UserChatResponse:
    # get question as vector
    rst = await vector.embed(user_question.question)

    # search in pinecone data to get relevant data
    search_results = await search.query(rst)

    # submit to open-api
    chat_response = await chat.submit(user_question.question, search_results)
    return UserChatResponse(q=user_question, response=chat_response)


# This is used for debugging purposes
# Start this via the IDE debugger and then hit the endpoint with postman
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
