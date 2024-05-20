# animal-retrievals
Playing with open-api and pinecone to generate answers to questions

# Installation:
pip3 install fastapi

# To run:
fastapi dev main.py (dev mode)

# Local testing
`curl --location 'http://127.0.0.1:8000/question/' \
--header 'Content-Type: application/json' \
--data '{
    "question": "Give me a paragraph on sea animals?",
    "chatSession": 123`

# Swagger Docs
http://127.0.0.1:8000/docs
