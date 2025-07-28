import types
from modules.utils import validate_metadata, filter_docs, check_file_size, add_query_history

def test_validate_metadata():
    meta = {"title": "t", "category": "c", "tag": "tg", "source": "s"}
    assert validate_metadata(meta) == meta
    meta = {"title": "t"}
    assert validate_metadata(meta) == {"title": "t", "category": "N/A", "tag": "N/A", "source": "N/A"}

def test_filter_docs():
    docs = [
        {"metadata": {"tag": "A", "source": "S1"}},
        {"metadata": {"tag": "B", "source": "S2"}},
        {"metadata": {"tag": "A", "source": "S2"}},
    ]
    # タグAのみ
    filtered = filter_docs(docs, ["A"], [])
    assert len(filtered) == 2
    # ソースS2のみ
    filtered = filter_docs(docs, [], ["S2"])
    assert len(filtered) == 2
    # タグAかつソースS2
    filtered = filter_docs(docs, ["A"], ["S2"])
    assert len(filtered) == 1

def test_check_file_size():
    class DummyFile:
        def __init__(self, size):
            self.size = size
    assert check_file_size(DummyFile(1024 * 1024 * 2))  # 2MB
    assert not check_file_size(DummyFile(1024 * 1024 * 6))  # 6MB

def test_add_query_history():
    state = {}
    add_query_history(state, "Q1")
    add_query_history(state, "Q2")
    assert state["history"] == ["Q1", "Q2"] 