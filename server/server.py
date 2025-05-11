from Embedding import chromaDB_initialize, embedding_generate, retrieve_advices
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from enum import Enum
from typing import List

router = APIRouter()

class TaskType(str, Enum):
    legal_statute_search = "legal_statute_search"
    similar_case_retrieval = "similar_case_retrieval"
    general_answer = "general_answer"

@router.get("/check_server_status")
def test():
    return JSONResponse(content={"success": "true", "message": "API is up and running"})

@router.get("/generate_text")
def receive_query(
    task: List[TaskType] = Query(..., description="List of tasks to perform"),
    input_string: str = Query(..., description="User's query string")
):

    output_string = f"Received query: '{input_string}' with tasks: {[t.value for t in task]}"
    
    # RAG
    # most_relevant_document = retrieve_advices(input_string)
    
    return JSONResponse(content={"result": output_string})