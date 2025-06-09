import json
import faiss
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/index/index.faiss"
CHUNKS_PATH = "data/index/chunks.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

TOP_K = 3

class Retriever:
    def __init__(self, index_path: str = INDEX_PATH, chunks_path: str = CHUNKS_PATH, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

        print("Загрузка FAISS-индекса...")
        self.index = faiss.read_index(index_path)

        print("Загрузка чанков...")
        with open(chunks_path, "r", encoding='utf-8') as f:
            self.chunks = json.load(f)

    def search(self, query: str, top_k: int = TOP_K) -> list[tuple[str, float]]:
        """
        Возвращает top_k самых подходящих по смыслу чанков вместе с расстоянием
        :param query: вопрос пользователя
        :param top_k: количество чанков, которые добавятся в запрос
        :return: список кортежей вида (чанк, расстояние)
        """
        query_vec = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)

        result = []
        for idx, dist in zip(indices[0], distances[0]):
            if 0 <= idx < len(self.chunks):
                result.append((self.chunks[idx], dist))

        return result