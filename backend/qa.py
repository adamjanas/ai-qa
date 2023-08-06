import uuid

import openai
from langchain.text_splitter import CharacterTextSplitter
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct

from backend.scrap import parse_content_for_given_url
from backend.settings.base import COLLECTION_NAME, OPENAI_API_KEY, QDRANT_HOST, QDRANT_PORT

openai.api_key = OPENAI_API_KEY

connection = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
connection.recreate_collection(
    collection_name=COLLECTION_NAME, vectors_config=models.VectorParams(size=1500, distance=models.Distance.COSINE)
)


def vectorize_url_content(url: str):
    parsed_content = parse_content_for_given_url(url)
    chunks = get_text_chunks(parsed_content)
    points = get_embedding(chunks)
    insert_data(points)


# parse text into chunks
def get_text_chunks(text: str) -> list[str]:
    text_splitter = CharacterTextSplitter(
        separator="/n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks


# convert chunks into embeddings
def get_embedding(text_chunks: list[str], model_id: str = "text-embedding-ada-002") -> list[PointStruct]:
    points = []
    for chunk in text_chunks:
        response = openai.Embedding.create(input=chunk, model=model_id)
        embeddings = response["data"][0]["embedding"]
        point_id = str(uuid.uuid4())
        points.append(PointStruct(id=point_id, vector=embeddings, payload={"text": chunk}))
    return points


# data insertion to qdrant db
def insert_data(points: list[PointStruct]):
    connection.upsert(collection_name=COLLECTION_NAME, wait=True, points=points)


# searching and answering
def compose_answer(question: str) -> str:
    response = openai.Embedding.create(input=question, model="text-embedding-ada-002")
    embeddings = response["data"][0]["embedding"]
    search_result = connection.search(collection_name=COLLECTION_NAME, query_vector=embeddings, limit=1)
    prompt = "Context:\n"
    for result in search_result:
        prompt += f"{result.payload['text']} \n"
    prompt += f"Question: {question}"

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    return completion.choices[0].message.content
