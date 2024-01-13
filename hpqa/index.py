from pathlib import Path
from typing import Union

from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores.faiss import FAISS

from . import preproc

__all__ = ["build_document_store", "load_document_store"]


def build_document_store(
    index_save_path: Union[str, Path], chunk_size: int = 500, chunk_overlap: int = 10, overwrite: bool = False
) -> FAISS:
    index_save_path = Path(index_save_path)

    if index_save_path.exists() and not overwrite:
        raise Exception(f"{index_save_path} already exists. Set overwrite=True to overwrite.")

    docs = []
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    for book_number in range(1, 8):
        chapters = preproc.get_book_chapters(book_number)
        text_list = list(chapters.values())
        metadata_list = [{"book": book_number, "chapter": name} for name in chapters.keys()]
        docs.extend(text_splitter.create_documents(texts=text_list, metadatas=metadata_list))

    embeddings = OpenAIEmbeddings()
    print(f"Embedding {len(docs)} documents...")
    document_store = FAISS.from_documents(docs, embeddings)
    print(f"Saving index at {index_save_path}")
    document_store.save_local(index_save_path)

    return document_store


def load_document_store(path: Union[str, Path], openai_api_key=None) -> FAISS:
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    document_store = FAISS.load_local(path, embeddings)
    return document_store
