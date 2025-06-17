import os
import json
import faiss
from sentence_transformers import SentenceTransformer
from document_loader import load_chunks_from_documents

DOCUMENTS_FOLDER = "data/documents"
INDEX_FOLDER = "data/index"
INDEX_PATH = os.path.join(INDEX_FOLDER, "index.faiss")
TEXTS_PATH = os.path.join(INDEX_FOLDER, "chunks.json")

# MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_NAME = "intfloat/multilingual-e5-base"

def build_index(chunks: list[str], model_name: str = MODEL_NAME):
    print("Загружаем модель...")
    model = SentenceTransformer(model_name)

    print("Векторизуем текстовые чанки...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    print("Создаем FAISS индекс...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print(f"Сохраняем индекс в {INDEX_PATH}")
    os.makedirs(INDEX_FOLDER, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    print(f"Сохраняем текстовые чанки в {TEXTS_PATH}")
    with open(TEXTS_PATH, "w", encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print("Индекс успешно создан!")

if __name__ == "__main__":
    print("Загружаем документы...")
    chunks = load_chunks_from_documents(DOCUMENTS_FOLDER)
    print(f"Найдено {len(chunks)} чанков текста")
    build_index(chunks)
