import os
from docx import Document
from PyPDF2 import PdfReader

def extract_text_from_docx(folder_path: str) -> str:
    """
    Извлекает текст из всех файлов .docx методической базы
    :param folder_path: путь к папке с файлами для векторизации
    :return: полный текст всех файлов
    """
    all_text = []
    for filename in os.listdir(folder_path):
        if ".docx" in filename:
            path = os.path.join(folder_path, filename)
            doc = Document(path)
            for paragraph in doc.paragraphs:
                all_text.append(paragraph.text)
    return "\n".join(all_text)

def extract_text_from_pdf(folder_path: str) -> str:
    """
    Извлекает текст из всех файлов .pdf методической базы
    :param folder_path: путь к папке с файлами для векторизации
    :return: полный текст всех файлов
    """
    all_text = ""
    for filename in os.listdir(folder_path):
        if ".pdf" in filename:
            path = os.path.join(folder_path, filename)
            reader = PdfReader(path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text + '\n'
    return all_text

def split_text(text: str, max_length: int = 700, overlap: int = 100) -> list[str]:
    """
    Разбивает текст на чанки с перекрытием
    :param text: исходный текст
    :param max_length: максимальная длина чанка
    :param overlap: размер перекрытия
    :return: список чанков
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += max_length - overlap
    return chunks

def load_chunks_from_documents(folder_path: str) -> list[str]:
    """
    Читает все файлы и разбивает на чанки
    :param folder_path: путь к папке с файлами
    :return: список чанков
    """
    full_text_from_pdf = extract_text_from_pdf(folder_path)
    full_text_from_docx = extract_text_from_docx(folder_path)
    full_text = full_text_from_pdf + full_text_from_docx
    return split_text(full_text, max_length=500, overlap=150)
