from pathlib import Path
from typing import Tuple, Union

from haystack import Document
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever, PreProcessor

from . import preproc

__all__ = ["build_document_store", "load_document_store"]


def build_document_store(
    db_path: Union[str, Path], index_save_path: Union[str, Path], max_words_per_doc: int = 100, overwrite: bool = False
) -> Tuple[FAISSDocumentStore, EmbeddingRetriever]:
    index_save_path = Path(index_save_path)

    if index_save_path.exists() and not overwrite:
        raise Exception(f"Document store {index_save_path} already exists. Use overwrite = True to force overwrite.")

    sql_url = f"sqlite:///{str(Path(db_path))}"
    document_store = FAISSDocumentStore(sql_url=sql_url, faiss_index_factory_str="Flat", return_embedding=True)
    document_store.delete_documents()

    documents = []
    for book_number in range(1, 8):
        chapters = preproc.get_book_chapters(book_number)
        for chapter, text in chapters.items():
            documents.append(Document(content=text.strip(), meta=dict(book=book_number, chapter=chapter)))

    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_length=max_words_per_doc,
        split_respect_sentence_boundary=True,
        split_overlap=10,
    )

    docs_processed = preprocessor.process(documents)
    document_store.write_documents(docs_processed)

    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="flax-sentence-embeddings/all_datasets_v3_mpnet-base",
        model_format="sentence_transformers",
    )

    document_store.update_embeddings(retriever=retriever)
    document_store.save(index_save_path)
    return document_store, retriever


def load_document_store(path: Union[str, Path]) -> Tuple[FAISSDocumentStore, EmbeddingRetriever]:
    document_store = FAISSDocumentStore.load(path)
    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="flax-sentence-embeddings/all_datasets_v3_mpnet-base",
        model_format="sentence_transformers",
    )
    return document_store, retriever
