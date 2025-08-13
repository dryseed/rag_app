
def validate_metadata(meta):
	"""
	メタデータの標準化・バリデーション。欠損値にはデフォルト値を設定。
	"""
	return {
		"title": meta.get("title", "N/A"),
		"category": meta.get("category", "N/A"),
		"tag": meta.get("tag", "N/A"),
		"source": meta.get("source", "N/A"),
	}

def filter_docs(docs, tags_filter, categories_filter):
	"""
	タグ・カテゴリによるドキュメントフィルタリング。
	"""
	filtered = []
	for doc in docs:
		meta = doc["metadata"] if isinstance(doc, dict) else doc.metadata
		if (not tags_filter or meta.get("tag") in tags_filter) and \
		   (not categories_filter or meta.get("category") in categories_filter):
			filtered.append(doc)
	return filtered

def check_file_size(uploaded_file, max_size_mb=20):
	"""
	ファイルサイズが上限を超えていないかチェック。
	"""
	if uploaded_file.size > max_size_mb * 1024 * 1024:
		return False
	return True

def add_query_history(session_state, query):
	"""
	検索履歴をセッションに追加。
	"""
	if "history" not in session_state:
		session_state["history"] = []
	session_state["history"].append(query)
