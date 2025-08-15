from modules.agents.base import BaseAgent
from modules.api_agent.loader import extract_markdown_sections_from_apidoc
from modules.api_agent.vectorstore import create_or_load_vectorstore
from modules.common.embedding_model import get_embedding

class APIAgent(BaseAgent):
    def __init__(self):
        self.embedding = get_embedding()
        self.vs = create_or_load_vectorstore(self.embedding)
    def search(self, query: str) -> str:
        retriever = self.vs.as_retriever(search_kwargs={"k": 10})
        results = retriever.invoke(query)
        return "\n".join([doc.page_content for doc in results])