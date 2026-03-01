

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
from app.search_engine import search_sections
# from app.llm_engine import analyze_with_llm_model

app = FastAPI(title="Legal AI Backend")


class PromptRequest(BaseModel):
    prompt: str

    @validator("prompt")
    def validate_prompt(cls, value):
        if not value.strip():
            raise ValueError("Prompt cannot be empty")
        if len(value.strip()) < 5:
            raise ValueError("Prompt too short")
        return value


class AnalyzeResponse(BaseModel):
    harmful: bool
    articles: List[str]



@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: PromptRequest):

    try:
        sections = search_sections(request.prompt)

        return AnalyzeResponse(
            harmful=True if sections else False,
            articles=sections
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


# @app.post("/analyze-with-llm")
# def analyze_with_llm(request: PromptRequest):

#     try:
#         # Step 1: Retrieval
#         sections = search_sections(request.prompt)

#         # Step 2: Send to LLM
#         llm_response = analyze_with_llm_model(
#             prompt=request.prompt,
#             sections=sections
#         )

#         # Step 3: Ensure only JSON returned
#         return llm_response

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Internal Server Error: {str(e)}"
#         )