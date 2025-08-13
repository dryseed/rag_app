
import os
import sqlite3
from datetime import datetime, timezone
from typing import List, Optional, Dict
from modules.common import utils
from modules.common import embedding_model

DB_PATH = 'db/qa_knowledge.db'

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS qa_knowledge (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT,
	category TEXT,
	tag TEXT,
	content TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE(title, category, tag)
);
'''

def init_db():
	with sqlite3.connect(DB_PATH) as conn:
		conn.execute(CREATE_TABLE_SQL)
		conn.commit()

def upsert_qa(title: str, category: str, tag: str, content: str) -> None:
	now = datetime.now(timezone.utc).isoformat()
	with sqlite3.connect(DB_PATH) as conn:
		cur = conn.cursor()
		cur.execute("""
			SELECT id FROM qa_knowledge WHERE title=? AND category=? AND tag=?
		""", (title, category, tag))
		row = cur.fetchone()
		if row:
			cur.execute("""
				UPDATE qa_knowledge
				SET content=?, updated_at=?
				WHERE title=? AND category=? AND tag=?
			""", (content, now, title, category, tag))
		else:
			cur.execute("""
				INSERT INTO qa_knowledge (title, category, tag, content, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?)
			""", (title, category, tag, content, now, now))
		conn.commit()

def load_all_qa() -> List[Dict]:
	with sqlite3.connect(DB_PATH) as conn:
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		cur.execute("SELECT * FROM qa_knowledge ORDER BY updated_at DESC, created_at DESC")
		rows = cur.fetchall()
		return [dict(row) for row in rows]

def update_qa_by_id(id: int, content: str) -> None:
	now = datetime.now(timezone.utc).isoformat()
	with sqlite3.connect(DB_PATH) as conn:
		conn.execute(
			"UPDATE qa_knowledge SET content=?, updated_at=? WHERE id=?",
			(content, now, id)
		)
		conn.commit()

def delete_qa_by_id(id: int) -> None:
	with sqlite3.connect(DB_PATH) as conn:
		conn.execute("DELETE FROM qa_knowledge WHERE id=?", (id,))
		conn.commit()
