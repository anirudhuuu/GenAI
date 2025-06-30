from fastapi import FastAPI, Query, Path
from .queue.connection import queue
from .queue.worker import process_query

app = FastAPI()


@app.get("/")
def health():
    return {"status": "Server is up and running"}


@app.post("/chat")
def chat(query: str = Query(..., description="Chat message...")):
    # Take the query & push the query to queue
    # Internally calls as process_query(query)
    job = queue.enqueue(process_query, query)

    # Give a response to user about job received
    return {"status": "Queued", "job_id": job.id}


@app.get("/result/{job_id}")
def get_result(
    job_id: str = Path(..., description="Job ID...")
):
    job = queue.fetch_job(job_id=job_id)

    result = job.return_value()

    return {"result": result}
