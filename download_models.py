import os
from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer

def download_all_models():
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError("CRITICAL ERROR: HF_TOKEN environment variable is missing during build.")

    print("Initiating download for Mistral-7B weights...")
    # Downloads weights to the Docker image cache
    snapshot_download(repo_id="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)

    print("Initiating download for Sentence Transformer embeddings...")
    SentenceTransformer('all-MiniLM-L6-v2')

    print("All models successfully cached in the Docker image.")

if __name__ == "__main__":
    download_all_models()