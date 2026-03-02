import json
import re
import os
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

app = FastAPI()

class AnalyzeRequest(BaseModel):
    prompt: str

knowledge_base = []
kb_embeddings = None
embedder = None
llm_pipeline = None

@app.on_event("startup")
def startup_event():
    """Server start hote hi 1 baar sab load hoga (Within 5 mins limit)"""
    global knowledge_base, kb_embeddings, embedder, llm_pipeline
    
    print("Loading Knowledge Base...")
    with open("ccpa_knowledge_base.json", "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)
    
    kb_texts = [item["content"] for item in knowledge_base]
    
    print("Loading Search Engine (Embedder)...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    kb_embeddings = embedder.encode(kb_texts, convert_to_tensor=True)
    
    print("Loading Mistral-7B LLM...")
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("WARNING: HF_TOKEN environment variable is not set!")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )
    
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        device_map="auto", 
        quantization_config=bnb_config, 
        token=hf_token
    )
    llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    print("System Ready! API is live.")

@app.get("/health")
def health_check():
    """Grading script check karegi ki server zinda hai ya nahi"""
    return {"status": "ok"}

@app.post("/analyze")
def analyze_prompt(request: AnalyzeRequest):
    user_prompt = request.prompt
    
    query_emb = embedder.encode(user_prompt, convert_to_tensor=True)
    hits = util.semantic_search(query_emb, kb_embeddings, top_k=2)[0]
    
    context = ""
    for hit in hits:
        item = knowledge_base[hit['corpus_id']]
        context += f"Section: {item['section']}\nRule: {item['content']}\n\n"
        
    system_prompt = f"""[INST] You are a strict legal AI evaluating CCPA compliance.
Analyze the business practice based ONLY on the provided CCPA laws context.
Return ONLY a valid JSON object. Do not output any other text, explanations, or markdown.

CCPA LAWS CONTEXT:
{context}

BUSINESS PRACTICE TO ANALYZE:
"{user_prompt}"

EXPECTED JSON FORMAT:
{{"harmful": true/false, "articles": ["<Insert EXACT Section heading from context here>"]}}

CRITICAL RULES:
1. If there is no violation, "articles" MUST be an empty list [].
2. Do NOT invent or modify section numbers. Copy the exact "Section:" string provided in the context above.
[/INST]
"""

    response = llm_pipeline(system_prompt, max_new_tokens=150, return_full_text=False)
    raw_output = response[0]['generated_text'].strip()
    
    try:
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if match:
            json_str = match.group()
            final_result = json.loads(json_str)
            
            if final_result.get("harmful") is False:
                final_result["articles"] = []
                
            return final_result
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        
    # Fallback response
    return {"harmful": False, "articles": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)