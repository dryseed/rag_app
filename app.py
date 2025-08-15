# app.py
import os
import streamlit as st
import pandas as pd
import logging
import re
import json
from streamlit_option_menu import option_menu
from modules.qa_agent.loader import upsert_qa, init_db, load_all_qa
from modules.qa_agent.vectorstore import create_or_load_vectorstore as create_or_load_qa_vectorstore, add_documents_to_vectorstore as add_documents_to_qa_vectorstore
from modules.api_agent.loader import extract_sections_by_toc_template, summarize_api_sections_with_nlp, debug_word_structure, extract_markdown_sections_from_apidoc
from modules.api_agent.vectorstore import create_or_load_vectorstore as create_or_load_api_vectorstore, add_documents_to_vectorstore as add_documents_to_api_vectorstore
from modules.common.embedding_model import get_embedding
from modules.common.deepseek_api import ask_deepseek
from modules.common.utils import validate_metadata, filter_docs, check_file_size, add_query_history
# --- 対話（メタエージェントチャットUI） ---
from modules.agents.qa_agent import QAAgent
from modules.agents.api_agent import APIAgent
from modules.agents.meta_agent import MetaAgent


st.set_page_config(page_title="RAG with DeepSeek", layout="wide")

if not os.getenv("DEEPSEEK_API_KEY"):
    st.error("DEEPSEEK_API_KEYが設定されていません。.envファイルを確認してください。")
    st.stop()
DB_PATH = 'db/qa_knowledge.db'

# --- カスタムCSSで全体の雰囲気を調整 ---
st.markdown("""
    <style>
    .main {background-color: #f5f6fa;}
    .block-container {padding-top: 2rem;}
    .sidebar .sidebar-content {background: #fff;}
    .card {background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #e0e0e0; padding: 2rem; margin-bottom: 2rem;}
    .menu-title {font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# --- サイドバー ---
with st.sidebar:
    selected = option_menu(
        "MENU",
        ["対話", "QA 検索", "一括QA登録", "手動QA登録", "API仕様書登録", "API仕様書検索"],
        icons=["chat-dots","search", "cloud-upload", "pencil-square", "file-earmark-arrow-up", "file-text",],
        menu_icon="cast",
        default_index=0,
    )

# --- メインエリア ---
st.title("QA RAG（DeepSeek API）")
def remove_greeting(text):
    """
    回答文からよくある日本語メールの挨拶文を除去します。
    パターンは必要に応じて編集してください。
    """
    patterns = [
        r"いつもお世話になっております。?",
        r"お世話になっております。?",
        r"お疲れ様です。?",
        r"ご担当者様。?",
        r"日本恒生の.*です。?",
        r"こんにちは。?",
        r"こんばんは。?",
        r"初めまして。?",
        # ここにパターンを追加・修正してください
    ]
    for pat in patterns:
        text = re.sub(pat, "", text)
    return text.strip()

# Initialize DB at app startup
init_db()

# --- カテゴリ・タグの初期値をDBから取得しセッションで管理 ---
def get_unique_categories_and_tags():
    records = load_all_qa()
    categories = sorted(set(r['category'] for r in records if r['category']))
    tags = sorted(set(r['tag'] for r in records if r['tag']))
    return categories, tags

if 'categories' not in st.session_state or 'tags' not in st.session_state:
    st.session_state['categories'], st.session_state['tags'] = get_unique_categories_and_tags()

if selected == "対話":
    st.header("AIエージェント対話（メタエージェント自動ルーティング）")
    st.info("1つのフォームで質問すると、AIが最適な知識領域から自動回答します。どの知識領域から回答したかも明示します。")
    if "meta_agent" not in st.session_state:
        st.session_state["meta_agent"] = MetaAgent({
            "qa": QAAgent(),
            "api": APIAgent(),
        })
    meta_agent = st.session_state["meta_agent"]
    chat_history = st.session_state.get("meta_chat_history", [])
    user_input = st.text_input("💬 質問を入力してください（日本語）", key="meta_chat_input")
    if st.button("送信", key="meta_chat_send") and user_input:
        with st.spinner("AIが回答中..."):
            answer = meta_agent.route(user_input)
            last_agent = meta_agent.history[-1]["agent"] if meta_agent.history else "-"
            chat_history.append({"user": user_input, "answer": answer, "agent": last_agent})
            st.session_state["meta_chat_history"] = chat_history
    st.markdown("---")
    st.markdown("#### チャット履歴")
    for msg in reversed(chat_history):
        st.markdown(f"**ユーザー:** {msg['user']}")
        st.markdown(f"**AI({msg['agent']}知識領域):** {msg['answer']}")
        st.markdown("---")

elif selected == "一括QA登録":
    with st.container():
        st.markdown("""
            <style>
                .block-container {
                    padding-top: 1.5 rem;
                    }
            </style>
            """, unsafe_allow_html=True)
        st.header("一括QA登録")
        logging.basicConfig(filename='app.log', level=logging.INFO)
        embedding = get_embedding()
        if "qa_vectorstore" not in st.session_state:
            st.session_state["qa_vectorstore"] = None
        if "tag_set" not in st.session_state:
            st.session_state["tag_set"] = set()
        if "category_set" not in st.session_state:
            st.session_state["category_set"] = set()
        uploaded_file = st.file_uploader("📤 Excelファイルをアップロードしてください", type=["xlsx"])
        if uploaded_file:
            if not check_file_size(uploaded_file, max_size_mb=30):
                st.error("30MBを超えるファイルはアップロードできません。")
            else:
                try:
                    df = pd.read_excel(uploaded_file)
                    count = 0
                    for _, row in df.iterrows():
                        title = str(row.get("title", "")).strip()
                        category = str(row.get("category", "")).strip()
                        tag = str(row.get("tag", "")).strip()
                        content = str(row.get("content", "")).strip()
                        if title and content:
                            upsert_qa(title, category, tag, content)
                            count += 1
                    st.success(f"{count} 件のドキュメントをDBに登録しました。")
                    # DBから再取得してカテゴリ・タグを更新
                    st.session_state['categories'], st.session_state['tags'] = get_unique_categories_and_tags()
                    # ベクトルストアも再構築
                    all_qa = load_all_qa()
                    vs = create_or_load_qa_vectorstore(embedding)
                    vs = add_documents_to_qa_vectorstore(vs, all_qa, embedding)
                    st.session_state["qa_vectorstore"] = vs
                except Exception as e:
                    st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "QA 検索":
    with st.container():
        st.markdown("""
            <style>
                .block-container {
                    padding-top: 1.5 rem;
                    }
            </style>
            """, unsafe_allow_html=True)
        st.header("QA 検索・フィルタ")
        st.subheader("🔍 フィルタを選択（任意）")
        categories_filter = st.multiselect("システム選択:", options=st.session_state['categories'], key="category_filter", disabled=(len(st.session_state['categories'])==0))
        tags_filter = st.multiselect("タグ選択:", options=st.session_state['tags'], key="tag_filter", disabled=(len(st.session_state['tags'])==0))
        query = st.text_input("💬 質問を入力してください（日本語）")
        results = []
        answer = ""
        if query:
            add_query_history(st.session_state, query)
            with st.spinner("検索中..."):
                embedding = get_embedding()
                vs = st.session_state.get("qa_vectorstore") or create_or_load_qa_vectorstore(embedding)
                if vs is None:
                    st.error("Q&Aベクトルストアがまだ存在しません。先にファイルをアップロードしてください。")
                else:
                    try:
                        retriever = vs.as_retriever(search_kwargs={"k": 20})
                        all_results = retriever.invoke(query)
                        results = filter_docs(all_results, tags_filter, categories_filter)
                    except Exception as e:
                        st.error(f"検索中にエラーが発生しました: {e}")
                        logging.error(f"検索エラー: {e}")
                        results = []
                    if not results:
                        st.warning("該当する結果が見つかりませんでした。フィルタを確認してください。")
                    else:
                        context = "\n".join([f"- {doc.page_content}" for doc in results])
                        prompt = f"以下の情報だけを参考にしてください。\n\n{context}\n\n質問: {query}\n\n答え："
                        try:
                            answer = ask_deepseek(
                                system_prompt="あなたは日本語に堪能なアシスタントです。",
                                user_prompt=prompt
                            )
                        except Exception as e:
                            st.error(f"DeepSeek API呼び出し中にエラーが発生しました: {e}")
                            logging.error(f"DeepSeek APIエラー: {e}")
                            answer = ""
                        st.markdown("### ✨ 回答")
                        st.write(answer)
                        with st.expander("🔎 使用されたコンテキスト"):
                            for doc in results:
                                meta = doc.metadata if hasattr(doc, "metadata") else doc["metadata"]
                                st.markdown(
                                    f"- **{meta.get('title')}** | カテゴリ: `{meta.get('category', 'N/A')}` | "
                                    f"タグ: `{meta.get('tag', 'N/A')}` | システム: `{meta.get('category', 'N/A')}`\n\n"
                                    f"{doc.page_content}"
                                )
        # 検索履歴を画面下部に表示
        if "history" in st.session_state and st.session_state["history"]:
            st.markdown("---")
            st.markdown("#### 検索履歴")
            for q in reversed(st.session_state["history"]):
                st.write(q)
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "手動QA登録":
    with st.container():
        st.markdown("""
            <style>
                .block-container {
                    padding-top: 1.5 rem;
                    }
            </style>
            """, unsafe_allow_html=True)
        st.header("手動QA登録")
        st.info("問い合わせ内容・回答内容を入力し、要約やタイトルを自動生成できます。カテゴリ・タグを設定して保存してください。")
        question = st.text_area("問い合わせ内容（お客様からの質問）", height=100)
        answer = st.text_area("回答内容（担当者の返信）", height=100)
        if st.button("要約・タイトル自動生成", key="summarize"):
            if question and answer:
                with st.spinner("要約生成中..."):
                    try:
                        prompt_title = f"Q: {question}\nA: {answer}\n\nこの問い合わせと回答の要点を30文字以内で要約してください。"
                        title = ask_deepseek(system_prompt="あなたは日本語に堪能なアシスタントです。", user_prompt=prompt_title)
                        st.session_state["manual_title"] = title
                        answer_for_summary = remove_greeting(answer)
                        prompt_anssum = f"A: {answer_for_summary}\n\nこの回答内容の要点を30文字以内で要約してください。"
                        answer_summary = ask_deepseek(system_prompt="あなたは日本語に堪能なアシスタントです。", user_prompt=prompt_anssum)
                        st.session_state["manual_answer_summary"] = answer_summary
                    except Exception as e:
                        st.error(f"要約生成エラー: {e}")
            else:
                st.warning("問い合わせ内容と回答内容を両方入力してください。")
        title = st.text_input("タイトル（自動生成可・編集可）", value=st.session_state.get("manual_title", ""))
        category = st.selectbox("システム選択", options=[""]+st.session_state['categories'], key="category_select", disabled=(len(st.session_state['categories'])==0))
        tag = st.selectbox("タグ選択", options=[""]+st.session_state['tags'], key="tag_select", disabled=(len(st.session_state['tags'])==0))
        answer_summary = st.text_input("回答要約（自動生成可・編集可）", value=st.session_state.get("manual_answer_summary", ""))
        if st.button("保存", key="save_manual"):
            if title and question and answer:
                content = answer_summary if answer_summary else answer
                upsert_qa(title, category, tag, content)
                st.success("DBに保存しました。")
                st.session_state["manual_title"] = ""
                st.session_state["manual_answer_summary"] = ""
                # DBから再取得してカテゴリ・タグを更新
                st.session_state['categories'], st.session_state['tags'] = get_unique_categories_and_tags()
            else:
                st.warning("タイトル・問い合わせ内容・回答内容は必須です。")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "API仕様書登録":
    with st.container():
        st.markdown("""
            <style>
                .block-container {
                    padding-top: 1.5 rem;
                    }
            </style>
            """, unsafe_allow_html=True)
        st.header("API仕様書登録")
        st.info("API仕様書（WordまたはMarkdown）を登録できます。\nAPIDoc配下の全Markdownも一括登録可能です。")
        uploaded_file = st.file_uploader("📤 API仕様書（.docx）ファイルをアップロードしてください", type=["docx"])
        if uploaded_file:
            try:
                debug_word_structure(uploaded_file)
                sections = extract_sections_by_toc_template(uploaded_file)
                json_path = "extracted_sections.json"
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(sections, f, ensure_ascii=False, indent=2)
                st.success(f"{len(sections)}件のセクションを抽出しました（プレビュー）。")
                st.info(f"抽出データを {json_path} に保存しました。外部エディタ等でご確認ください。")
                with st.expander("抽出内容プレビュー（構造化）", expanded=False):
                    for i, sec in enumerate(sections):
                        st.markdown(f"**{i+1}. {sec.get('chapter','')} - {sec.get('section','')}**", unsafe_allow_html=True)
                        st.write(f"タイトル: {sec.get('title','')}")
                        st.markdown(f"<pre style='font-size:12px'>{sec.get('content','')[:500]}</pre>", unsafe_allow_html=True)
                        if sec.get('tables'):
                            st.markdown(f"**抽出された表:**")
                            st.table(pd.DataFrame(sec['tables'][0]))
                nlp_results = summarize_api_sections_with_nlp(sections)
                with st.expander("パラメータ・コード定義マッピングプレビュー", expanded=False):
                    for res in nlp_results:
                        if res['param_map']:
                            st.markdown(f"**{res['section_title']}**")
                            st.json(res['param_map'])
            except Exception as e:
                st.error(f"Wordファイルの解析中にエラーが発生しました: {e}")
        st.markdown("---")
        st.subheader("APIDoc配下のMarkdown一括登録")
        if st.button("APIDoc/ 配下のMarkdownを一括抽出・登録"):
            try:
                sections = extract_markdown_sections_from_apidoc()
                st.success(f"{len(sections)}件のMarkdownセクションを抽出しました。API仕様書ベクトルDBへ登録します。")
                embedding = get_embedding()
                vs = st.session_state.get("api_vectorstore") or create_or_load_api_vectorstore(embedding)
                vs = add_documents_to_api_vectorstore(vs, sections, embedding)
                st.session_state["api_vectorstore"] = vs
                st.info("登録完了。API仕様書検索で利用できます。")
                with st.expander("抽出内容プレビュー（構造化）", expanded=False):
                    for i, sec in enumerate(sections[:30]):
                        st.markdown(f"**{i+1}. {sec.get('spec_name','')} / {sec.get('filename','')} - {sec.get('section','')}**", unsafe_allow_html=True)
                        st.write(f"タイトル: {sec.get('title','')}")
                        st.markdown(f"<pre style='font-size:12px'>{sec.get('content','')[:500]}</pre>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Markdown一括登録中にエラーが発生しました: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "API仕様書検索":
    with st.container():
        st.markdown("""
            <style>
                .block-container {
                    padding-top: 1.5 rem;
                    }
            </style>
            """, unsafe_allow_html=True)
        st.header("API仕様書検索")
        st.info("API仕様書の内容に特化した検索・QA機能です。\nパラメータ詳細や仕様の根拠となる参照元（章・見出し）も必ず表示します。")
        query = st.text_input("💬 API仕様書に関する質問を入力してください（日本語）")
        results = []
        answer = ""
        if query:
            add_query_history(st.session_state, query)
            with st.spinner("検索中..."):
                embedding = get_embedding()
                vs = st.session_state.get("api_vectorstore") or create_or_load_api_vectorstore(embedding)
                if vs is None:
                    st.error("API仕様書ベクトルストアがまだ存在しません。先にAPI仕様書を登録してください。")
                else:
                    try:
                        retriever = vs.as_retriever(search_kwargs={"k": 10})
                        all_results = retriever.invoke(query)
                        results = [doc for doc in all_results if hasattr(doc, "metadata") and doc.metadata.get("category") == "API仕様書"]
                    except Exception as e:
                        st.error(f"検索中にエラーが発生しました: {e}")
                        results = []
                    if not results:
                        st.warning("該当する結果が見つかりませんでした。API仕様書の登録や質問内容をご確認ください。")
                    else:
                        context = "\n".join([f"- {doc.page_content}" for doc in results])
                        prompt = f"以下はAPI仕様書の抜粋です。これだけを参考にしてください。\n\n{context}\n\n質問: {query}\n\n答え："
                        try:
                            answer = ask_deepseek(
                                system_prompt="あなたはAPI仕様書の内容に精通したアシスタントです。回答には必ず参照元（章・見出し）を明記してください。",
                                user_prompt=prompt
                            )
                        except Exception as e:
                            st.error(f"DeepSeek API呼び出し中にエラーが発生しました: {e}")
                            answer = ""
                        st.markdown("### ✨ 回答")
                        st.write(answer)
                        with st.expander("🔎 使用されたAPI仕様書セクション（参照元）"):
                            for doc in results:
                                meta = doc.metadata
                                st.markdown(
                                    f"- **{meta.get('title', 'N/A')}**\n<pre style='font-size:12px'>{doc.page_content[:500]}</pre>", unsafe_allow_html=True
                                )
        # 検索履歴を画面下部に表示
        if "history" in st.session_state and st.session_state["history"]:
            st.markdown("---")
            st.markdown("#### 検索履歴")
            for q in reversed(st.session_state["history"]):
                st.write(q)
        st.markdown('</div>', unsafe_allow_html=True)

# 他のメニュー（Email, Charts, Tables）は今後拡張可能
