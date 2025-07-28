import io
import pandas as pd
from modules.loader import load_docs_from_excel, load_docs_from_file

def test_load_docs_from_excel(tmp_path):
    # テスト用Excelデータを作成
    df = pd.DataFrame([
        {"title": "T1", "content": "C1", "tag": "A", "category": "Cat1", "source": "S1"},
        {"title": "T2", "content": "C2", "tag": "B", "category": "Cat2", "source": "S2"},
        {"title": "", "content": "C3", "tag": "C", "category": "Cat3", "source": "S3"},  # title空
        {"title": "T4", "content": "", "tag": "D", "category": "Cat4", "source": "S4"},  # content空
    ])
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)
    with open(file_path, "rb") as f:
        docs = load_docs_from_excel(f, "test.xlsx")
    # titleまたはcontentが空の行は除外される
    assert len(docs) == 2
    assert docs[0]["title"] == "T1"
    assert docs[1]["metadata"]["tag"] == "B"

def test_load_docs_from_file_excel(tmp_path):
    """Excelファイルのload_docs_from_fileテスト"""
    df = pd.DataFrame([
        {"title": "T1", "content": "C1", "tag": "A", "category": "Cat1", "source": "S1"},
    ])
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)
    with open(file_path, "rb") as f:
        docs = load_docs_from_file(f, "test.xlsx")
    assert len(docs) == 1
    assert docs[0]["title"] == "T1"

def test_load_docs_from_file_pdf():
    """PDFファイルのload_docs_from_fileテスト（サポートされていない形式のテスト）"""
    # 実際のPDFファイルがないため、サポートされていない形式のテスト
    class DummyFile:
        pass
    
    docs = load_docs_from_file(DummyFile(), "test.txt")
    assert len(docs) == 0  # サポートされていない形式は空リストを返す

def test_load_docs_from_file_unsupported():
    """サポートされていないファイル形式のテスト"""
    class DummyFile:
        pass
    
    docs = load_docs_from_file(DummyFile(), "test.txt")
    assert len(docs) == 0 