import chromadb
from chromadb.config import Settings
import pandas as pd
from transformers import AutoModel
import pandas as pd
import json
import lzma
from tqdm import tqdm
from openai import OpenAI

openai_client = OpenAI(api_key="")


def chromaDB_initialize():
    client = chromadb.PersistentClient(path="./ChromaDB", settings=Settings(allow_reset=True))
    exist_collections = False
    if "legalrag" in [c.name for c in client.list_collections()]:
        exist_collections = True
    collection = client.get_or_create_collection(name='legalrag', metadata={"hnsw:space": "cosine"})
    
    if exist_collections == False:
        file_path = "../data/xml.data.jsonl.xz"
        num = 0
        with lzma.open(file_path, "rt", encoding="utf-8") as file:
            print("Read file.....")
            
            for line in tqdm(file, desc="Processing records"):
                try:
                    record = json.loads(line.strip())
                    num = num + 1
                    #print(embedding_generate(record.get("casebody")['data']))
                    embedding = embedding_generate(record.get("casebody")['data'][:7000])
                    collection.add(
                        ids=[str(num)],
                        embeddings=embedding,
                        documents=[record.get("casebody")['data']],
                        metadatas=[{"state": "Illinois"}]
                    )
                
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {e}")
                
                if num == 100:
                    break
    print("Embedding Process end.....")              

    
def embedding_generate(content):
    
    response = openai_client.embeddings.create(
                input=content,
                model="text-embedding-3-small"
            )
    embedding = response.data[0].embedding

    return embedding

def retrieve_advices(query):
    # retrieve most relevant document
    
    client = chromadb.PersistentClient(path="./ChromaDB", settings=Settings(allow_reset=True))
    collection = client.get_or_create_collection(name='legalrag', metadata={"hnsw:space": "cosine"})
    
    # generate an embedding for the prompt and retrieve the most relevant doc
    embedding = embedding_generate(query)
    
    results = collection.query(
    query_embeddings=[embedding],
    n_results=1
    )
    
    data = results['documents'][0][0]
    
    
    
    return data





