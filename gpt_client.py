import os
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()
GIGACHAT_TOKEN = os.getenv("GIGACHAT_API_KEY")

giga = GigaChat(credentials=GIGACHAT_TOKEN,
                ca_bundle_file='certs/russian_trusted_root_ca.cer',
                ) # model='GigaChat-Max'

SYSTEM_PROMPT = (
        "Ты — эксперт по системе менеджмента качества. "
        "Отвечай строго на основе представленного контекста. "
        "но **не упоминай слово «контекст» и не ссылайся на его номера**. "
        "Если ответа нет в контексте, скажи: 'Информация отсутствует в базе знаний.'"
)

def ask_gigachat(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(f"{i + 1}. {c}" for i, c in enumerate(context_chunks))
    user_prompt = SYSTEM_PROMPT + f"Контекст:\n{context}\n\nВопрос: {question}"
    print(user_prompt)
    try:
        resp = giga.chat(user_prompt)
        return resp.choices[0].message.content
    except Exception as e:
        return  f"Ошибка при запросе к GigaChat: {e}"