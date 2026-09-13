import os
import re
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
from knowledge_base.kb_documents import KB_DOCUMENTS

MODEL_NAME = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)


def chunk_fixed_size(text: str, chunk_size: int = 150, overlap: int = 40) -> List[str]:
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def chunk_sentence_based(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]


def build_vector_stores(db_dir: str = "./chroma_db") -> Dict[str, Any]:
    client = chromadb.PersistentClient(path=db_dir)
    
    # Collection 1: Fixed-Size Chunks
    fixed_collection = client.get_or_create_collection(
        name="nykaa_kb_fixed",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Collection 2: Sentence-Based Chunks
    sentence_collection = client.get_or_create_collection(
        name="nykaa_kb_sentence",
        metadata={"hnsw:space": "cosine"}
    )

    fixed_docs, fixed_ids, fixed_metadatas = [], [], []
    sentence_docs, sentence_ids, sentence_metadatas = [], [], []

    for doc in KB_DOCUMENTS:
        doc_id = doc["doc_id"]
        topic = doc["topic"]
        content = doc["content"]

        # 1. Fixed-size chunking
        f_chunks = chunk_fixed_size(content, chunk_size=150, overlap=40)
        for idx, chunk in enumerate(f_chunks):
            cid = f"{doc_id}_fixed_{idx}"
            fixed_ids.append(cid)
            fixed_docs.append(chunk)
            fixed_metadatas.append({
                "doc_id": doc_id,
                "topic": topic,
                "chunk_id": cid,
                "strategy": "fixed_size"
            })

        # 2. Sentence-based chunking
        s_chunks = chunk_sentence_based(content)
        for idx, chunk in enumerate(s_chunks):
            cid = f"{doc_id}_sent_{idx}"
            sentence_ids.append(cid)
            sentence_docs.append(chunk)
            sentence_metadatas.append({
                "doc_id": doc_id,
                "topic": topic,
                "chunk_id": cid,
                "strategy": "sentence_based"
            })

    # Embed and populate Fixed Collection
    if fixed_docs and fixed_collection.count() == 0:
        fixed_embeddings = embedding_model.encode(fixed_docs).tolist()
        fixed_collection.add(
            ids=fixed_ids,
            documents=fixed_docs,
            embeddings=fixed_embeddings,
            metadatas=fixed_metadatas
        )

    # Embed and populate Sentence Collection
    if sentence_docs and sentence_collection.count() == 0:
        sentence_embeddings = embedding_model.encode(sentence_docs).tolist()
        sentence_collection.add(
            ids=sentence_ids,
            documents=sentence_docs,
            embeddings=sentence_embeddings,
            metadatas=sentence_metadatas
        )

    return {
        "fixed_collection": fixed_collection,
        "sentence_collection": sentence_collection
    }


def query_vector_store(collection, query_text: str, top_k: int = 3) -> Dict[str, Any]:
    query_embedding = embedding_model.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    return results


if __name__ == "__main__":
    stores = build_vector_stores()
    fixed_coll = stores["fixed_collection"]
    sent_coll = stores["sentence_collection"]

    print(f"Fixed Collection count: {fixed_coll.count()} chunks")
    print(f"Sentence Collection count: {sent_coll.count()} chunks")

    sample_query = "What is the return window for makeup items?"
    
    print("\n--- Testing Fixed-Size Collection Retrieval ---")
    fixed_res = query_vector_store(fixed_coll, sample_query, top_k=2)
    for doc, meta, dist in zip(fixed_res["documents"][0], fixed_res["metadatas"][0], fixed_res["distances"][0]):
        cosine_sim = 1.0 - dist
        print(f"[{meta['doc_id']}] Similarity: {cosine_sim:.4f} | Chunk: {doc}")

    print("\n--- Testing Sentence-Based Collection Retrieval ---")
    sent_res = query_vector_store(sent_coll, sample_query, top_k=2)
    for doc, meta, dist in zip(sent_res["documents"][0], sent_res["metadatas"][0], sent_res["distances"][0]):
        cosine_sim = 1.0 - dist
        print(f"[{meta['doc_id']}] Similarity: {cosine_sim:.4f} | Chunk: {doc}")