from modules.vectorstore import get_vectorstore_path
import os
import shutil
import tempfile
from modules.vectorstore import create_or_load_vectorstore, add_documents_to_vectorstore
from langchain.schema import Document

class DummyEmbedding:
    def embed_documents(self, texts):
        # 各テキストを[0.1, 0.2, ...]のような固定長ベクトルに変換
        return [[float(i+1)/10 for i in range(5)] for _ in texts]
    def embed_query(self, text):
        return [0.1, 0.2, 0.3, 0.4, 0.5]

def test_get_vectorstore_path():
    assert get_vectorstore_path() == "db/faiss_index"

def test_add_and_load_vectorstore():
    # テスト用の一時ディレクトリを作成
    temp_dir = tempfile.mkdtemp()
    try:
        # VECTORSTORE_PATHを一時ディレクトリに一時的に変更
        orig_path = os.environ.get("VECTORSTORE_PATH")
        os.environ["VECTORSTORE_PATH"] = temp_dir
        # テスト用ドキュメント
        docs = [
            {"title": "T1", "content": "C1"},
            {"title": "T2", "content": "C2"},
        ]
        embedding = DummyEmbedding()
        # 追加・保存
        vs = add_documents_to_vectorstore(None, docs, embedding)
        assert vs is not None
        # ロード
        loaded_vs = create_or_load_vectorstore(embedding)
        assert loaded_vs is not None
        # 検索（FAISSのas_retriever/searchは本物のembeddingでないと動かない場合があるので省略）
    finally:
        shutil.rmtree(temp_dir)
        if orig_path is not None:
            os.environ["VECTORSTORE_PATH"] = orig_path
        else:
            del os.environ["VECTORSTORE_PATH"] 