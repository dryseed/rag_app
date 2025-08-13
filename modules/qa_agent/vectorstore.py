
import os
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.vectorstores.base import VectorStore

VECTORSTORE_PATH = "db/faiss_index/qa_index"

def get_vectorstore_path() -> str:
	return VECTORSTORE_PATH

def create_or_load_vectorstore(embedding) -> Optional[VectorStore]:
	path = get_vectorstore_path()
	index_file = os.path.join(path, "index.faiss")
	if os.path.exists(index_file):
		return FAISS.load_local(path, embedding, allow_dangerous_deserialization=True)
	else:
		return None

def add_documents_to_vectorstore(vs: Optional[VectorStore], docs: List[dict], embedding) -> VectorStore:
	langchain_docs = [
		Document(
			page_content=doc["content"],
			metadata={k: v for k, v in doc.items() if k != "content"}
		)
		for doc in docs
	]
	if vs is None:
		vs = FAISS.from_documents(langchain_docs, embedding)
	else:
		vs.add_documents(langchain_docs)

	vs.save_local(get_vectorstore_path())
	return vs
