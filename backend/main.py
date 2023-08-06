from fastapi import FastAPI, Query, status

from backend.qa import compose_answer, vectorize_url_content

app = FastAPI()


@app.get("/api/v1/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Load url and then ask some questions based on its content"}


@app.get("/api/v1/load-url", status_code=status.HTTP_204_NO_CONTENT)
def load_url(url: str = Query(..., description="load url content")):
    vectorize_url_content(url)


@app.get("/api/v1/ask", status_code=status.HTTP_200_OK)
def ask(question: str = Query(..., description="question u would like to ask")):
    answer = compose_answer(question)

    return {"answer": answer}
